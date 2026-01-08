export interface Task {
  id: number;
  name: string;
  processingTime: number;
  status: 'Pending' | 'Processing' | 'Completed';
}
