import axios from './axios';

export const chatAPI = {
  // Send message
  sendMessage: (message, movieId = null, conversationId = null) =>
    axios.post('/chat/message/', {
      message,
      movie_id: movieId,
      conversation_id: conversationId,
    }),

  // Get conversations
  getConversations: () =>
    axios.get('/chat/conversations/'),

  // Get conversation detail
  getConversation: (id) =>
    axios.get(`/chat/conversation_detail/${id}/`),
};