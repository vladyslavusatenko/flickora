import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from django.conf import settings
import logging
import pickle
import os

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_dim = 384
        self.model = None
        self.index = None
        self.section_ids = []
        self.index_path = settings.BASE_DIR / "data" / "faiss_index/bin"
        self.metadata_path = settings.BASE_DIR / "data" / "faiss_metadata.pkl"
        
    def load_model(self):
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        return self.model
    
    def generate_embedding(self, text):
        model = self.load_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.astype('float32')
    
    def build_index_from_sections(self, sections):
        logger.info(f"Building FAISS index from {len(sections)} sections")
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.section_ids = []
        
        embeddings = []
        for section in sections:
            embedding = self.generate_embedding(section.content)
            embeddings.append(embedding)
            self.section_ids.append(section.id)
            
        embeddings_array = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings_array)
        self.index.add(embeddings_array)
        
        logger.info(f"Index built with {self.index.ntotal} vectors")
        return self.index
    
    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.section_ids, f)
            
            logger.info(f"index saved to {self.index_path}")
            
    def load_index(self):
        if not os.path.exists(self.index_path):
            return False
        
        self.index = faiss.read_index(str(self.index_path))
        
        with open(self.metadata_path, 'rb') as f:
            self.section_ids = pickle.load(f)
            
        logger.info(f"index loaded with {self.index.ntotal} vectors")
        return True
    
    def search(self, query, k=5):
        if self.index is None:
            if not self.load_index():
                logger.error("No index available")
                return []
        
        query_embedding = self.generate_embedding(query)
        faiss.normalize_L2(query_embedding.reshape(1, -1))
        
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.section_ids):
                results.append({
                    'section_id': self.section_ids[idx],
                    'similarity': float(dist)
                })
        
        return results