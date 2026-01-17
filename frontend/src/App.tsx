import React, { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import { Task } from './types';

const API_URL = 'http://localhost:3001';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(`${API_URL}/tasks`);
        const data = await response.json();
        setTasks(data);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();

    const interval = setInterval(fetchTasks, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, []);

  const handleAddTask = async (task: { name: string; processingTime: number }) => {
    try {
      await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(task),
      });
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  return (
    <div className="App">
      <h1>Smart Task Queue</h1>
      <TaskForm onSubmit={handleAddTask} />
      <TaskList tasks={tasks} />
    </div>
  );
}

export default App;
