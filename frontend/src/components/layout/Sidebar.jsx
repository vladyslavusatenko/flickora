import { Link, useLocation } from 'react-router-dom';
import { 
  Home, Film, TrendingUp, Heart, Clock, 
  MessageCircle, Settings, ChevronRight, Folder 
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { moviesAPI } from '../../api';

const Sidebar = () => {
  const location = useLocation();
  const [genres, setGenres] = useState([]);
  const [showGenres, setShowGenres] = useState(false);

  useEffect(() => {
    fetchGenres();
  }, []);

  const fetchGenres = async () => {
    try {
      const fetchGenres = async () => {
        try {
            const response = await moviesAPI.getGenres();
            // Check if data is array or paginated object
            const genresList = Array.isArray(response.data) 
            ? response.data 
            : response.data.results || [];
            setGenres(genresList.slice(0, 10));
        } catch (error) {
            console.error('Error fetching genres:', error);
            setGenres([]); // Set empty array on error
        }
        };
    } catch (error) {
      console.error('Error fetching genres:', error);
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
    <aside className="w-64 bg-[var(--color-dark-sidebar)] border-r border-gray-700 flex flex-col">
      {/* Logo */}
      <div className="p-4 border-b border-gray-700 flex items-center gap-3">
        <div className="w-8 h-8 bg-[var(--color-primary)] rounded flex items-center justify-center">
          <Film className="w-5 h-5" />
        </div>
        <span className="text-xl font-bold">flickora</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto scrollbar-hide p-4">
        <div className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                  isActive(item.path)
                    ? 'bg-[var(--color-primary)] text-white'
                    : 'text-gray-400 hover:bg-[var(--color-dark-hover)] hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Divider */}
        <div className="h-px bg-gray-700 my-4"></div>

        {/* Genres Section */}
        <div className="mb-2">
          <button
            onClick={() => setShowGenres(!showGenres)}
            className="flex items-center justify-between w-full px-4 py-3 rounded-lg hover:bg-[var(--color-dark-hover)] transition text-gray-400 hover:text-white"
          >
            <div className="flex items-center gap-3">
              <Folder className="w-5 h-5" />
              <span>Genres</span>
            </div>
            <ChevronRight
              className={`w-4 h-4 transition-transform ${
                showGenres ? 'rotate-90' : ''
              }`}
            />
          </button>

          {showGenres && (
            <div className="pl-8 mt-2 space-y-1">
              {genres.map((genre) => (
                <Link
                  key={genre.id}
                  to={`/movies?genre=${genre.tmdb_id}`}
                  className="block px-4 py-2 rounded-lg hover:bg-[var(--color-dark-hover)] transition text-sm text-gray-400 hover:text-white"
                >
                  {genre.name}
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Divider */}
        <div className="h-px bg-gray-700 my-4"></div>

        {/* Global Chat */}
        <Link
          to="/chat"
          className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
            isActive('/chat')
              ? 'bg-[var(--color-primary)] text-white'
              : 'text-gray-400 hover:bg-[var(--color-dark-hover)] hover:text-white'
          }`}
        >
          <MessageCircle className="w-5 h-5" />
          <span>Global Chat</span>
        </Link>

        <Link
          to="/settings"
          className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
            isActive('/settings')
              ? 'bg-[var(--color-primary)] text-white'
              : 'text-gray-400 hover:bg-[var(--color-dark-hover)] hover:text-white'
          }`}
        >
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </Link>
      </nav>
    </aside>
  );
};

export default Sidebar;