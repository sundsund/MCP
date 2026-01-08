import React, { useState } from 'react';

interface TaskFormProps {
  onSubmit: (task: { name: string; processingTime: number }) => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [processingTime, setProcessingTime] = useState(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ name, processingTime });
    setName('');
    setProcessingTime(1);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Task Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Processing Time (s)"
        value={processingTime}
        onChange={(e) => setProcessingTime(Number(e.target.value))}
        min="1"
        required
      />
      <button type="submit">Add Task</button>
    </form>
  );
};

export default TaskForm;
