import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Plus, Moon, Bell, LogOut, User } from 'lucide-react';
import useAuthStore from '../../store/authStore';

const Header = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/movies?search=${searchQuery}`);
      setSearchQuery('');
    }
  };

  const handleLogout = async () => {
    await logout();
    setShowUserMenu(false);
    navigate('/login');
  };

  return (
    <header className="bg-[var(--color-dark-sidebar)] border-b border-gray-700 p-4 flex items-center justify-between">
      {/* Search Bar */}
      <div className="flex-1 max-w-2xl">
        <form onSubmit={handleSearch} className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search movies, shows, or discussions..."
            className="w-full pl-10 pr-4 py-2 bg-[var(--color-dark-bg)] border border-gray-700 rounded-lg focus:outline-none focus:border-[var(--color-primary)] text-white"
          />
        </form>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-4 ml-4">
        {isAuthenticated ? (
          <>
            <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition flex items-center gap-2">
              <Plus className="w-5 h-5" />
              <span className="hidden md:inline">Add to Desktop</span>
            </button>

            <button className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition">
              <Moon className="w-5 h-5" />
            </button>

            <button className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition">
              <Bell className="w-5 h-5" />
            </button>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="w-10 h-10 bg-[var(--color-primary)] rounded-full flex items-center justify-center font-semibold cursor-pointer hover:bg-[var(--color-primary-dark)] transition"
              >
                {user?.username?.charAt(0).toUpperCase()}
              </button>

              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-[var(--color-dark-card)] border border-gray-700 rounded-lg shadow-xl py-2 z-50">
                  <div className="px-4 py-2 border-b border-gray-700">
                    <p className="font-semibold">{user?.username}</p>
                    <p className="text-sm text-gray-400">{user?.email}</p>
                  </div>
                  <button
                    onClick={() => {
                      navigate('/profile');
                      setShowUserMenu(false);
                    }}
                    className="w-full px-4 py-2 hover:bg-[var(--color-dark-hover)] transition text-left flex items-center gap-2"
                  >
                    <User className="w-4 h-4" />
                    Profile
                  </button>
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-2 hover:bg-[var(--color-dark-hover)] transition text-left flex items-center gap-2 text-red-400"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          </>
        ) : (
          <>
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition"
            >
              Login
            </button>
            <button
              onClick={() => navigate('/register')}
              className="px-4 py-2 bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)] rounded-lg transition font-semibold"
            >
              Sign Up
            </button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;