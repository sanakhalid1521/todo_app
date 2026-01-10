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

    // Start with default headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add any provided headers
    if (options.headers) {
      if (Array.isArray(options.headers)) {
        // Handle headers as array of tuples
        for (const [key, value] of options.headers) {
          headers[key] = value;
        }
      } else if (options.headers instanceof Headers) {
        // Handle Headers instance
        for (const [key, value] of options.headers.entries()) {
          headers[key] = value;
        }
      } else {
        // Handle headers as object
        Object.assign(headers, options.headers);
      }
    }

    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        headers,
        ...options,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  async listTasks(): Promise<Task[]> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<Task[]>(`/api/${encodeURIComponent(userId)}/tasks`);
  }

  async getTask(taskId: number): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<Task>(`/api/${encodeURIComponent(userId)}/tasks/${taskId}`);
  }

  async createTask(data: CreateTaskRequest): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<Task>(`/api/${encodeURIComponent(userId)}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateTask(taskId: number, data: UpdateTaskRequest): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<Task>(`/api/${encodeURIComponent(userId)}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTask(taskId: number): Promise<{ success: boolean }> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<{ success: boolean }>(`/api/${encodeURIComponent(userId)}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleComplete(taskId: number): Promise<Task> {
    // Get user ID from auth system
    const { getUserId } = await import('./auth');
    const userId = getUserId() || 'user-demo';
    return this.request<Task>(`/api/${encodeURIComponent(userId)}/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    });
  }
}

export const tasksAPI = new TasksAPI();