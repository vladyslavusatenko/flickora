from django.core.management.base import BaseCommand
from reports.models import MovieSection
from services.rag_service import RAGService

class Command(BaseCommand):
    help = 'Build FAISS index from movie sections'
    
    def handle(self, *args, **options):
        rag = RAGService()
        
        sections = MovieSection.objects.all()
        if not sections.exists():
            self.stdout.write(self.style.ERROR('No sections found'))
            return
        
        self.stdout.write(f"Building index from {sections.count()} sections...")
        
        rag.build_index_from_sections(sections)
        rag.save_index()
        
        self.stdout.write(self.style.SUCCESS('Index built successfully'))