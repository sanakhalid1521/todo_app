"use client";

import { useState, useEffect } from "react";
import { useModal } from "@/context/ModalContext";
import { useSearch } from "@/context/SearchContext";
import { tasksAPI } from "@/lib/tasks-api";
import {
  Plus, Check, Trash2, CheckCircle2, X, Calendar, AlignLeft,
  Filter, CheckSquare, Clock, ListTodo, Eye, TrendingUp, Target, Edit3, Flag, Tag, Search as SearchIcon
} from "lucide-react";
import { useTaskUpdates } from '@/hooks/useTaskUpdates';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  dueDate?: string; // Optional field for UI purposes
  priority?: "low" | "medium" | "high"; // Optional field for UI purposes
  category?: string; // Optional field for UI purposes
  status?: "pending" | "in_progress" | "completed"; // Optional field for UI purposes
}

export default function TasksPage() {
  const { isTaskModalOpen, closeTaskModal, openTaskModal } = useModal();
  const { searchQuery, activeFilter, setActiveFilter } = useSearch();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // Listen for task updates from the chatbot
  const updateTrigger = useTaskUpdates();

  useEffect(() => {
    loadTasks();
  }, []); // Initial load only

  useEffect(() => {
    // Reload tasks when updateTrigger changes (when chatbot makes changes)
    loadTasks();
  }, [updateTrigger]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      // Fetch tasks from the API
      const apiTasks = await tasksAPI.listTasks();
      // Map API response to our Task interface
      const mappedTasks: Task[] = apiTasks.map(task => ({
        ...task,
        dueDate: task.updated_at, // Using updated_at as due date for now
        priority: "medium", // Default priority since API doesn't have this field
        category: "General", // Default category since API doesn't have this field
        status: task.completed ? "completed" : "pending" // Set status based on completion
      }));
      setTasks(mappedTasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      // Fallback to demo tasks if API fails
      const demoTasks: Task[] = [
        {
          id: 1,
          user_id: 'user-uuid-placeholder',
          title: "System Synchronization",
          description: "Perform deep sync of core modules with the central server.",
          completed: true,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-01T12:00",
          priority: "high",
          category: "System",
          status: "completed"
        },
        {
          id: 2,
          user_id: 'user-uuid-placeholder',
          title: "Network Perimeter Check",
          description: "Verify firewall integrity and scan for unusual traffic patterns.",
          completed: false,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-01T14:00",
          priority: "medium",
          category: "Security",
          status: "in_progress"
        },
        {
          id: 3,
          user_id: 'user-uuid-placeholder',
          title: "Database Optimization",
          description: "Index the latest mission logs and clear temporary cache files.",
          completed: false,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-01T16:00",
          priority: "low",
          category: "Database",
          status: "pending"
        },
        {
          id: 4,
          user_id: 'user-uuid-placeholder',
          title: "Tactical Briefing Preparation",
          description: "Compile data for the upcoming strategic overview session.",
          completed: false,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-02T09:00",
          priority: "high",
          category: "Planning",
          status: "pending"
        },
        {
          id: 5,
          user_id: 'user-uuid-placeholder',
          title: "Module Alpha Refactor",
          description: "Upgrade terminal handling for unicode support and refined UI icons.",
          completed: false,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-02T18:00",
          priority: "medium",
          category: "Dev",
          status: "in_progress"
        },
        {
          id: 6,
          user_id: 'user-uuid-placeholder',
          title: "Resource Audit",
          description: "Inventory available server credits and allocated cloud assets.",
          completed: false,
          created_at: "2026-01-01T10:00:00",
          updated_at: "2026-01-01T12:00:00",
          dueDate: "2026-01-03T10:00",
          priority: "low",
          category: "Admin",
          status: "pending"
        }
      ];
      setTasks(demoTasks);
    } finally {
      setLoading(false);
    }
  };

  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);

  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newDate, setNewDate] = useState("");
  const [newPriority, setNewPriority] = useState<"low" | "medium" | "high">("medium");
  const [newCategory, setNewCategory] = useState("General");

  const saveTask = async () => {
    if (!newTitle.trim()) return;

    try {
      if (editingTaskId) {
        // Update existing task via API
        const updatedTask = await tasksAPI.updateTask(editingTaskId, {
          title: newTitle,
          description: newDesc,
          completed: tasks.find(t => t.id === editingTaskId)?.completed || false
        });
        // Update local state with API response
        setTasks(tasks.map(t =>
          t.id === editingTaskId
            ? {
                ...updatedTask,
                dueDate: updatedTask.updated_at,
                priority: t.priority || "medium",
                category: t.category || "General",
                status: updatedTask.completed ? "completed" : "pending"
              }
            : t
        ));
      } else {
        // Create new task via API
        const newTaskAPI = await tasksAPI.createTask({
          title: newTitle,
          description: newDesc,
        });
        // Add to local state with API response
        const newTask: Task = {
          ...newTaskAPI,
          dueDate: newTaskAPI.updated_at,
          priority: newPriority,
          category: newCategory,
          status: newTaskAPI.completed ? "completed" : "pending"
        };
        setTasks([newTask, ...tasks]);
      }
      handleCloseSidebar();
      // Reload tasks to sync with API
      await loadTasks();
    } catch (error) {
      console.error('Failed to save task:', error);
    }
  };

  const handleEditClick = (task: Task) => {
    setEditingTaskId(task.id);
    setNewTitle(task.title);
    setNewDesc(task.description);
    setNewDate(task.dueDate || task.updated_at);
    setNewPriority(task.priority || "medium");
    setNewCategory(task.category || "General");
    openTaskModal();
  };

  const handleCloseSidebar = () => {
    closeTaskModal();
    setEditingTaskId(null);
    setNewTitle("");
    setNewDesc("");
    setNewDate("");
    setNewPriority("medium");
    setNewCategory("General");
  };

  const toggleTask = async (id: number) => {
    try {
      // Toggle via API
      const updatedTask = await tasksAPI.toggleComplete(id);
      // Update local state with API response
      setTasks(tasks.map(task =>
        task.id === id
          ? {
              ...updatedTask,
              dueDate: updatedTask.updated_at,
              priority: task.priority || "medium",
              category: task.category || "General",
              status: updatedTask.completed ? "completed" : "pending"
            }
          : task
      ));
    } catch (error) {
      console.error('Failed to toggle task:', error);
    }
  };

  const deleteTask = async (id: number) => {
    try {
      // Delete via API
      await tasksAPI.deleteTask(id);
      // Update local state
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (task.category && task.category.toLowerCase().includes(searchQuery.toLowerCase()));

    if (!matchesSearch) return false;

    if (activeFilter === "completed") return task.completed;
    if (activeFilter === "pending") return !task.completed;
    return true;
  });

  const stats = {
    progress: tasks.length > 0 ? Math.round((tasks.filter(t => t.completed).length / tasks.length) * 100) : 0
  };

  return (
    <div className="min-h-screen font-sans text-slate-300 relative overflow-x-hidden pb-10">
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">

        {/* Global Progress - Refined */}
        <div className="mb-8 glass-panel p-6 rounded-3xl border-white/5">
            <div className="flex flex-col md:flex-row gap-6 items-center">
                <div className="flex-1 space-y-3 w-full">
                    <div className="flex justify-between items-center">
                        <h2 className="text-white text-lg font-bold tracking-tight">MISSION PROGRESS</h2>
                        <span className="text-2xl font-bold text-white tracking-tighter">{stats.progress}%</span>
                    </div>
                    <div className="h-3 w-full bg-white/5 rounded-full overflow-hidden border border-white/10 shadow-inner">
                        <div
                            className="h-full bg-indigo-500 transition-all duration-1000 ease-out shadow-[0_0_20px_rgba(99,102,241,0.5)]"
                            style={{ width: `${stats.progress}%` }}
                        ></div>
                    </div>
                </div>
            </div>
        </div>

        {/* Action Bar - Search Informed */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8 glass-panel p-4 rounded-3xl border-white/5 shadow-2xl">
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 sm:pb-0">
            {["all", "pending", "completed"].map((f) => (
               <button
                key={f}
                onClick={() => setActiveFilter(f as any)}
                className={`flex-shrink-0 px-5 py-2 rounded-xl text-[10px] font-bold uppercase tracking-widest transition-all ${activeFilter === f ? 'bg-white text-[#0f172a] shadow-lg shadow-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
               >
                {f}
               </button>
            ))}
          </div>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            {searchQuery && (
              <div className="flex-1 sm:flex-initial px-4 py-2 glass-input rounded-xl border border-indigo-500/30 flex items-center gap-2 animate-in zoom-in-95 duration-200">
                <SearchIcon size={12} className="text-indigo-400" />
                <span className="text-[10px] font-bold text-white truncate max-w-[100px] uppercase tracking-wider">{searchQuery}</span>
              </div>
            )}
            <button
              onClick={openTaskModal}
              className="px-6 py-2.5 bg-white text-[#0f172a] rounded-xl hover:bg-gray-100 transition-all flex items-center justify-center gap-2 font-bold text-[10px] uppercase tracking-[0.2em] shadow-xl active:scale-95 glass-button-glow flex-1 sm:flex-initial"
            >
              <Plus size={14} /> New Directive
            </button>
          </div>
        </div>

        {/* Task Section - Refined */}
        <div className="glass-card rounded-[2.5rem] border-white/5 overflow-hidden mb-20 shadow-2xl">
          <div className="p-8 border-b border-white/5 bg-white/[0.02] flex items-center justify-between">
            <h1 className="text-xl font-bold text-white tracking-widest uppercase">Active Directives</h1>
            <div className="w-10 h-10 rounded-2xl glass-input flex items-center justify-center text-gray-500 shadow-inner">
                <Filter size={18} />
            </div>
          </div>

          <div className="p-8 space-y-4">
              {filteredTasks.length === 0 ? (
                <div className="text-center py-20 rounded-3xl border border-white/5 bg-white/[0.01]">
                  <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-4 border border-white/10">
                    <ListTodo size={24} className="text-gray-600" />
                  </div>
                  <p className="text-gray-500 font-bold text-xs tracking-[0.3em] uppercase">No Directives Found</p>
                  {searchQuery && <p className="text-gray-700 text-[10px] mt-2 font-bold uppercase">Clear search to see all tasks</p>}
                </div>
              ) : (
                filteredTasks.map(task => (
                  <div key={task.id} className={`group flex flex-col sm:flex-row sm:items-center gap-4 p-6 rounded-3xl transition-all duration-500 border border-white/5 glass-input hover:border-white/20 hover:shadow-2xl ${task.completed ? 'opacity-30 grayscale-[0.8]' : 'opacity-100'}`}>
                    <div className="flex items-start gap-5 flex-1">
                        <button onClick={() => toggleTask(task.id)} className={`mt-1.5 w-7 h-7 rounded-xl flex items-center justify-center border transition-all duration-300 ${task.completed ? 'bg-white text-[#0f172a] border-white shadow-lg' : 'border-white/10 hover:border-white/30 bg-white/5 shadow-inner'}`}>
                            {task.completed && <Check size={16} strokeWidth={3} />}
                        </button>
                        <div className="flex-1 space-y-3">
                            <div>
                                <h3 className={`font-bold text-xl transition-all leading-tight tracking-tight ${task.completed ? 'line-through text-gray-500' : 'text-white'}`}>{task.title}</h3>
                                {task.description && <p className="text-gray-500 mt-2 text-xs font-semibold leading-relaxed line-clamp-2 uppercase tracking-wide opacity-60">{task.description}</p>}
                            </div>
                            <div className="flex flex-wrap gap-2 pt-1">
                                <div className="px-3 py-1.5 bg-white/[0.03] rounded-xl border border-white/5 text-[9px] font-bold uppercase tracking-widest text-indigo-400 flex items-center gap-2 group-hover:bg-indigo-500/10 transition-colors">
                                    <Tag size={12} /> {task.category || 'General'}
                                </div>
                                <div className={`px-3 py-1.5 rounded-xl text-[9px] font-bold uppercase tracking-widest flex items-center gap-2 ${task.priority === 'high' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-white/[0.03] text-gray-500 border border-white/5'}`}>
                                    <Flag size={12} /> {task.priority || 'medium'}
                                </div>
                                <div className="px-3 py-1.5 bg-white/[0.03] rounded-xl border border-white/5 text-[9px] font-bold uppercase tracking-widest text-gray-500 flex items-center gap-2 ml-auto sm:ml-0">
                                    <Clock size={12} /> {task.dueDate ? new Date(task.dueDate).toLocaleDateString() : new Date(task.updated_at).toLocaleDateString()}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-3 self-end sm:self-center">
                      <button onClick={() => handleEditClick(task)} className="p-3 bg-white/[0.02] hover:bg-white/[0.08] text-gray-500 hover:text-white rounded-2xl transition-all border border-white/5 shadow-sm active:scale-95"><Edit3 size={18} /></button>
                      <button onClick={() => deleteTask(task.id)} className="p-3 bg-white/[0.02] hover:bg-red-500/10 text-gray-600 hover:text-red-400 rounded-2xl transition-all border border-white/5 shadow-sm active:scale-95"><Trash2 size={18} /></button>
                    </div>
                  </div>
                ))
              )}
          </div>
        </div>

        {/* Sidebar - Refined Glass */}
        <div className={`fixed inset-0 z-[100] ${isTaskModalOpen ? 'block' : 'hidden'}`}>
            <div className="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity duration-500" onClick={handleCloseSidebar}></div>
            <div className={`absolute right-0 top-0 h-full w-full max-w-lg glass-panel shadow-[0_0_100px_rgba(0,0,0,0.5)] transition-transform duration-500 transform ${isTaskModalOpen ? 'translate-x-0' : 'translate-x-full'} flex flex-col border-l border-white/10`}>
                <div className="p-8 border-b border-white/5 flex items-center justify-between bg-white/[0.02] shadow-sm">
                    <h2 className="text-xl font-bold text-white tracking-[0.3em] uppercase">{editingTaskId ? "Edit Mission" : "New Mission"}</h2>
                    <button onClick={handleCloseSidebar} className="p-3 text-gray-500 hover:text-white transition-all hover:bg-white/5 rounded-2xl"><X size={24} /></button>
                </div>

                <div className="flex-1 overflow-y-auto p-8 space-y-10 no-scrollbar">
                    <div className="space-y-3">
                        <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.4em] ml-2">Mission Title</label>
                        <input value={newTitle} onChange={e => setNewTitle(e.target.value)} placeholder="Entry level objective..." className="w-full px-8 py-5 glass-input focus:bg-white/[0.05] focus:border-white/30 rounded-2xl outline-none transition-all placeholder:text-gray-800 font-bold text-white text-2xl shadow-inner" />
                    </div>

                    <div className="grid grid-cols-2 gap-8">
                        <div className="space-y-3">
                            <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.4em] ml-2">Priority</label>
                            <select value={newPriority} onChange={e => setNewPriority(e.target.value as any)} className="w-full px-6 py-4 glass-input rounded-2xl font-bold text-[10px] uppercase text-white outline-none cursor-pointer shadow-inner">
                                <option value="low" className="bg-[#0f172a]">Low Level</option>
                                <option value="medium" className="bg-[#0f172a]">Medium Risk</option>
                                <option value="high" className="bg-[#0f172a]">High Priority</option>
                            </select>
                        </div>
                        <div className="space-y-3">
                            <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.4em] ml-2">Sector</label>
                            <input value={newCategory} onChange={e => setNewCategory(e.target.value)} className="w-full px-6 py-4 glass-input rounded-2xl font-bold text-[10px] uppercase text-white outline-none shadow-inner" placeholder="GENERAL" />
                        </div>
                    </div>

                    <div className="space-y-3">
                        <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.4em] ml-2">Temporal Window</label>
                        <div className="relative">
                            <Calendar size={14} className="absolute left-6 top-1/2 -translate-y-1/2 text-gray-500" />
                            <input type="datetime-local" value={newDate} onChange={e => setNewDate(e.target.value)} className="w-full px-14 py-5 glass-input rounded-3xl font-bold text-white uppercase text-xs cursor-pointer shadow-inner border-white/5" />
                        </div>
                    </div>

                    <div className="space-y-3">
                        <label className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.4em] ml-2">Briefing Details</label>
                        <textarea value={newDesc} onChange={e => setNewDesc(e.target.value)} rows={5} className="w-full px-8 py-6 glass-input rounded-3xl text-gray-300 font-semibold leading-relaxed resize-none shadow-inner text-sm border-white/5" placeholder="Detailed objective notes..." />
                    </div>
                </div>

                <div className="p-10 glass-panel border-t border-white/5 flex gap-5">
                    <button onClick={handleCloseSidebar} className="flex-1 py-5 text-gray-600 font-bold text-[10px] uppercase tracking-[0.3em] hover:text-white transition-all rounded-2xl hover:bg-white/[0.02]">Abort</button>
                    <button onClick={saveTask} disabled={!newTitle.trim()} className="flex-[2] py-5 bg-white text-[#0f172a] rounded-2xl shadow-2xl font-black text-[10px] uppercase tracking-[0.4em] active:scale-95 transition-all glass-button-glow disabled:opacity-50">Confirm Directive</button>
                </div>
            </div>
        </div>
      </main>
    </div>
  );
}
