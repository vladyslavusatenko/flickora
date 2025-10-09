from sentence_transformers import SentenceTransformer
from django.conf import settings
import logging
from pgvector.django import CosineDistance
import torch

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_dim = 384
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            try:
                # Force download and load properly
                self.model = SentenceTransformer(
                    self.model_name,
                    device='cpu',
                    cache_folder=None  # Use default cache
                )
                # Ensure model is on CPU and fully loaded
                self.model = self.model.to('cpu')
                self.model.eval()
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise
        return self.model
    
    def generate_embedding(self, text):
        try:
            model = self.load_model()
            # Encode with proper settings
            embedding = model.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=False
            )
            return embedding.astype('float32')
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
        
    def search(self, query, k=5, movie_id=None):
        """
        Search for similar movie sections using pgvector
        
        Args:
            query: Search query text
            k: Number of results to return
            movie_id: Optional movie ID to filter results
            
        Returns:
            QuerySet of MovieSection objects ordered by similarity
        """
        from reports.models import MovieSection
        
        query_embedding = self.generate_embedding(query)
        
        queryset = MovieSection.objects.filter(
            embedding__isnull=False
        ).annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')
        
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        
        results = queryset[:k]
        
        logger.info(f"Found {len(results)} results for query: {query[:50]}...")
        
        return results
    
    def search_with_scores(self, query, k=5, movie_id=None):
        """
        Search and return results with similarity scores
        
        Returns:
            List of dicts with 'section' and 'similarity' keys
        """
        results = self.search(query, k, movie_id)
        
        return [
            {
                'section': section,
                'section_id': section.id,
                'similarity': 1.0 - section.distance,
                'movie_title': section.movie.title,
                'section_type': section.get_section_type_display()
            }
            for section in results
        ]