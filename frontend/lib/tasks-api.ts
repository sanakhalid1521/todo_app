/**
 * Tasks API client for managing user tasks
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

class TasksAPI {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    // Import auth functions to get token
    const { getToken } = await import('./auth');
    const token = getToken();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers,
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async listTasks(): Promise<Task[]> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<Task[]>(`/api/${userId}/tasks`);
  }

  async getTask(taskId: number): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async createTask(data: CreateTaskRequest): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTask(taskId: number, data: UpdateTaskRequest): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTask(taskId: number): Promise<{ success: boolean }> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<{ success: boolean }>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleComplete(taskId: number): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-uuid-placeholder';
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    });
  }
}

export const tasksAPI = new TasksAPI();