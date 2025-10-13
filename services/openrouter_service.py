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
            'basic_info': """Write EXACTLY 500 words analyzing the production, budget, box office, awards, and reception. 
            Focus on: production history, financial performance, critical acclaim, awards won, behind-the-scenes stories, and initial reception.
            Be informative and insightful, but write clearly so anyone interested in film can understand.""",
            
            'cast_performances': """Write EXACTLY 500 words analyzing the actors and their performances.
            Focus on: what each actor brings to their role, casting decisions, chemistry between actors, memorable performances, and critical praise.
            Be analytical but accessible - explain acting techniques in clear terms.""",
            
            'character_analysis': """Write EXACTLY 500 words analyzing the characters and their development.
            Focus on: character motivations, development arcs, relationships, and what they represent in the story.
            Be thoughtful but clear - make character psychology accessible to general audiences.""",
            
            'thematic_artistic': """Write EXACTLY 500 words analyzing themes and artistic elements.
            Focus on: central themes, directorial vision, cinematography, production design, musical score, and visual symbolism.
            Be sophisticated but accessible - explain artistic choices in understandable terms.""",
            
            'critical_reception': """Write EXACTLY 500 words analyzing reviews and critical reception.
            Focus on: what critics said (with specific examples), audience reactions, awards recognition, and how opinions evolved.
            Be thorough but readable - present critical perspectives clearly.""",
            
            'legacy_impact': """Write EXACTLY 500 words analyzing the film's lasting impact.
            Focus on: influence on other films, cultural significance, ongoing relevance, and place in cinema history.
            Be insightful but accessible - explain the film's importance in clear terms."""
        }
        
        instruction = section_instructions.get(section_type, "Write EXACTLY 500 words of thoughtful, accessible analysis.")
        
        genres_str = movie_data.get('genres', '') if isinstance(movie_data.get('genres'), str) else ', '.join([g.name for g in movie_data.get('genres', [])])
        
        prompt = f"""You are a knowledgeable film writer creating accessible, engaging analysis for movie enthusiasts.

Movie: "{movie_data.get('title', '')}" ({movie_data.get('year', '')})
Director: {movie_data.get('director', '')}
Genres: {genres_str}
Plot: {movie_data.get('plot_summary', '')}

{instruction}

CRITICAL STYLE GUIDELINES:
- Write EXACTLY 500 words (not 400, not 600 - exactly 500)
- NO titles, NO headings, NO section labels, NO hashtags
- Start directly with the analysis
- Write in flowing, clear paragraphs
- Be intelligent and insightful, but accessible
- Use precise language, but explain complex concepts clearly
- Avoid overly academic jargon - choose clear words over complicated ones
- Include specific examples and details
- Write for educated general audiences, not film scholars
- Balance depth with readability

Think: "Smart magazine article" not "academic paper" or "casual blog post"

Begin writing the 500-word analysis NOW:"""
        
        return prompt
