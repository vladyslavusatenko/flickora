import { useQuery } from '@tanstack/react-query';
import { moviesAPI } from '../api';
import { Film, TrendingUp, Star, Play, Plus, ChevronRight } from 'lucide-react';
import LoadingSpinner from '../components/common/loadingSpinner';
import { Link } from 'react-router-dom';
import '../styles/pages/Home.css';

const Home = () => {
  const { data: trendingData, isLoading: trendingLoading } = useQuery({
    queryKey: ['trending'],
    queryFn: moviesAPI.getTrending
  });

  const { data: moviesData, isLoading: moviesLoading } = useQuery({
    queryKey: ['movies', { limit: 12 }],
    queryFn: () => moviesAPI.getMovies({ limit: 12, ordering: '-imdb_rating' })
  });

  const { data: genresData } = useQuery({
    queryKey: ['genres'],
    queryFn: moviesAPI.getGenres
  });

  const trendingMovies = trendingData?.data?.results || trendingData?.data || [];
  const topMovies = moviesData?.data?.results || moviesData?.data || [];
  const genres = genresData?.data?.results || genresData?.data || [];
  const featuredMovie = trendingMovies[0];

  if (trendingLoading || moviesLoading) {
    return <LoadingSpinner size="lg" />;
  }

  return (
    <div className="home">
      {featuredMovie && (
        <div 
          className="hero"
          style={{ 
            backgroundImage: `linear-gradient(to bottom, rgba(10, 14, 39, 0.3), rgba(10, 14, 39, 0.95)), url(${featuredMovie.backdrop_url || featuredMovie.poster_url})` 
          }}
        >
          <div className="hero-overlay">
            <div className="hero-content">
              <div className="hero-inner">
                <div className="hero-badge">
                  <Film className="hero-badge-icon" size={24} />
                  <span className="hero-badge-text">Featured Movie</span>
                </div>
                
                <h1 className="hero-title">{featuredMovie.title}</h1>
                
                <div className="hero-meta">
                  {featuredMovie.imdb_rating && (
                    <div className="hero-rating">
                      <Star className="hero-rating-icon" size={20} />
                      <span className="hero-rating-value">{featuredMovie.imdb_rating}</span>
                    </div>
                  )}
                  <span>{featuredMovie.year}</span>
                  {featuredMovie.runtime && <span>{featuredMovie.runtime} min</span>}
                </div>
                
                <p className="hero-description">{featuredMovie.plot_summary}</p>
                
                <div className="hero-actions">
                  <Link 
                    to={`/movies/${featuredMovie.id}`}
                    className="btn btn-primary"
                  >
                    <Play size={20} />
                    View Details
                  </Link>
                  <button className="btn btn-secondary">
                    <Plus size={20} />
                    My List
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="section">
        <div className="section-header">
          <div className="section-title-wrapper">
            <TrendingUp className="section-icon" size={24} />
            <h2 className="section-title">Trending Now</h2>
          </div>
          <Link to="/trending" className="section-link">
            View All
            <ChevronRight size={20} />
          </Link>
        </div>

        <div className="movies-grid">
          {trendingMovies.slice(1, 7).map((movie) => (
            <Link 
              key={movie.id}
              to={`/movies/${movie.id}`}
              className="movie-card"
            >
              <div className="movie-poster">
                <img
                  src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'}
                  alt={movie.title}
                />
                {movie.imdb_rating && (
                  <div className="movie-rating">
                    <Star className="movie-rating-icon" />
                    <span className="movie-rating-value">{movie.imdb_rating}</span>
                  </div>
                )}
              </div>
              <h3 className="movie-title">{movie.title}</h3>
              <p className="movie-year">{movie.year}</p>
            </Link>
          ))}
        </div>

        <div className="section-header">
          <h2 className="section-title">Top Rated Movies</h2>
          <Link to="/movies" className="section-link">
            View All
            <ChevronRight size={20} />
          </Link>
        </div>

        <div className="movies-grid">
          {topMovies.slice(0, 12).map((movie) => (
            <Link 
              key={movie.id}
              to={`/movies/${movie.id}`}
              className="movie-card"
            >
              <div className="movie-poster">
                <img
                  src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'}
                  alt={movie.title}
                />
                {movie.imdb_rating && (
                  <div className="movie-rating">
                    <Star className="movie-rating-icon" />
                    <span className="movie-rating-value">{movie.imdb_rating}</span>
                  </div>
                )}
              </div>
              <h3 className="movie-title">{movie.title}</h3>
              <p className="movie-year">{movie.year}</p>
            </Link>
          ))}
        </div>

        {genres.length > 0 && (
          <>
            <h2 className="section-title">Browse by Genre</h2>
            <div className="genres-grid">
              {genres.slice(0, 10).map((genre) => (
                <Link
                  key={genre.id}
                  to={`/movies?genre=${genre.tmdb_id}`}
                  className="genre-card"
                >
                  <h3 className="genre-name">{genre.name}</h3>
                  {genre.movie_count && (
                    <p className="genre-count">{genre.movie_count} movies</p>
                  )}
                </Link>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Home;