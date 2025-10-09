from django.urls import path
from . import views

urlpatterns = [
    path('import-movie/', views.import_movie, name='api_import_movie'),
    path('generate-section/', views.generate_section, name='api_generate_section'),
    path('generate-embedding/', views.generate_embedding, name='api_generate_embedding'),
    path('movie-status/<int:movie_id>/', views.movie_status, name='api_movie_status'),
    path('movie-sections/<int:movie_id>/', views.get_movie_sections, name='api_movie_sections'),
    path('movies-without-reports/', views.movies_without_reports, name='api_movies_without_reports'),
]