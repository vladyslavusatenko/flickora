import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { moviesAPI } from '../api';
import { Star, Clock, Calendar, ArrowLeft, ChevronDown, Film, Heart, Share2, Send } from 'lucide-react';
import { useState } from 'react';
import LoadingSpinner from '../components/common/loadingSpinner';
import '../styles/pages/MovieDetail.css';

const MovieDetail = () => {
  const { id } = useParams();
  const [expandedSections, setExpandedSections] = useState({});
  const [showFullSynopsis, setShowFullSynopsis] = useState(false);
  const [chatMessage, setChatMessage] = useState('');

  const { data: movieData, isLoading: movieLoading } = useQuery({
    queryKey: ['movie', id],
    queryFn: () => moviesAPI.getMovie(id)
  });

  const { data: sectionsData } = useQuery({
    queryKey: ['movie-sections', id],
    queryFn: () => moviesAPI.getMovieSections(id),
    enabled: !!id
  });

  const { data: castData } = useQuery({
    queryKey: ['movie-cast', id],
    queryFn: () => moviesAPI.getMovieCast(id),
    enabled: !!id
  });

  const { data: similarData } = useQuery({
    queryKey: ['movie-similar', id],
    queryFn: () => moviesAPI.getSimilarMovies(id),
    enabled: !!id
  });

  const movie = movieData?.data;
  const sections = sectionsData?.data || [];
  const cast = castData?.data?.cast || [];
  const similarMovies = similarData?.data?.similar || [];

  const toggleSection = (sectionId) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (chatMessage.trim()) {
      console.log('Sending message:', chatMessage);
      setChatMessage('');
    }
  };

  const quickQuestions = [
    "What's the meaning behind the spinning top?",
    "Explain the dream levels in this movie",
    "What are some hidden details I might have missed?"
  ];

  if (movieLoading) {
    return <LoadingSpinner size="lg" />;
  }

  if (!movie) {
    return (
      <div className="movie-detail-error">
        <h1>Movie not found</h1>
        <Link to="/" className="btn btn-primary">
          <ArrowLeft size={20} />
          Back to Home
        </Link>
      </div>
    );
  }

  return (
    <div className="movie-detail">
      <div className="movie-detail-container">
        <div className="movie-detail-main">
          <Link to="/" className="back-button">
            <ArrowLeft size={20} />
            Back
          </Link>

          <div className="movie-detail-content-wrapper">
            <div className="movie-detail-poster">
              <img 
                src={movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Poster'} 
                alt={movie.title}
              />
            </div>

            <div className="movie-detail-info">
              <h1 className="movie-detail-title">{movie.title}</h1>
              
              <div className="movie-detail-meta">
                <span className="meta-year">{movie.year}</span>
                <span className="meta-separator">•</span>
                {movie.runtime && (
                  <>
                    <span className="meta-runtime">{movie.runtime} min</span>
                    <span className="meta-separator">•</span>
                  </>
                )}
                {movie.director && (
                  <span className="meta-director">Directed by {movie.director}</span>
                )}
              </div>

              {movie.imdb_rating && (
                <div className="movie-detail-rating">
                  {[...Array(5)].map((_, i) => (
                    <Star 
                      key={i} 
                      className={`rating-star ${i < Math.floor(movie.imdb_rating / 2) ? 'filled' : ''}`}
                      size={24}
                    />
                  ))}
                  <span className="rating-value">{movie.imdb_rating}/10</span>
                </div>
              )}

              {movie.genres && movie.genres.length > 0 && (
                <div className="movie-detail-genres">
                  {movie.genres.map(genre => (
                    <span key={genre.id} className="genre-tag">
                      {genre.name}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {movie.plot_summary && (
            <div className="synopsis-section">
              <h2 className="section-title">Synopsis</h2>
              <div className="synopsis-content">
                <p className={showFullSynopsis ? 'full' : 'truncated'}>
                  {movie.plot_summary}
                </p>
                {movie.plot_summary.length > 300 && (
                  <button 
                    className="read-more-btn"
                    onClick={() => setShowFullSynopsis(!showFullSynopsis)}
                  >
                    <ChevronDown 
                      className={`chevron ${showFullSynopsis ? 'expanded' : ''}`}
                      size={16}
                    />
                    {showFullSynopsis ? 'Read Less' : 'Read More'}
                  </button>
                )}
              </div>
            </div>
          )}

          {cast.length > 0 && (
            <div className="cast-section">
              <h2 className="section-title">Cast</h2>
              <div className="cast-grid">
                {cast.map((actor, index) => (
                  <div key={index} className="cast-member">
                    <div className="cast-avatar">
                      <img 
                        src={actor.profile_path || 'https://via.placeholder.com/100?text=No+Photo'} 
                        alt={actor.name} 
                      />
                    </div>
                    <div className="cast-info">
                      <h3 className="cast-name">{actor.name}</h3>
                      <p className="cast-role">{actor.character}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {sections.length > 0 && (
            <div className="movie-sections">
              <div className="sections-header">
                <Film size={24} className="sections-icon" />
                <h2 className="sections-title">AI-Generated Analysis</h2>
              </div>
              
              <div className="sections-list">
                {sections.map((section) => (
                  <div key={section.id} className="section-card">
                    <button 
                      className="section-header"
                      onClick={() => toggleSection(section.id)}
                    >
                      <h3 className="section-title-text">{section.section_type_display}</h3>
                      <div className="section-meta">
                        <span className="section-word-count">{section.word_count} words</span>
                        <ChevronDown 
                          className={`section-chevron ${expandedSections[section.id] ? 'expanded' : ''}`}
                          size={20}
                        />
                      </div>
                    </button>
                    
                    {expandedSections[section.id] && (
                      <div className="section-content">
                        <p>{section.content}</p>
                        {section.key_topics && section.key_topics.length > 0 && (
                          <div className="section-topics">
                            <span className="topics-label">Key Topics:</span>
                            <div className="topics-list">
                              {section.key_topics.map((topic, index) => (
                                <span key={index} className="topic-tag">{topic}</span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {similarMovies.length > 0 && (
            <div className="similar-movies-section">
              <h2 className="section-title">Similar Movies</h2>
              <div className="similar-movies-grid">
                {similarMovies.map((similar) => (
                  <Link 
                    key={similar.id}
                    to={`/movies/${similar.id}`}
                    className="similar-movie-card"
                  >
                    <img 
                      src={similar.poster_url || 'https://via.placeholder.com/200x300?text=No+Poster'} 
                      alt={similar.title} 
                    />
                    <div className="similar-movie-info">
                      <h3 className="similar-movie-title">{similar.title}</h3>
                      <p className="similar-movie-year">{similar.year}</p>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="movie-detail-sidebar">
          <div className="chat-widget">
            <h3 className="chat-title">Chat with AI</h3>
            
            <div className="chat-messages">
              <div className="chat-message ai-message">
                <p>Hi! I'm here to help you explore this movie. Ask me anything about {movie.title}!</p>
              </div>
            </div>

            <form onSubmit={handleSendMessage} className="chat-input-form">
              <input 
                type="text" 
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder="Ask about this movie..."
                className="chat-input"
              />
              <button type="submit" className="chat-send-btn" disabled={!chatMessage.trim()}>
                <Send size={18} />
              </button>
            </form>

            <div className="quick-questions">
              <h4 className="quick-questions-title">Quick Questions</h4>
              {quickQuestions.map((question, index) => (
                <button 
                  key={index}
                  className="quick-question-btn"
                  onClick={() => setChatMessage(question)}
                >
                  {question}
                </button>
              ))}
            </div>

            <div className="actions-section">
              <h4 className="actions-title">Actions</h4>
              <button className="action-btn">
                <Heart size={18} />
                Add to Favorites
              </button>
              <button className="action-btn">
                <Share2 size={18} />
                Share Movie
              </button>
              
              <div className="rate-movie">
                <span className="rate-label">Rate this movie</span>
                <div className="rating-stars">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="rate-star" size={20} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;