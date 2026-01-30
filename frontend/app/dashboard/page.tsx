'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { tasksAPI } from '@/lib/tasks-api';

// Define types for our statistics
interface TaskStats {
  total: number;
  completed: number;
  pending: number;
  completion_rate: number;
  by_category: {
    work: number;
    personal: number;
    shopping: number;
    health: number;
    other: number;
  };
  by_priority: {
    low: number;
    medium: number;
    high: number;
    urgent: number;
  };
  overdue: number;
  due_today: number;
  due_this_week: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<TaskStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        // Get user ID from auth system
        const { getUserId } = await import('@/lib/auth');
        const userId = getUserId() || 'user-demo';

        // Fetch stats from API
        const response = await fetch(`/api/${userId}/tasks/stats`);
        if (!response.ok) {
          throw new Error('Failed to fetch statistics');
        }
        const data: TaskStats = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Error fetching stats:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen font-sans text-slate-300 relative overflow-x-hidden">
        <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto"></div>
            <p className="mt-4 text-gray-500">Loading dashboard...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen font-sans text-slate-300 relative overflow-x-hidden">
        <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
          <div className="text-center py-20">
            <p className="text-red-500">Error: {error}</p>
          </div>
        </main>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-screen font-sans text-slate-300 relative overflow-x-hidden">
        <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
          <div className="text-center py-20">
            <p className="text-gray-500">No statistics available</p>
          </div>
        </main>
      </div>
    );
  }

  // Prepare data for charts
  const categoryData = [
    { name: 'Work', value: stats.by_category.work },
    { name: 'Personal', value: stats.by_category.personal },
    { name: 'Shopping', value: stats.by_category.shopping },
    { name: 'Health', value: stats.by_category.health },
    { name: 'Other', value: stats.by_category.other },
  ];

  const priorityData = [
    { name: 'Low', value: stats.by_priority.low, color: '#10B981' }, // green
    { name: 'Medium', value: stats.by_priority.medium, color: '#FBBF24' }, // yellow
    { name: 'High', value: stats.by_priority.high, color: '#F59E0B' }, // amber
    { name: 'Urgent', value: stats.by_priority.urgent, color: '#EF4444' }, // red
  ];

  const completionData = [
    { name: 'Total', value: stats.total },
    { name: 'Completed', value: stats.completed },
    { name: 'Pending', value: stats.pending },
  ];

  // Colors for charts
  const COLORS_CATEGORY = ['#3B82F6', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B'];
  const COLORS_PRIORITY = priorityData.map(item => item.color);

  return (
    <div className="min-h-screen font-sans text-slate-300 relative overflow-x-hidden">
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white tracking-tight">Dashboard</h1>
          <p className="text-gray-400 mt-2">Track your productivity and task statistics</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-3xl font-bold text-white">{stats.total}</div>
            <div className="text-gray-400 text-sm">Total Tasks</div>
          </div>
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-3xl font-bold text-white">{stats.completed}</div>
            <div className="text-gray-400 text-sm">Completed</div>
          </div>
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-3xl font-bold text-white">{stats.pending}</div>
            <div className="text-gray-400 text-sm">Pending</div>
          </div>
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-3xl font-bold text-white">{stats.completion_rate}%</div>
            <div className="text-gray-400 text-sm">Completion Rate</div>
          </div>
        </div>

        {/* Due Date Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-2xl font-bold text-red-400">{stats.overdue}</div>
            <div className="text-gray-400 text-sm">Overdue</div>
          </div>
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-2xl font-bold text-yellow-400">{stats.due_today}</div>
            <div className="text-gray-400 text-sm">Due Today</div>
          </div>
          <div className="glass-panel p-6 rounded-2xl border-white/5">
            <div className="text-2xl font-bold text-blue-400">{stats.due_this_week}</div>
            <div className="text-gray-400 text-sm">Due This Week</div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Category Distribution - Pie Chart */}
          <div className="glass-card rounded-2xl border-white/5 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Tasks by Category</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS_CATEGORY[index % COLORS_CATEGORY.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value} tasks`, 'Count']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Priority Distribution - Pie Chart */}
          <div className="glass-card rounded-2xl border-white/5 p-6">
            <h2 className="text-xl font-bold text-white mb-4">Tasks by Priority</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={priorityData}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {priorityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value} tasks`, 'Count']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Task Status - Bar Chart */}
          <div className="glass-card rounded-2xl border-white/5 p-6 lg:col-span-2">
            <h2 className="text-xl font-bold text-white mb-4">Task Status Overview</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={[{
                    name: 'Tasks',
                    total: stats.total,
                    completed: stats.completed,
                    pending: stats.pending
                  }]}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '0.5rem' }}
                    formatter={(value) => [value, 'Count']}
                  />
                  <Legend />
                  <Bar dataKey="total" name="Total Tasks" fill="#6366F1" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="completed" name="Completed" fill="#10B981" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="pending" name="Pending" fill="#F59E0B" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}