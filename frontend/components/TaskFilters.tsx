'use client';

import { useState, useEffect } from 'react';
import { Filter, X, ChevronDown } from 'lucide-react';
import { Task } from '@/lib/tasks-api';

interface TaskFiltersProps {
  onFilterChange: (filters: {
    status: string;
    category: string;
    priority: string;
    dueDate: string;
  }) => void;
  tasks: Task[];
}

export default function TaskFilters({ onFilterChange, tasks }: TaskFiltersProps) {
  const [showFilters, setShowFilters] = useState(false);
  const [status, setStatus] = useState('all');
  const [category, setCategory] = useState('all');
  const [priority, setPriority] = useState('all');
  const [dueDate, setDueDate] = useState('all');

  // Calculate filter counts
  const statusCounts = {
    all: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    pending: tasks.filter(t => !t.completed).length
  };

  const categoryCounts = {
    all: tasks.length,
    work: tasks.filter(t => t.category === 'work').length,
    personal: tasks.filter(t => t.category === 'personal').length,
    shopping: tasks.filter(t => t.category === 'shopping').length,
    health: tasks.filter(t => t.category === 'health').length,
    other: tasks.filter(t => t.category === 'other').length
  };

  const priorityCounts = {
    all: tasks.length,
    low: tasks.filter(t => t.priority === 'low').length,
    medium: tasks.filter(t => t.priority === 'medium').length,
    high: tasks.filter(t => t.priority === 'high').length,
    urgent: tasks.filter(t => t.priority === 'urgent').length
  };

  const dueDateCounts = {
    all: tasks.length,
    overdue: tasks.filter(t => t.due_date && new Date(t.due_date) < new Date() && !t.completed).length,
    today: tasks.filter(t => {
      if (!t.due_date) return false;
      const due = new Date(t.due_date);
      const today = new Date();
      return due.toDateString() === today.toDateString() && !t.completed;
    }).length,
    week: tasks.filter(t => {
      if (!t.due_date) return false;
      const due = new Date(t.due_date);
      const today = new Date();
      const weekEnd = new Date(today);
      weekEnd.setDate(today.getDate() + 7);
      return due >= today && due <= weekEnd && !t.completed;
    }).length
  };

  // Notify parent when filters change
  useEffect(() => {
    onFilterChange({ status, category, priority, dueDate });
  }, [status, category, priority, dueDate, onFilterChange]);

  const clearFilters = () => {
    setStatus('all');
    setCategory('all');
    setPriority('all');
    setDueDate('all');
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 mb-6">
      <div className="flex-1">
        <div className="flex flex-wrap gap-2">
          {/* Status Filter */}
          <div className="relative">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                showFilters
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white/5 text-gray-300 hover:bg-white/10'
              }`}
            >
              <Filter size={16} />
              Filters
              <ChevronDown size={16} className={`transition-transform ${showFilters ? 'rotate-180' : ''}`} />
            </button>

            {showFilters && (
              <div className="absolute z-10 mt-2 w-80 bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-4">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-bold text-white">Filters</h3>
                  <button
                    onClick={clearFilters}
                    className="text-sm text-gray-400 hover:text-white flex items-center gap-1"
                  >
                    <X size={14} /> Clear
                  </button>
                </div>

                <div className="space-y-4">
                  {/* Status Filter */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Status</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { value: 'all', label: 'All', count: statusCounts.all },
                        { value: 'pending', label: 'Pending', count: statusCounts.pending },
                        { value: 'completed', label: 'Completed', count: statusCounts.completed }
                      ].map(filter => (
                        <button
                          key={filter.value}
                          onClick={() => setStatus(filter.value)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                            status === filter.value
                              ? 'bg-indigo-600 text-white'
                              : 'bg-white/5 text-gray-300 hover:bg-white/10'
                          }`}
                        >
                          {filter.label} ({filter.count})
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Category Filter */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Category</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { value: 'all', label: 'All', count: categoryCounts.all },
                        { value: 'work', label: 'Work', count: categoryCounts.work },
                        { value: 'personal', label: 'Personal', count: categoryCounts.personal },
                        { value: 'shopping', label: 'Shopping', count: categoryCounts.shopping },
                        { value: 'health', label: 'Health', count: categoryCounts.health },
                        { value: 'other', label: 'Other', count: categoryCounts.other }
                      ].map(filter => (
                        <button
                          key={filter.value}
                          onClick={() => setCategory(filter.value)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                            category === filter.value
                              ? 'bg-indigo-600 text-white'
                              : 'bg-white/5 text-gray-300 hover:bg-white/10'
                          }`}
                        >
                          {filter.label} ({filter.count})
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Priority Filter */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Priority</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { value: 'all', label: 'All', count: priorityCounts.all },
                        { value: 'low', label: 'Low', count: priorityCounts.low },
                        { value: 'medium', label: 'Medium', count: priorityCounts.medium },
                        { value: 'high', label: 'High', count: priorityCounts.high },
                        { value: 'urgent', label: 'Urgent', count: priorityCounts.urgent }
                      ].map(filter => (
                        <button
                          key={filter.value}
                          onClick={() => setPriority(filter.value)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                            priority === filter.value
                              ? 'bg-indigo-600 text-white'
                              : 'bg-white/5 text-gray-300 hover:bg-white/10'
                          }`}
                        >
                          {filter.label} ({filter.count})
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Due Date Filter */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Due Date</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { value: 'all', label: 'All', count: dueDateCounts.all },
                        { value: 'overdue', label: 'Overdue', count: dueDateCounts.overdue },
                        { value: 'today', label: 'Today', count: dueDateCounts.today },
                        { value: 'week', label: 'This Week', count: dueDateCounts.week }
                      ].map(filter => (
                        <button
                          key={filter.value}
                          onClick={() => setDueDate(filter.value)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                            dueDate === filter.value
                              ? 'bg-indigo-600 text-white'
                              : 'bg-white/5 text-gray-300 hover:bg-white/10'
                          }`}
                        >
                          {filter.label} ({filter.count})
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Active Filter Badges */}
          <div className="flex flex-wrap gap-2">
            {status !== 'all' && (
              <div className="flex items-center gap-1 bg-indigo-600/20 text-indigo-300 px-3 py-1.5 rounded-lg text-xs">
                <span>Status: {status}</span>
                <button onClick={() => setStatus('all')} className="ml-1 hover:text-white">
                  <X size={12} />
                </button>
              </div>
            )}
            {category !== 'all' && (
              <div className="flex items-center gap-1 bg-indigo-600/20 text-indigo-300 px-3 py-1.5 rounded-lg text-xs">
                <span>Category: {category}</span>
                <button onClick={() => setCategory('all')} className="ml-1 hover:text-white">
                  <X size={12} />
                </button>
              </div>
            )}
            {priority !== 'all' && (
              <div className="flex items-center gap-1 bg-indigo-600/20 text-indigo-300 px-3 py-1.5 rounded-lg text-xs">
                <span>Priority: {priority}</span>
                <button onClick={() => setPriority('all')} className="ml-1 hover:text-white">
                  <X size={12} />
                </button>
              </div>
            )}
            {dueDate !== 'all' && (
              <div className="flex items-center gap-1 bg-indigo-600/20 text-indigo-300 px-3 py-1.5 rounded-lg text-xs">
                <span>Due: {dueDate}</span>
                <button onClick={() => setDueDate('all')} className="ml-1 hover:text-white">
                  <X size={12} />
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}