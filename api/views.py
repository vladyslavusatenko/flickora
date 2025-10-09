from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from movies.models import Movie, Genre
from reports.models import MovieSection
from services.tmdb_service import TMDBService
from services.openrouter_service import OpenRouterService
from services.rag_service import RAGService
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def import_movie(request):
    """
    Import movie from TMDB
    POST /api/import-movie/
    Body: {"tmdb_id": 278}
    """
    try:
        data = json.loads(request.body)
        tmdb_id = data.get('tmdb_id')
        
        if not tmdb_id:
            return JsonResponse({'error': 'tmdb_id required'}, status=400)
        
        tmdb = TMDBService()
        movie_data = tmdb.get_movie_details(tmdb_id)
        
        if not movie_data:
            return JsonResponse({'error': 'Movie not found in TMDB'}, status=404)
        
        movie, created = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': movie_data['title'],
                'year': int(movie_data['release_date'][:4]) if movie_data.get('release_date') else 2024,
                'director': get_director(movie_data),
                'plot_summary': movie_data.get('overview', ''),
                'runtime': movie_data.get('runtime'),
                'imdb_rating': movie_data.get('vote_average'),
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get('poster_path') else '',
                'backdrop_url': f"https://image.tmdb.org/t/p/w1280{movie_data['backdrop_path']}" if movie_data.get('backdrop_path') else '',
            }
        )
        
        for genre_data in movie_data.get('genres', []):
            genre, _ = Genre.objects.get_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
            movie.genres.add(genre)
        
        return JsonResponse({
            'success': True,
            'created': created,
            'movie': {
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'tmdb_id': movie.tmdb_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error importing movie: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_section(request):
    """
    Generate single section for movie
    POST /api/generate-section/
    Body: {"movie_id": 1, "section_type": "basic_info"}
    """
    try:
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        section_type = data.get('section_type')
        
        if not movie_id or not section_type:
            return JsonResponse({'error': 'movie_id and section_type required'}, status=400)
        
        movie = Movie.objects.get(id=movie_id)
        
        if MovieSection.objects.filter(movie=movie, section_type=section_type).exists():
            return JsonResponse({'error': 'Section already exists'}, status=400)
        
        openrouter = OpenRouterService()
        movie_data = {
            'title': movie.title,
            'year': movie.year,
            'director': movie.director,
            'genres': ', '.join([g.name for g in movie.genres.all()]),
            'plot_summary': movie.plot_summary
        }
        
        content = openrouter.generate_movie_section(movie_data, section_type)
        
        if not content:
            return JsonResponse({'error': 'Failed to generate content'}, status=500)
        
        section = MovieSection.objects.create(
            movie=movie,
            section_type=section_type,
            content=content,
            embedding=None
        )
        
        return JsonResponse({
            'success': True,
            'section': {
                'id': section.id,
                'section_type': section.section_type,
                'word_count': section.word_count,
                'movie_id': movie.id
            }
        })
        
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    except Exception as e:
        logger.error(f"Error generating section: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_embedding(request):
    """
    Generate embedding for section using management command
    POST /api/generate-embedding/
    Body: {"section_id": 1}
    """
    try:
        data = json.loads(request.body)
        section_id = data.get('section_id')
        
        if not section_id:
            return JsonResponse({'error': 'section_id required'}, status=400)
        
        section = MovieSection.objects.get(id=section_id)
        
        if section.embedding is not None and len(section.embedding) > 0:
            return JsonResponse({'error': 'Embedding already exists'}, status=400)
        
        # Use management command instead of RAGService
        from django.core.management import call_command
        import io
        
        out = io.StringIO()
        call_command('generate_embeddings', section_id=section_id, stdout=out)
        
        # Refresh from DB
        section.refresh_from_db()
        
        if section.embedding is not None and len(section.embedding) > 0:
            return JsonResponse({
                'success': True,
                'section_id': section.id,
                'embedding_dimensions': len(section.embedding)
            })
        else:
            return JsonResponse({'error': 'Embedding generation failed'}, status=500)
        
    except MovieSection.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def movie_status(request, movie_id):
    """
    Check movie report status
    GET /api/movie-status/<movie_id>/
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        sections = MovieSection.objects.filter(movie=movie)
        
        section_status = {}
        for section in sections:
            section_status[section.section_type] = {
                'exists': True,
                'word_count': section.word_count,
                'has_embedding': section.embedding is not None and len(section.embedding) > 0
            }
        
        all_types = ['basic_info', 'cast_performances', 'character_analysis', 
                     'thematic_artistic', 'critical_reception', 'legacy_impact']
        
        for section_type in all_types:
            if section_type not in section_status:
                section_status[section_type] = {
                    'exists': False,
                    'word_count': 0,
                    'has_embedding': False
                }
        
        return JsonResponse({
            'movie_id': movie.id,
            'title': movie.title,
            'sections': section_status,
            'total_sections': sections.count(),
            'complete': sections.count() == 6
        })
        
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)


@require_http_methods(["GET"])
def movies_without_reports(request):
    """
    Get list of movies without complete reports OR missing embeddings
    GET /api/movies-without-reports/?limit=10
    """
    limit = int(request.GET.get('limit', 10))
    
    # Movies with incomplete sections OR missing embeddings
    movies = Movie.objects.annotate(
        section_count=models.Count('sections'),
        sections_with_embeddings=models.Count(
            'sections',
            filter=models.Q(sections__embedding__isnull=False)
        )
    ).filter(
        models.Q(section_count__lt=6) |  # Less than 6 sections
        models.Q(section_count__gt=models.F('sections_with_embeddings'))  # Missing embeddings
    ).order_by('id')[:limit]
    
    result = []
    for movie in movies:
        result.append({
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'tmdb_id': movie.tmdb_id,
            'sections_count': movie.section_count,
            'embeddings_count': movie.sections_with_embeddings
        })
    
    return JsonResponse({
        'count': len(result),
        'movies': result
    })


@require_http_methods(["GET"])
def get_movie_sections(request, movie_id):
    """
    Get all sections for a movie with their IDs
    GET /api/movie-sections/<movie_id>/
    """
    try:
        movie = Movie.objects.get(id=movie_id)
        sections = MovieSection.objects.filter(movie=movie)
        
        result = {}
        for section in sections:
            result[section.section_type] = {
                'id': section.id,
                'section_type': section.section_type,
                'word_count': section.word_count,
                'has_embedding': section.embedding is not None and len(section.embedding) > 0
            }
        
        return JsonResponse({
            'movie_id': movie.id,
            'movie_title': movie.title,
            'sections': result
        })
        
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)


def get_director(movie_data):
    if 'credits' in movie_data and 'crew' in movie_data['credits']:
        for person in movie_data['credits']['crew']:
            if person['job'] == 'Director':
                return person['name']
    return 'Unknown Director'