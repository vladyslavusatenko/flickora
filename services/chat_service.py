import openai
from django.conf import settings
from services.rag_service import RAGService
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model = "deepseek/deepseek-chat-v3.1:free"
        self.rag = RAGService()
        
    def chat(self, user_message, movie_id=None):
        results = self.rag.search_with_scores(user_message, k=3, movie_id=movie_id)
        sections = [r['section'] for r in results]
        
        context = "\n---\n".join([
            f"[{s.movie.title} - {s.get_section_type_display()}]\n{s.content}"
            for s in sections
        ])
        
        if movie_id:
            from movies.models import Movie
            movie = Movie.objects.get(id=movie_id)
            system_prompt = f"""You are discussing "{movie.title}" ({movie.year}).

Context from the movie:
{context}

Answer based on this context"""
        else:
            system_prompt = f"""You are a film expert.

Context:
{context}

Answer based on this context."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return{
                'message': response.choices[0].message.content.strip(),
                'sources': results
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return{
                'message': "Error occured",
                'sources': []
            }

