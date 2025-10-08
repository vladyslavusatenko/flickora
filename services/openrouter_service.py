import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OpenRouterService:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.model = "google/gemma-3-4b-it:free"  
    
    def generate_movie_section(self, movie_data, section_type):
        try:
            prompt = self._create_section_prompt(movie_data, section_type)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating section {section_type} for {movie_data.get('title', 'Unknown')}: {e}")
            return None
    
    def _create_section_prompt(self, movie_data, section_type):
        section_instructions = {
            'basic_info': """Write EXACTLY 500 words analyzing the production, budget, box office, awards, and cultural impact. 
            Focus on: production history, financial performance, critical reception, awards won, behind-the-scenes stories, and initial cultural reception.""",
            
            'cast_performances': """Write EXACTLY 500 words analyzing actor performances.
            Focus on: each main actor's technique, casting decisions, on-screen chemistry, preparation methods, memorable scenes, critical reception of performances, and career context.""",
            
            'character_analysis': """Write EXACTLY 500 words analyzing character psychology and development.
            Focus on: character motivations, internal conflicts, character arcs, relationships, symbolic functions, how characters embody themes, and psychological depth.""",
            
            'thematic_artistic': """Write EXACTLY 500 words analyzing themes and artistic elements.
            Focus on: central themes, directorial vision, cinematography techniques, production design, musical score, editing style, and visual symbolism.""",
            
            'critical_reception': """Write EXACTLY 500 words analyzing reviews and critical reception.
            Focus on: major critics' opinions (with specific examples), professional reviews, audience reception, festival response, awards recognition, and evolution of critical opinion.""",
            
            'legacy_impact': """Write EXACTLY 500 words analyzing long-term influence and legacy.
            Focus on: cultural impact, influence on later films, place in cinema history, ongoing relevance, and lasting significance in film culture."""
        }
        
        instruction = section_instructions.get(section_type, "Write EXACTLY 500 words of detailed analysis.")
        
        genres_str = movie_data.get('genres', '') if isinstance(movie_data.get('genres'), str) else ', '.join([g.name for g in movie_data.get('genres', [])])
        
        prompt = f"""You are an expert film critic. Write EXACTLY 500 words of analysis. Do NOT include any titles, headings, or labels. Start directly with the analysis text.

Movie: "{movie_data.get('title', '')}" ({movie_data.get('year', '')})
Director: {movie_data.get('director', '')}
Genres: {genres_str}
Plot: {movie_data.get('plot_summary', '')}

{instruction}

CRITICAL RULES:
- Write EXACTLY 500 words (not 400, not 600 - exactly 500)
- NO titles, NO headings, NO section labels, NO hashtags
- Start immediately with the analysis
- Write in flowing prose paragraphs
- Use professional film criticism language
- Include specific examples and details
- Demonstrate deep cinematic knowledge

Begin writing the 500-word analysis NOW:"""
        
        return prompt