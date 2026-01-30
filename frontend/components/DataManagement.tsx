'use client';

import { useState, useRef } from 'react';
import { Download, Upload, FileText, AlertCircle } from 'lucide-react';
import { Task } from '@/lib/tasks-api';

interface DataManagementProps {
  tasks: Task[];
  onImport: (tasks: Task[]) => void;
}

export default function DataManagement({ tasks, onImport }: DataManagementProps) {
  const [isImporting, setIsImporting] = useState(false);
  const [importError, setImportError] = useState<string | null>(null);
  const [importPreview, setImportPreview] = useState<Task[] | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Export tasks to CSV
  const exportToCSV = () => {
    if (!tasks || tasks.length === 0) {
      alert('No tasks to export');
      return;
    }

    // Create CSV content
    const headers = ['id', 'user_id', 'title', 'description', 'completed', 'category', 'priority', 'due_date', 'created_at', 'updated_at'];
    const csvContent = [
      headers.join(','),
      ...tasks.map(task => [
        task.id,
        task.user_id,
        `"${task.title.replace(/"/g, '""')}"`,
        `"${(task.description || '').replace(/"/g, '""')}"`,
        task.completed,
        task.category,
        task.priority,
        task.due_date ? new Date(task.due_date).toISOString() : '',
        new Date(task.created_at).toISOString(),
        new Date(task.updated_at).toISOString()
      ].join(','))
    ].join('\n');

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `tasks-export-${new Date().toISOString().slice(0, 10)}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Export tasks to JSON
  const exportToJSON = () => {
    if (!tasks || tasks.length === 0) {
      alert('No tasks to export');
      return;
    }

    const jsonData = JSON.stringify(tasks, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `tasks-export-${new Date().toISOString().slice(0, 10)}.json`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Handle file selection
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImportError(null);
    setImportPreview(null);
    setShowPreview(false);

    // Check file type
    if (!file.name.endsWith('.csv') && !file.name.endsWith('.json')) {
      setImportError('Please select a CSV or JSON file');
      return;
    }

    // Process the file based on type
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const content = event.target?.result as string;
        if (!content) {
          setImportError('Could not read file content');
          return;
        }

        if (file.name.endsWith('.csv')) {
          processCSV(content);
        } else if (file.name.endsWith('.json')) {
          processJSON(content);
        }
      } catch (error) {
        setImportError(`Error processing file: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    };

    reader.onerror = () => {
      setImportError('Error reading file');
    };

    reader.readAsText(file);
  };

  // Process CSV content
  const processCSV = (content: string) => {
    const lines = content.split('\n');
    if (lines.length < 2) {
      setImportError('CSV file is empty or has no data rows');
      return;
    }

    // Parse headers
    const headers = lines[0].split(',').map(h => h.trim());
    const requiredHeaders = ['title'];

    // Check for required headers
    for (const reqHeader of requiredHeaders) {
      if (!headers.includes(reqHeader)) {
        setImportError(`Missing required column: ${reqHeader}`);
        return;
      }
    }

    // Process data rows
    const importedTasks: Task[] = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Split line considering quotes
      const row = parseCSVRow(line);

      if (row.length !== headers.length) {
        setImportError(`Row ${i} has incorrect number of columns`);
        return;
      }

      const taskData: any = {};
      for (let j = 0; j < headers.length; j++) {
        taskData[headers[j]] = row[j];
      }

      // Validate required fields
      if (!taskData.title) {
        setImportError(`Row ${i} is missing required title field`);
        return;
      }

      // Validate enums
      if (taskData.category && !['work', 'personal', 'shopping', 'health', 'other'].includes(taskData.category)) {
        setImportError(`Row ${i} has invalid category: ${taskData.category}`);
        return;
      }

      if (taskData.priority && !['low', 'medium', 'high', 'urgent'].includes(taskData.priority)) {
        setImportError(`Row ${i} has invalid priority: ${taskData.priority}`);
        return;
      }

      // Create task object
      const newTask: Task = {
        id: importedTasks.length + 1, // Temporary ID, will be updated after import
        user_id: taskData.user_id || 'user-demo',
        title: taskData.title,
        description: taskData.description || '',
        completed: taskData.completed === 'true' || taskData.completed === 'TRUE' || taskData.completed === '1',
        created_at: taskData.created_at || new Date().toISOString(),
        updated_at: taskData.updated_at || new Date().toISOString(),
        category: taskData.category || 'other',
        priority: taskData.priority || 'medium',
        due_date: taskData.due_date || undefined
      };

      importedTasks.push(newTask);
    }

    setImportPreview(importedTasks);
    setShowPreview(true);
  };

  // Helper to parse CSV row considering quotes
  const parseCSVRow = (row: string): string[] => {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < row.length; i++) {
      const char = row[i];

      if (char === '"') {
        if (inQuotes && i + 1 < row.length && row[i + 1] === '"') {
          // Escaped quote
          current += '"';
          i++; // Skip next quote
        } else {
          // Toggle quote state
          inQuotes = !inQuotes;
        }
      } else if (char === ',' && !inQuotes) {
        result.push(current);
        current = '';
      } else {
        current += char;
      }
    }

    result.push(current);
    return result;
  };

  // Process JSON content
  const processJSON = (content: string) => {
    try {
      const parsed = JSON.parse(content);

      if (!Array.isArray(parsed)) {
        setImportError('JSON file must contain an array of tasks');
        return;
      }

      const importedTasks: Task[] = [];
      for (let i = 0; i < parsed.length; i++) {
        const taskData = parsed[i];

        // Validate required fields
        if (!taskData.title) {
          setImportError(`Task at index ${i} is missing required title field`);
          return;
        }

        // Validate enums
        if (taskData.category && !['work', 'personal', 'shopping', 'health', 'other'].includes(taskData.category)) {
          setImportError(`Task at index ${i} has invalid category: ${taskData.category}`);
          return;
        }

        if (taskData.priority && !['low', 'medium', 'high', 'urgent'].includes(taskData.priority)) {
          setImportError(`Task at index ${i} has invalid priority: ${taskData.priority}`);
          return;
        }

        // Create task object
        const newTask: Task = {
          id: importedTasks.length + 1, // Temporary ID, will be updated after import
          user_id: taskData.user_id || 'user-demo',
          title: taskData.title,
          description: taskData.description || '',
          completed: Boolean(taskData.completed),
          created_at: taskData.created_at || new Date().toISOString(),
          updated_at: taskData.updated_at || new Date().toISOString(),
          category: taskData.category || 'other',
          priority: taskData.priority || 'medium',
          due_date: taskData.due_date || undefined
        };

        importedTasks.push(newTask);
      }

      setImportPreview(importedTasks);
      setShowPreview(true);
    } catch (error) {
      setImportError(`Invalid JSON format: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  // Confirm import
  const confirmImport = () => {
    if (!importPreview) return;

    // Add new tasks to existing tasks
    onImport(importPreview);

    // Reset state
    setImportPreview(null);
    setShowPreview(false);
    setIsImporting(false);

    // Clear file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Cancel import
  const cancelImport = () => {
    setImportPreview(null);
    setShowPreview(false);
    setIsImporting(false);
    setImportError(null);

    // Clear file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Export Section */}
        <div className="flex-1 glass-panel p-6 rounded-2xl border-white/5">
          <h3 className="text-lg font-bold text-white mb-4">Export Tasks</h3>
          <p className="text-gray-400 text-sm mb-4">Download your tasks in CSV or JSON format</p>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={exportToCSV}
              className="flex items-center gap-2 px-4 py-2 bg-green-600/20 text-green-400 hover:bg-green-600/30 rounded-lg transition-all"
            >
              <Download size={16} />
              Export CSV
            </button>

            <button
              onClick={exportToJSON}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600/20 text-blue-400 hover:bg-blue-600/30 rounded-lg transition-all"
            >
              <Download size={16} />
              Export JSON
            </button>
          </div>
        </div>

        {/* Import Section */}
        <div className="flex-1 glass-panel p-6 rounded-2xl border-white/5">
          <h3 className="text-lg font-bold text-white mb-4">Import Tasks</h3>
          <p className="text-gray-400 text-sm mb-4">Upload a CSV or JSON file to import tasks</p>

          <div className="space-y-3">
            <input
              type="file"
              ref={fileInputRef}
              accept=".csv,.json"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />

            <label
              htmlFor="file-upload"
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600/30 rounded-lg cursor-pointer transition-all"
            >
              <Upload size={16} />
              Choose File
            </label>

            {importError && (
              <div className="flex items-start gap-2 text-red-400 text-sm mt-2">
                <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>{importError}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Import Preview Modal */}
      {showPreview && importPreview && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
            <div className="p-6 border-b border-gray-700">
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-bold text-white">Import Preview</h3>
                <button
                  onClick={cancelImport}
                  className="text-gray-400 hover:text-white"
                >
                  ✕
                </button>
              </div>
              <p className="text-gray-400 mt-1">Review the tasks to be imported</p>
            </div>

            <div className="overflow-y-auto max-h-[60vh]">
              <table className="w-full">
                <thead className="sticky top-0 bg-gray-900 z-10">
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Title</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Category</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Priority</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Due Date</th>
                    <th className="text-left py-3 px-4 text-gray-400 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {importPreview.map((task, index) => (
                    <tr key={index} className="border-b border-gray-800 last:border-b-0 hover:bg-gray-800/50">
                      <td className="py-3 px-4 text-white">{task.title}</td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs ${
                          task.category === 'work' ? 'bg-blue-500/20 text-blue-400' :
                          task.category === 'personal' ? 'bg-purple-500/20 text-purple-400' :
                          task.category === 'shopping' ? 'bg-pink-500/20 text-pink-400' :
                          task.category === 'health' ? 'bg-green-500/20 text-green-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {task.category}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs ${
                          task.priority === 'low' ? 'bg-green-500/20 text-green-400' :
                          task.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                          task.priority === 'high' ? 'bg-orange-500/20 text-orange-400' :
                          'bg-red-500/20 text-red-400'
                        }`}>
                          {task.priority}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-300">
                        {task.due_date ? new Date(task.due_date).toLocaleDateString() : '-'}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs ${
                          task.completed ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'
                        }`}>
                          {task.completed ? 'Done' : 'Pending'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-6 border-t border-gray-700 flex justify-end gap-3">
              <button
                onClick={cancelImport}
                className="px-4 py-2 bg-gray-700 text-gray-300 hover:bg-gray-600 rounded-lg transition-all"
              >
                Cancel
              </button>
              <button
                onClick={confirmImport}
                className="px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg transition-all"
              >
                Import {importPreview.length} Tasks
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}