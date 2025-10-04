from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()[:20]
    return render(request, 'movies/list.html', {'movies':movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    sections = movie.sections.all()
    return render(request, 'movies/detail.html', {
        'movie': movie,
        'sections': sections
    })

# Create your views here.

class MovieListView(ListView):
    model = Movie
    template_name = 'movies/list.html'
    context_object_name = 'movies'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Movie.objects.all().prefetch_related('sections')
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(director__icontains=search_query)
            )
        
        return queryset.order_by('-year', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/detail.html'
    context_object_name = 'movie'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.sections.all().order_by('section_type')
        return context