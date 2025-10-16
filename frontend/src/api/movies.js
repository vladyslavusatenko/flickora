import axios from './axios';

export const moviesAPI = {
  // Get all movies with pagination
  getMovies: (params = {}) =>
    axios.get('/movies/', { params }),

  // Get single movie
  getMovie: (id) =>
    axios.get(`/movies/${id}/`),

  // Get movie sections
  getMovieSections: (id) =>
    axios.get(`/movies/${id}/sections/`),

  // Mark movie as viewed
  markAsViewed: (id) =>
    axios.post(`/movies/${id}/view/`),

  // Get trending movies
  getTrending: () =>
    axios.get('/movies/trending/'),

  // Get recently viewed movies
  getRecentlyViewed: () =>
    axios.get('/movies/recently_viewed/'),

  // Search movies
  searchMovies: (query, params = {}) =>
    axios.get('/movies/', { params: { search: query, ...params } }),

  // Get genres
  getGenres: () =>
    axios.get('/genres/'),
};