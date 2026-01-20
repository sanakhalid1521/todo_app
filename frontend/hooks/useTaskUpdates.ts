import { useEffect, useState } from 'react';

// Global event emitter for task updates
class TaskEventEmitter {
  private listeners: Array<(event: string) => void> = [];

  subscribe(listener: (event: string) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  emit(event: string) {
    this.listeners.forEach(listener => listener(event));
  }
}

export const taskEventEmitter = new TaskEventEmitter();

// Custom hook to listen for task updates
export const useTaskUpdates = () => {
  const [updateTrigger, setUpdateTrigger] = useState(0);

  useEffect(() => {
    const unsubscribe = taskEventEmitter.subscribe(() => {
      setUpdateTrigger(prev => prev + 1);
    });

    return unsubscribe;
  }, []);

  return updateTrigger;
};

// Function to trigger task updates
export const triggerTaskUpdate = () => {
  taskEventEmitter.emit('task_updated');
};