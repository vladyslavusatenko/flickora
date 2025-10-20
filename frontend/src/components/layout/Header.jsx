import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Moon, Bell, LogOut, User } from 'lucide-react';
import useAuthStore from '../../store/authStore';
import '../../styles/components/Header.css';

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
    <header className="header">
      <div className="search-bar">
        <form onSubmit={handleSearch}>
          <Search className="search-icon" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search movies, shows, or discussions..."
            className="search-input"
          />
        </form>
      </div>

      <div className="header-actions">
        {isAuthenticated ? (
          <>
            <button className="header-btn">
              <Moon size={20} />
            </button>

            <button className="header-btn">
              <Bell size={20} />
            </button>

            <div className="user-menu">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="user-avatar"
              >
                {user?.username?.charAt(0).toUpperCase()}
              </button>

              {showUserMenu && (
                <div className="user-dropdown">
                  <div className="user-dropdown-header">
                    <p className="user-dropdown-name">{user?.username}</p>
                    <p className="user-dropdown-email">{user?.email}</p>
                  </div>
                  <button
                    onClick={() => {
                      navigate('/profile');
                      setShowUserMenu(false);
                    }}
                    className="user-dropdown-item"
                  >
                    <User size={16} />
                    Profile
                  </button>
                  <button
                    onClick={handleLogout}
                    className="user-dropdown-item logout"
                  >
                    <LogOut size={16} />
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
              className="header-btn"
            >
              Login
            </button>
            <button
              onClick={() => navigate('/register')}
              className="btn btn-primary"
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