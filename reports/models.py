from django.db import models
from movies.models import Movie

class MovieSection(models.Model):
    SECTION_TYPES = [
        ('basic_info', 'Basic Information'),
        ('cast_performances', 'Cast & Performances'),
        ('character_analysis', 'Character Analysis'),
        ('thematic_artistic', 'Thematic & Artistic Elements'),
        ('critical_reception', 'Critical Reception & Reviews'),
        ('legacy_impact', 'Legacy & Cultural Impact'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    content = models.TextField()
    word_count = models.IntegerField(default=0)
    key_topics = models.JSONField(default=list, blank=True)  # For storing extracted topics
    generated_at = models.DateTimeField(auto_now_add=True)
    embedding = models.TextField(default=0)
    
    class Meta:
        unique_together = ['movie', 'section_type']
        ordering = ['movie', 'section_type']
        indexes = [
            models.Index(fields=['section_type']),
            models.Index(fields=['generated_at']),
        ]
    def __str__(self):
        return f"{self.movie.title} - {self.get_section_type_display()}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate word count
        if self.content:
            self.word_count = len(self.content.split())
        super().save(*args, **kwargs)