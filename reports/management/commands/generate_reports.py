from django.core.management.base import BaseCommand
from movies.models import Movie
from reports.models import MovieSection
from services.openrouter_service import OpenRouterService
import time

class Command(BaseCommand):
    help = 'Generate AI reports for movies'
    
    def add_arguments(self, parser):
        parser.add_argument('--movie-id', type=int, help='Generate report for specific movie')
        parser.add_argument('--all', action='store_true', help='Generate reports for all movies without reports')
        parser.add_argument('--limit', type=int, default=5, help='Limit number of movies to process')
    
    def handle(self, *args, **options):
        openrouter = OpenRouterService()
        
        # Get movies to process
        if options['movie_id']:
            movies = Movie.objects.filter(id=options['movie_id'])
        elif options['all']:
            movies = Movie.objects.filter(sections__isnull=True).distinct()[:options['limit']]
        else:
            movies = Movie.objects.filter(sections__isnull=True).distinct()[:options['limit']]
        
        if not movies:
            self.stdout.write(self.style.WARNING('No movies to process'))
            return
        
        section_types = [
            'basic_info',
            'cast_performances', 
            'character_analysis',
            'thematic_artistic',
            'critical_reception',
            'legacy_impact'
        ]
        
        total_generated = 0
        
        for movie in movies:
            self.stdout.write(f"\nProcessing: {movie.title} ({movie.year})")
            
            movie_data = {
                'title': movie.title,
                'year': movie.year,
                'director': movie.director,
                'genre': movie.genre,
                'plot_summary': movie.plot_summary
            }
            
            for section_type in section_types:
                # Check if section already exists
                if MovieSection.objects.filter(movie=movie, section_type=section_type).exists():
                    self.stdout.write(f"  - {section_type}: already exists")
                    continue
                
                try:
                    self.stdout.write(f"  - Generating {section_type}...")
                    
                    content = openrouter.generate_movie_section(movie_data, section_type)
                    
                    if content:
                        MovieSection.objects.create(
                            movie=movie,
                            section_type=section_type,
                            content=content
                        )
                        total_generated += 1
                        self.stdout.write(self.style.SUCCESS(f"    ✓ Generated ({len(content.split())} words)"))
                    else:
                        self.stdout.write(self.style.ERROR(f"    ✗ Failed to generate"))
                    
                    # Rate limiting - wait 1 second between API calls
                    time.sleep(1)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ✗ Error: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"\nTotal sections generated: {total_generated}"))