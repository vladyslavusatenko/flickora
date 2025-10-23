import { useQuery } from '@tanstack/react-query';
import { moviesAPI } from '../api';
import { Search, MessageCircle, Star, ChevronLeft, ChevronRight } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { useState } from 'react';
import LoadingSpinner from '../components/common/loadingSpinner';
import '../styles/pages/Home.css';

const Home = () => {
  const navigate = useNavigate();
  const [trendingScroll, setTrendingScroll] = useState(0);

  const { data: trendingData, isLoading: trendingLoading } = useQuery({
    queryKey: ['trending'],
    queryFn: moviesAPI.getTrending
  });

  const { data: topMoviesData, isLoading: topLoading } = useQuery({
    queryKey: ['top-movies'],
    queryFn: () => moviesAPI.getMovies({ limit: 20, ordering: '-imdb_rating' })
  });

  const trendingMovies = trendingData?.data?.results || trendingData?.data || [];
  const topMovies = topMoviesData?.data?.results || topMoviesData?.data || [];

  const popularQuestions = [
    {
      question: "What are the best sci-fi movies of 2024?",
      category: "sci-fi"
    },
    {
      question: "Recommend movies similar to Christopher Nolan films",
      category: "recommendations"
    },
    {
      question: "What's trending in horror movies right now?",
      category: "trending"
    }
  ];

  const handleAskAI = (question) => {
    navigate('/chat', { state: { initialQuestion: question } });
  };

  if (trendingLoading || topLoading) {
    return <LoadingSpinner size="lg" />;
  }

  return (
    <div className="home-new">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to CineChat</h1>
          <p className="hero-subtitle">Your AI-Powered Movie Discovery Platform</p>
          
          <div className="hero-actions">
            <button 
              className="hero-btn hero-btn-primary"
              onClick={() => navigate('/movies')}
            >
              <Search size={20} />
              Search Movies
            </button>
            <button 
              className="hero-btn hero-btn-secondary"
              onClick={() => navigate('/chat')}
            >
              <MessageCircle size={20} />
              Start Chatting
            </button>
          </div>
        </div>
      </div>

      <div className="home-content">
        <div className="popular-questions-section">
          <h2 className="section-title">Popular Questions</h2>
          
          <div className="popular-questions-grid">
            {popularQuestions.map((item, index) => (
              <div key={index} className="question-card">
                <p className="question-text">{item.question}</p>
                <button 
                  className="question-btn"
                  onClick={() => handleAskAI(item.question)}
                >
                  Ask AI
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="movies-section">
          <div className="movies-section-header">
            <h2 className="section-title">Trending This Week</h2>
          </div>
          
          <div className="movies-carousel">
            {trendingMovies.slice(0, 10).map((movie) => (
              <Link 
                key={movie.id}
                to={`/movies/${movie.id}`}
                className="movie-card-home"
              >
                <div className="movie-poster-home">
                  <img
                    src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'}
                    alt={movie.title}
                  />
                  {movie.imdb_rating && (
                    <div className="movie-rating-home">
                      <Star className="rating-icon" size={14} />
                      <span>{movie.imdb_rating}</span>
                    </div>
                  )}
                </div>
                <h3 className="movie-title-home">{movie.title}</h3>
              </Link>
            ))}
          </div>
        </div>

        <div className="movies-section">
          <div className="movies-section-header">
            <h2 className="section-title">Recently Viewed</h2>
          </div>
          
          <div className="movies-carousel">
            {topMovies.slice(0, 10).map((movie) => (
              <Link 
                key={movie.id}
                to={`/movies/${movie.id}`}
                className="movie-card-home"
              >
                <div className="movie-poster-home">
                  <img
                    src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'}
                    alt={movie.title}
                  />
                  {movie.imdb_rating && (
                    <div className="movie-rating-home">
                      <Star className="rating-icon" size={14} />
                      <span>{movie.imdb_rating}</span>
                    </div>
                  )}
                </div>
                <h3 className="movie-title-home">{movie.title}</h3>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;