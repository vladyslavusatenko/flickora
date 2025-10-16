import { useState, useEffect } from 'react'
import { moviesAPI } from './api'
import useAuthStore from './store/authStore'

function App() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const { user, isAuthenticated } = useAuthStore()

  useEffect(() => {
    fetchMovies()
  }, [])

  const fetchMovies = async () => {
    try {
      const response = await moviesAPI.getTrending()
      setMovies(response.data.slice(0, 5))
      setLoading(false)
    } catch (error) {
      console.error('Error fetching movies:', error)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[var(--color-dark-bg)] text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-[var(--color-primary)]">
          🎬 flickora - React Frontend Test
        </h1>

        <div className="bg-[var(--color-dark-card)] rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Auth Status</h2>
          <p className="text-lg">
            {isAuthenticated ? (
              <span className="text-green-400">✓ Logged in as: {user?.username}</span>
            ) : (
              <span className="text-yellow-400">⚠ Not logged in</span>
            )}
          </p>
        </div>

        <div className="bg-[var(--color-dark-card)] rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">API Test - Trending Movies</h2>
          
          {loading ? (
            <p className="text-gray-400">Loading movies...</p>
          ) : movies.length > 0 ? (
            <div className="space-y-4">
              {movies.map((movie) => (
                <div 
                  key={movie.id}
                  className="bg-[var(--color-dark-sidebar)] p-4 rounded-lg hover:bg-[var(--color-dark-hover)] transition"
                >
                  <h3 className="text-xl font-semibold">{movie.title}</h3>
                  <p className="text-gray-400">
                    {movie.year} • {movie.director} • ⭐ {movie.imdb_rating}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-red-400">No movies found. Check Django backend!</p>
          )}
        </div>

        <div className="mt-8 text-center text-gray-400">
          <p>✓ React + Vite running</p>
          <p>✓ Tailwind v4 configured</p>
          <p>✓ API connection: {movies.length > 0 ? '✓ Working' : '✗ Check backend'}</p>
        </div>
      </div>
    </div>
  )
}

export default App