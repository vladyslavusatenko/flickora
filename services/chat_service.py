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
        self.model = "meta-llama/llama-4-maverick:free"
        self.rag = RAGService()
    
    def chat(self, user_message, movie_id=None):
        """
        Enhanced chat with better context retrieval (8 sections)
        """
        # Use enhanced RAG with prioritization
        if movie_id:
            # Movie-specific: fewer but more relevant sections
            results = self.rag.search_with_scores(user_message, k=3, movie_id=movie_id)
        else:
            # Global search: more sections from different movies
            results = self.rag.search_with_scores(user_message, k=5, movie_id=None)
        
        sections = [r['section'] for r in results]
        
        # Build context with MORE content per section
        context_parts = []
        for s in sections:
            # Use more content based on section importance
            content_length = self._get_context_length(s.section_type, movie_id)
            
            context_parts.append(
                f"[{s.movie.title} - {s.get_section_type_display()}]\n"
                f"{s.content[:content_length]}"
            )
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Build system prompt
        if movie_id:
            from movies.models import Movie
            movie = Movie.objects.get(id=movie_id)
            system_prompt = f"""You are a knowledgeable movie assistant discussing "{movie.title}" ({movie.year}).

Context from the movie analysis:
{context}

IMPORTANT RULES:
- Answer DIRECTLY and COMPLETELY but stay CONCISE
- Use 3-5 sentences (100-150 words maximum)
- Focus ONLY on what the user asked
- Be conversational and engaging
- If context doesn't have the answer, say so briefly
- Don't repeat information unnecessarily

Answer the user's question based on this context."""
        else:
            system_prompt = f"""You are a knowledgeable movie expert assistant.

Context from movie analyses:
{context}

IMPORTANT RULES:
- Answer DIRECTLY and COMPLETELY but stay CONCISE
- Use 3-5 sentences (100-150 words maximum)  
- Focus ONLY on what the user asked
- Mention movie titles when relevant
- Be conversational and engaging
- If context doesn't have the answer, say so briefly

Answer based on this context."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=250,
                temperature=0.7,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Quality control: trim if too long
            sentences = answer.split('. ')
            if len(sentences) > 6:
                answer = '. '.join(sentences[:6]) + '.'
            
            return {
                'message': answer,
                'sources': results
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'message': "Sorry, I encountered an error. Please try again.",
                'sources': []
            }
    
    def _get_context_length(self, section_type, movie_id):
        """
        Determine how much content to include based on section type and chat mode (8 sections)
        """
        # Priority sections get more context
        high_priority = ['plot_structure', 'characters', 'themes']
        medium_priority = ['visual_technical', 'production', 'cast_crew']
        low_priority = ['reception', 'legacy']
        
        if movie_id:
            # Movie-specific: can use more context per section
            if section_type in high_priority:
                return 1200  # ~200 words
            elif section_type in medium_priority:
                return 900   # ~150 words
            else:
                return 600   # ~100 words
        else:
            # Global search: use less per section since we have more movies
            if section_type in high_priority:
                return 800   # ~130 words
            elif section_type in medium_priority:
                return 600   # ~100 words
            else:
                return 400   # ~70 words