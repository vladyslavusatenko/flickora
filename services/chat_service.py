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
        results = self.rag.search_with_scores(user_message, k=2, movie_id=movie_id)
        sections = [r['section'] for r in results]
        
        context = "\n---\n".join([
            f"[{s.movie.title} - {s.get_section_type_display()}]\n{s.content[:600]}"
            for s in sections
        ])
        
        if movie_id:
            from movies.models import Movie
            movie = Movie.objects.get(id=movie_id)
            system_prompt = f"""You are a knowledgeable movie assistant discussing "{movie.title}" ({movie.year}).

Context from the movie:
{context}

CRITICAL RULES:
- Answer the question COMPLETELY but CONCISELY
- Get straight to the point - no fluff or repetition
- Use 3-5 sentences maximum (or about 100-150 words)
- Focus ONLY on what the user asked
- Don't repeat the same information in different words
- Be conversational and engaging
- If you don't have enough context, say so briefly

Answer the user's question directly:"""
        else:
            system_prompt = f"""You are a knowledgeable movie expert.

Context:
{context}

CRITICAL RULES:
- Answer the question COMPLETELY but CONCISELY
- Get straight to the point - no fluff or repetition
- Use 3-5 sentences maximum (or about 100-150 words)
- Focus ONLY on what the user asked
- Don't repeat the same information in different words
- Be conversational and engaging

Answer based on this context:"""
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
            
            sentences = answer.split('. ')
            if len(sentences) > 6:
                answer = '. '.join(sentences[:6]) + '.'
            
            return{
                'message': answer,
                'sources': results
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return{
                'message': "Sorry, I encountered an error. Please try again.",
                'sources': []
            }
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
        results = self.rag.search_with_scores(user_message, k=2, movie_id=movie_id)
        sections = [r['section'] for r in results]
        
        context = "\n---\n".join([
            f"[{s.movie.title} - {s.get_section_type_display()}]\n{s.content[:500]}"
            for s in sections
        ])
        
        if movie_id:
            from movies.models import Movie
            movie = Movie.objects.get(id=movie_id)
            system_prompt = f"""You are a helpful movie assistant discussing "{movie.title}" ({movie.year}).

Context from the movie analysis:
{context}

IMPORTANT RULES:
- Keep responses SHORT and CONCISE (max 2-3 sentences or 150 words)
- Answer directly and conversationally
- Focus on the most relevant information
- Don't repeat information unnecessarily
- Be engaging but brief

Answer the user's question based on this context."""
        else:
            system_prompt = f"""You are a helpful movie expert assistant.

Context:
{context}

IMPORTANT RULES:
- Keep responses SHORT and CONCISE (max 2-3 sentences or 150 words)
- Answer directly and conversationally
- Focus on the most relevant information
- Don't repeat information unnecessarily
- Be engaging but brief

Answer based on this context."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return{
                'message': response.choices[0].message.content.strip(),
                'sources': results
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return{
                'message': "Sorry, I encountered an error. Please try again.",
                'sources': []
            }