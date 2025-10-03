from django.contrib import admin
from .models import MovieSection

@admin.register(MovieSection)
class MovieSectionAdmin(admin.ModelAdmin):
    list_display = ['movie', 'section_type', 'word_count', 'generated_at']
    list_filter = ['section_type', 'generated_at']
    search_fields = ['movie__title', 'content']
    readonly_fields = ['word_count', 'generated_at']