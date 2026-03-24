import type { Task, TaskCreateOrUpdate } from '../models/task';
import { API_BASE_URL } from '../utils/config';

const BASE_URL = `${API_BASE_URL}/api/tasks/`;

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = 'Request failed';
    try {
      const data = await response.json();
      if (typeof data === 'string') {
        message = data;
      } else if (data?.detail) {
        message = String(data.detail);
      } else if (data?.dueDate) {
        message = Array.isArray(data.dueDate) ? data.dueDate.join(', ') : String(data.dueDate);
      }
    } catch {
      // keep fallback message
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const taskService = {
  getTasks(): Promise<Task[]> {
    return fetch(BASE_URL).then(handleResponse<Task[]>);
  },

  getTask(id: number): Promise<Task> {
    return fetch(`${BASE_URL}${id}/`).then(handleResponse<Task>);
  },

  createTask(task: TaskCreateOrUpdate): Promise<Task> {
    return fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    }).then(handleResponse<Task>);
  },

  updateTask(id: number, task: TaskCreateOrUpdate): Promise<Task> {
    return fetch(`${BASE_URL}${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    }).then(handleResponse<Task>);
  },

  deleteTask(id: number): Promise<void> {
    return fetch(`${BASE_URL}${id}/`, { method: 'DELETE' }).then(handleResponse<void>);
  },
};
