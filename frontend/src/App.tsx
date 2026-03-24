import { useEffect, useState } from 'react';
import './index.css';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import type { Task, TaskCreateOrUpdate } from './models/task';
import { taskService } from './services/taskService';

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadTasks(): Promise<void> {
    setLoading(true);
    setError(null);

    try {
      const data = await taskService.getTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadTasks();
  }, []);

  async function handleCreateOrUpdate(taskInput: TaskCreateOrUpdate): Promise<void> {
    setError(null);

    try {
      if (editingTask) {
        const updated = await taskService.updateTask(editingTask.id, taskInput);
        setTasks((current) => current.map((task) => (task.id === updated.id ? updated : task)));
        setEditingTask(null);
      } else {
        const created = await taskService.createTask(taskInput);
        setTasks((current) => [...current, created]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save task');
    }
  }

  async function handleDelete(id: number): Promise<void> {
    setError(null);

    try {
      await taskService.deleteTask(id);
      setTasks((current) => current.filter((task) => task.id !== id));
      setEditingTask((current) => (current?.id === id ? null : current));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Task Manager</h1>
        <p className="subtitle">Manage tasks.</p>
      </header>

      <main className="layout">
        <div className="layout-column">
         <TaskForm
           initialTask={editingTask}
           onSubmit={handleCreateOrUpdate}
           onCancel={() => setEditingTask(null)}
         />

          {error && <div className="alert alert-error">{error}</div>}
        </div>

        <div className="layout-column">
          <TaskList
            tasks={tasks}
            loading={loading}
            onEdit={setEditingTask}
            onDelete={(id) => {
              void handleDelete(id);
            }}
            onRefresh={() => {
              void loadTasks();
            }}
          />
        </div>
      </main>
    </div>
  );
}
