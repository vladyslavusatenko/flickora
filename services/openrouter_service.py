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
        self.model = "deepseek/deepseek-chat-v3.1:free"  # Your chosen free model
    
    def generate_movie_section(self, movie_data, section_type):
        """Generate a 500-word analysis section for a movie"""
        try:
            prompt = self._create_section_prompt(movie_data, section_type)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert film critic writing professional movie analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,  # Slightly higher for 500 words
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating section {section_type} for {movie_data.get('title', 'Unknown')}: {e}")
            return None
    
    def _create_section_prompt(self, movie_data, section_type):
        """Create prompt for specific section type"""
        
        section_instructions = {
            'basic_info': "Cover production history, budget, box office performance, critical reception, awards, cultural impact, and behind-the-scenes insights.",
            'cast_performances': "Analyze each main actor's performance, casting decisions, on-screen chemistry, preparation methods, and critical reception of performances.",
            'character_analysis': "Examine character psychology, development arcs, relationships, symbolic functions, and how characters embody themes.",
            'thematic_artistic': "Explore central themes, directorial vision, cinematography, production design, score, and visual symbolism.",
            'critical_reception': "Analyze major critics' reviews, audience reception, awards recognition, and evolution of critical opinion over time.",
            'legacy_impact': "Discuss long-term cultural influence, place in cinema history, and ongoing relevance."
        }
        
        instruction = section_instructions.get(section_type, "Provide detailed analysis of this aspect of the film.")
        
        prompt = f"""Write exactly 500 words analyzing the {section_type.replace('_', ' ').title()} for "{movie_data.get('title', '')}" ({movie_data.get('year', '')}).

Focus: {instruction}

Movie Details:
- Title: {movie_data.get('title', '')}
- Year: {movie_data.get('year', '')}
- Director: {movie_data.get('director', '')}
- Genre: {movie_data.get('genre', '')}
- Plot: {movie_data.get('plot_summary', '')}

Requirements:
- Write exactly 500 words
- Use professional film criticism language
- Include specific examples and details
- Write in flowing prose (no bullet points)
- Demonstrate deep cinematic knowledge

Begin the {section_type.replace('_', ' ').title()} analysis:"""
        
        return prompt