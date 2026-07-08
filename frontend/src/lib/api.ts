import { z } from 'zod';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const errorSchema = z.object({
  message: z.string(),
  errors: z.record(z.array(z.string())).optional(),
});

type ApiError = z.infer<typeof errorSchema>;

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let error: ApiError;
    try {
      const data = await response.json();
      error = errorSchema.parse(data);
    } catch {
      error = { message: 'An unknown error occurred' };
    }
    throw new Error(error.message);
  }
  return response.json();
}

interface FetchOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
  params?: Record<string, string | number | boolean>;
}

async function fetchApi<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { body, params, ...init } = options;
  const url = new URL(`${API_BASE_URL}${endpoint}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (init.headers) {
    Object.assign(headers, init.headers);
  }

  const config: RequestInit = {
    ...init,
    headers,
    credentials: 'include',
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(url.toString(), config);
  return handleResponse<T>(response);
}

// Auth endpoints
const authEndpoints = {
  register: '/auth/register',
  login: '/auth/login',
  refresh: '/auth/refresh',
  me: '/auth/me',
  logout: '/auth/logout',
};

const roomEndpoints = {
  list: '/rooms',
  create: '/rooms',
  join: '/rooms/:roomId/join',
  leave: '/rooms/:roomId/leave',
  get: '/rooms/:roomId',
};

const messageEndpoints = {
  list: '/messages',
  search: '/messages/search',
};

const moderationEndpoints = {
  ban: '/moderation/ban',
  kick: '/moderation/kick',
  report: '/moderation/report',
};

// Public API functions
async function registerUser(data: { email: string; name: string; password: string }) {
  return fetchApi<{ user: { id: string; email: string; name: string } }>(authEndpoints.register, {
    method: 'POST',
    body: data,
  });
}

async function loginUser(data: { email: string; password: string }) {
  return fetchApi<{ accessToken: string; refreshToken: string }>(authEndpoints.login, {
    method: 'POST',
    body: data,
  });
}

async function refreshToken() {
  return fetchApi<{ accessToken: string }>(authEndpoints.refresh, {
    method: 'POST',
  });
}

async function getMe() {
  return fetchApi<{ id: string; email: string; name: string; image?: string }>(authEndpoints.me);
}

async function logoutUser() {
  return fetchApi<{ message: string }>(authEndpoints.logout, {
    method: 'POST',
  });
}

async function listRooms(params?: { cursor?: string; limit?: number }) {
  return fetchApi<{ rooms: Array<{ id: string; name: string; slug: string; description: string; createdAt: string; memberCount: number }>; nextCursor?: string }>(roomEndpoints.list, { params });
}

async function createRoom(data: { name: string; slug: string; description?: string }) {
  return fetchApi<{ room: { id: string; name: string; slug: string; description: string; createdAt: string } }>(roomEndpoints.create, {
    method: 'POST',
    body: data,
  });
}

async function joinRoom(roomId: string) {
  return fetchApi<{ message: string }>(roomEndpoints.join.replace(':roomId', roomId), {
    method: 'POST',
  });
}

async function leaveRoom(roomId: string) {
  return fetchApi<{ message: string }>(roomEndpoints.leave.replace(':roomId', roomId), {
    method: 'POST',
  });
}

async function getRoom(roomId: string) {
  return fetchApi<{ room: { id: string; name: string; slug: string; description: string; createdAt: string; isMember: boolean } }>(roomEndpoints.get.replace(':roomId', roomId));
}

async function listMessages(params?: { roomId?: string; cursor?: string; limit?: number }) {
  return fetchApi<{ messages: Array<{ id: string; content: string; createdAt: string; user: { id: string; name: string; image?: string } }>; nextCursor?: string }>(messageEndpoints.list, { params });
}

async function searchMessages(query: string, params?: { roomId?: string; limit?: number }) {
  return fetchApi<{ messages: Array<{ id: string; content: string; createdAt: string; user: { id: string; name: string; image?: string } }> }>(messageEndpoints.search, {
    method: 'GET',
    params: { ...params, q: query },
  });
}

async function banUser(data: { userId: string; roomId: string; reason?: string }) {
  return fetchApi<{ message: string }>(moderationEndpoints.ban, {
    method: 'POST',
    body: data,
  });
}

async function kickUser(data: { userId: string; roomId: string }) {
  return fetchApi<{ message: string }>(moderationEndpoints.kick, {
    method: 'POST',
    body: data,
  });
}

async function reportMessage(data: { messageId: string; reason: string }) {
  return fetchApi<{ message: string }>(moderationEndpoints.report, {
    method: 'POST',
    body: data,
  });
}

export {
  registerUser,
  loginUser,
  refreshToken,
  getMe,
  logoutUser,
  listRooms,
  createRoom,
  joinRoom,
  leaveRoom,
  getRoom,
  listMessages,
  searchMessages,
  banUser,
  kickUser,
  reportMessage,
};
