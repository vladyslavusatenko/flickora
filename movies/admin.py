from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['tmdb_id', 'id', 'title', 'year', 'director', 'genre', 'imdb_rating']
    list_filter = ['year', 'genre']
    search_fields = ['title', 'director']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['id']