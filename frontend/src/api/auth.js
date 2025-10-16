import axios from './axios';

export const authAPI = {
  login: (username, password) =>
    axios.post('/auth/login/', { username, password }),

  register: (username, email, password, password2) =>
    axios.post('/auth/register/', { username, email, password, password2 }),

  logout: (refreshToken) =>
    axios.post('/auth/logout/', { refresh_token: refreshToken }),

  getProfile: () =>
    axios.get('/auth/profile/'),

  updateProfile: (data) =>
    axios.put('/auth/profile/update/', data),

  refreshToken: (refreshToken) =>
    axios.post('/auth/token/refresh/', { refresh: refreshToken }),
};