import axios from 'axios';
import { User, Room, Message } from '@/types';

/**
 * Axios instance configured with base URL from environment.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Auth endpoints
 */
export const loginUser = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data as { access_token: string; user: User };
};

export const registerUser = async (data: { name: string; email: string; password: string }) => {
  const response = await api.post('/auth/register', data);
  return response.data as { user: User };
};

/**
 * Room endpoints
 */
export const fetchRooms = async (token: string): Promise<Room[]> => {
  const response = await api.get('/rooms', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as Room[];
};

/**
 * Message endpoints
 */
export const fetchMessages = async (roomId: string, page: number = 1, limit: number = 50): Promise<Message[]> => {
  const response = await api.get(`/rooms/${roomId}/messages`, {
    params: { page, limit },
  });
  return response.data as Message[];
};

export const sendMessageApi = async (roomId: string, content: string): Promise<Message> => {
  const response = await api.post(`/rooms/${roomId}/messages`, { content });
  return response.data as Message;
};

export default api;
