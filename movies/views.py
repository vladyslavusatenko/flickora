from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Movie, Genre

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/list.html'
    context_object_name = 'movies'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related('sections', 'genres')
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(director__icontains=search_query)
            )
        
        genre_filter = self.request.GET.get('genre')
        if genre_filter:
            queryset = queryset.filter(genres__tmdb_id=genre_filter).distinct()
        
        year_filter = self.request.GET.get('year')
        if year_filter and year_filter != 'all':
            queryset = queryset.filter(year=year_filter)
        
        return queryset.order_by('-year', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['selected_year'] = self.request.GET.get('year', 'all')
        
        context['all_genres'] = Genre.objects.annotate(
            movie_count=Count('movies')
        ).filter(movie_count__gt=0).order_by('name')
        
        context['all_years'] = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')
        
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/detail.html'
    context_object_name = 'movie'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.sections.all().order_by('section_type')
        return context