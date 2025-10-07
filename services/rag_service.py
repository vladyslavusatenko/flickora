from sentence_transformers import SentenceTransformer
from django.conf import settings
import logging
from pgvector.django import CosineDistance


logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_dim = 384
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        return self.model
    
    def generate_embedding(self, text):
        model = self.load_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.astype('float32')
    
        
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
        
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Build query with pgvector cosine distance
        queryset = MovieSection.objects.filter(
            embedding__isnull=False
        ).annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')
        
        # Filter by movie if specified
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        
        # Get top k results
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
                'similarity': 1.0 - section.distance,  # Convert distance to similarity
                'movie_title': section.movie.title,
                'section_type': section.get_section_type_display()
            }
            for section in results
        ]