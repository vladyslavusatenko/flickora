import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinechat.settings')
django.setup()

from services.tmdb_service import TMDBService
from services.openrouter_service import OpenRouterService

# Test TMDB
tmdb = TMDBService()
movie_data = tmdb.get_movie_details(278)  # Shawshank Redemption
print("TMDB Test:", movie_data['title'] if movie_data else "Failed")

# Test OpenRouter
openrouter = OpenRouterService()
if movie_data:
    section = openrouter.generate_movie_section(movie_data, 'basic_info')
    print("OpenRouter Test:", "Success" if section else "Failed")
    print(section)