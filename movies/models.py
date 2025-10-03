from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    director = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    plot_summary = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    runtime = models.IntegerField(null=True, blank=True)  # minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.year})"