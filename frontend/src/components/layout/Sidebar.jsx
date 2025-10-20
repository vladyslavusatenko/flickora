import { Link, useLocation } from 'react-router-dom';
import { 
  Home, Film, TrendingUp, Heart, Clock, 
  MessageCircle, Settings, ChevronRight, Folder 
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { moviesAPI } from '../../api';
import '../../styles/components/Sidebar.css';

const Sidebar = () => {
  const location = useLocation();
  const [genres, setGenres] = useState([]);
  const [showGenres, setShowGenres] = useState(false);

  useEffect(() => {
    fetchGenres();
  }, []);

  const fetchGenres = async () => {
    try {
      const response = await moviesAPI.getGenres();
      const genresList = Array.isArray(response.data) 
        ? response.data 
        : response.data.results || [];
      setGenres(genresList.slice(0, 10));
    } catch (error) {
      console.error('Error fetching genres:', error);
      setGenres([]);
    }
  };

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/movies', icon: Film, label: 'Browse Movies' },
    { path: '/trending', icon: TrendingUp, label: 'Trending' },
    { path: '/favorites', icon: Heart, label: 'Favorites' },
    { path: '/recent', icon: Clock, label: 'Recent Chats' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <Film size={24} />
        </div>
        <span className="sidebar-title">flickora</span>
      </div>

      <nav className="sidebar-nav scrollbar-hide">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${isActive(item.path) ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          );
        })}

        <div className="nav-divider"></div>

        <button
          onClick={() => setShowGenres(!showGenres)}
          className="nav-link"
        >
          <Folder size={20} />
          <span>Genres</span>
          <ChevronRight 
            size={16} 
            className={`chevron ${showGenres ? 'open' : ''}`}
          />
        </button>

        {showGenres && (
          <div className="nav-submenu">
            {genres.map((genre) => (
              <Link
                key={genre.id}
                to={`/movies?genre=${genre.tmdb_id}`}
                className="nav-submenu-link"
              >
                {genre.name}
              </Link>
            ))}
          </div>
        )}

        <div className="nav-divider"></div>

        <Link
          to="/chat"
          className={`nav-link ${isActive('/chat') ? 'active' : ''}`}
        >
          <MessageCircle size={20} />
          <span>Global Chat</span>
        </Link>

        <Link
          to="/settings"
          className={`nav-link ${isActive('/settings') ? 'active' : ''}`}
        >
          <Settings size={20} />
          <span>Settings</span>
        </Link>
      </nav>
    </aside>
  );
};

export default Sidebar;