from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .viewsets import (GenreViewSet, MovieViewSet, MovieSectionViewSet, ChatViewSet)
from .auth_views import (register, login, logout, update_profile, user_profile)
from . import views as legacy_views
from . import chat_views

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename = 'genre')
router.register(r'movies', MovieViewSet, basename = 'movie')
router.register(r'sections', MovieSectionViewSet, basename = 'section')


urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/register/', register, name='api_register'),
    path('auth/login/', login, name='api_login'),
    path('auth/logout/', logout, name='api_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', user_profile, name='user_profile'),
    path('auth/profile/update/', update_profile, name='update_profile'),
    
    path('chat/send/', chat_views.send_chat_message, name='chat_send'),
    
    path('import-movie/', legacy_views.import_movie, name='api_import_movie'),
    path('generate-section/', legacy_views.generate_section, name='api_generate_section'),
    path('generate-embedding/', legacy_views.generate_embedding, name='api_generate_embedding'),
    path('movie-status/<int:movie_id>/', legacy_views.movie_status, name='api_movie_status'),
    path('movie-sections/<int:movie_id>/', legacy_views.get_movie_sections, name='api_movie_sections'),
    path('movies-without-reports/', legacy_views.movies_without_reports, name='api_movies_without_reports'),
]