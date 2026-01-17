import express from 'express';
import cors from 'cors';

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

interface Task {
  id: number;
  name: string;
  processingTime: number;
  status: 'Pending' | 'Processing' | 'Completed';
}

let tasks: Task[] = [];
let nextTaskId = 1;

app.get('/tasks', (req, res) => {
  res.json(tasks);
});

app.post('/tasks', (req, res) => {
  const { name, processingTime } = req.body;

  if (!name || !processingTime) {
    return res.status(400).json({ error: 'Task name and processing time are required' });
  }

  const newTask: Task = {
    id: nextTaskId++,
    name,
    processingTime,
    status: 'Pending',
  };

  tasks.push(newTask);

  setTimeout(() => {
    newTask.status = 'Processing';
    setTimeout(() => {
      newTask.status = 'Completed';
    }, newTask.processingTime * 1000);
  }, 1000);

  res.status(201).json(newTask);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
