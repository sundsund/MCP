"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const app = (0, express_1.default)();
const port = 3001;
app.use((0, cors_1.default)());
app.use(express_1.default.json());
let tasks = [];
let nextTaskId = 1;
app.get('/tasks', (req, res) => {
    res.json(tasks);
});
app.post('/tasks', (req, res) => {
    const { name, processingTime } = req.body;
    if (!name || !processingTime) {
        return res.status(400).json({ error: 'Task name and processing time are required' });
    }
    const newTask = {
        id: nextTaskId++,
        name,
        processingTime,
        status: 'Pending',
    };
    tasks.push(newTask);
    setTimeout(() => {
        const taskIndex = tasks.findIndex(task => task.id === newTask.id);
        if (taskIndex !== -1) {
            tasks[taskIndex].status = 'Processing';
            setTimeout(() => {
                const completedTaskIndex = tasks.findIndex(task => task.id === newTask.id);
                if (completedTaskIndex !== -1) {
                    tasks[completedTaskIndex].status = 'Completed';
                }
            }, newTask.processingTime * 1000);
        }
    }, 1000);
    res.status(201).json(newTask);
});
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
