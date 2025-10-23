import axios from './axios';

export const chatAPI = {
  sendMessage: (message, movieId = null, conversationId = null) =>
    axios.post('/chat/send/', {
      message,
      movie_id: movieId,
      conversation_id: conversationId,
    }),

  getConversations: () =>
    axios.get('/chat/conversations/'),

  getConversation: (id) =>
    axios.get(`/chat/${id}/conversation_detail/`),
};