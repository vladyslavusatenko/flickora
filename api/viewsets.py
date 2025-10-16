from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend

from movies.models import Movie, Genre, MovieView
from movies.serializers import (
    MovieListSerializer, MovieDetailSerializer,
    GenreSerializer, MovieViewSerializer
)
from reports.models import MovieSection
from reports.serializers import MovieSectionSerializer, MovieSectionListSerializer
from chat.models import ChatConversation, ChatMessage
from chat.serializers import (
    ChatConversationSerializer, ChatRequestSerializer,
    ChatResponseSerializer
)
from services.chat_service import ChatService


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for movie genres"""
    queryset = Genre.objects.annotate(
        movie_count=Count('movies')
    ).filter(movie_count__gt=0).order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for movies with filtering and search"""
    queryset = Movie.objects.prefetch_related('genres', 'sections')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['year', 'genres__tmdb_id']
    search_fields = ['title', 'director']
    ordering_fields = ['year', 'title', 'imdb_rating', 'created_at']
    ordering = ['-year', 'title']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer
    
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        """Get all sections for a movie"""
        movie = self.get_object()
        sections = movie.sections.all().order_by('section_type')
        serializer = MovieSectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def view(self, request, pk=None):
        """Mark movie as viewed by current user"""
        movie = self.get_object()
        view, created = MovieView.objects.update_or_create(
            user=request.user,
            movie=movie
        )
        serializer = MovieViewSerializer(view)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending movies"""
        movies = self.get_queryset().order_by('-created_at')[:20]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recently_viewed(self, request):
        """Get recently viewed movies for current user"""
        views = MovieView.objects.filter(
            user=request.user
        ).select_related('movie').order_by('-viewed_at')[:10]
        
        movies = [view.movie for view in views]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)


class MovieSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for movie sections"""
    queryset = MovieSection.objects.select_related('movie')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'section_type']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSectionListSerializer
        return MovieSectionSerializer


class ChatViewSet(viewsets.ViewSet):
    """API endpoint for chat functionality"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def message(self, request):
        """Send a message and get AI response"""
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.validated_data['message']
        movie_id = serializer.validated_data.get('movie_id')
        conversation_id = serializer.validated_data.get('conversation_id')
        
        # Get or create conversation
        if conversation_id:
            try:
                conversation = ChatConversation.objects.get(id=conversation_id)
            except ChatConversation.DoesNotExist:
                conversation = None
        else:
            conversation = None
        
        if not conversation:
            conversation = ChatConversation.objects.create(
                conversation_type='movie' if movie_id else 'global',
                movie_id=movie_id
            )
        
        # Save user message
        ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=message
        )
        
        # Get AI response
        chat_service = ChatService()
        result = chat_service.chat(message, movie_id)
        
        # Save assistant message
        ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=result['message'],
            context_sections=[
                {
                    'section_id': source['section_id'],
                    'similarity': source['similarity'],
                    'movie_title': source['movie_title'],
                    'section_type': source['section_type']
                }
                for source in result['sources']
            ]
        )
        
        # Prepare response
        response_data = {
            'message': result['message'],
            'conversation_id': conversation.id,
            'sources': [
                {
                    'section_id': source['section_id'],
                    'similarity': source['similarity'],
                    'movie_title': source['movie_title'],
                    'section_type': source['section_type']
                }
                for source in result['sources']
            ]
        }
        
        response_serializer = ChatResponseSerializer(response_data)
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Get user's chat conversations"""
        conversations = ChatConversation.objects.all().order_by('-updated_at')[:20]
        serializer = ChatConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def conversation_detail(self, request, pk=None):
        """Get conversation with all messages"""
        try:
            conversation = ChatConversation.objects.get(id=pk)
        except ChatConversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ChatConversationSerializer(conversation)
        return Response(serializer.data)