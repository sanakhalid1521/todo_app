"use client";

import { useState, useRef, useEffect } from "react";
import { MessageCircle, Send, X, Bot, User, CheckCircle2, Trash2 } from "lucide-react";
import { tasksAPI, Task } from "@/lib/tasks-api";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your TodoPro assistant. How can I help you today? Type 'show tasks' to see your tasks, 'add task [name]' to create, 'complete task [name]' to mark done, or 'delete task [name]' to remove.", sender: "bot", timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Function to load tasks
  const loadTasks = async () => {
    try {
      const loadedTasks = await tasksAPI.listTasks();
      setTasks(loadedTasks);

      // Add response message
      const responseText = loadedTasks.length > 0
        ? `You have ${loadedTasks.length} tasks:\n${loadedTasks.slice(0, 5).map(t => `- ${t.title} (${t.completed ? '✓ Completed' : '○ Pending'})`).join('\n')}${loadedTasks.length > 5 ? '\n...and more' : ''}`
        : "You don't have any tasks yet. Type 'add task [name]' to create one!";

      const newBotMessage = {
        id: messages.length + 1,
        text: responseText,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      const newBotMessage = {
        id: messages.length + 1,
        text: "Sorry, I couldn't load your tasks. Please try again later.",
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  // Function to add a task
  const addTask = async (title: string, description: string = "Added via chatbot") => {
    try {
      const newTask = await tasksAPI.createTask({ title, description });
      setTasks(prev => [...prev, newTask]);

      const newBotMessage = {
        id: messages.length + 1,
        text: `Task "${title}" has been added successfully!`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      const newBotMessage = {
        id: messages.length + 1,
        text: `Sorry, I couldn't add the task. Error: ${(error as Error).message}`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  // Function to complete a task
  const completeTask = async (taskTitle: string) => {
    try {
      const taskToComplete = tasks.find(t => t.title.toLowerCase().includes(taskTitle.toLowerCase()));

      if (!taskToComplete) {
        // Try to find in API directly if not in local state
        const allTasks = await tasksAPI.listTasks();
        const task = allTasks.find(t => t.title.toLowerCase().includes(taskTitle.toLowerCase()));

        if (!task) {
          const newBotMessage = {
            id: messages.length + 1,
            text: `I couldn't find a task with "${taskTitle}". Try showing tasks first with 'show tasks'.`,
            sender: "bot",
            timestamp: new Date()
          };
          setMessages(prev => [...prev, newBotMessage]);
          return;
        }

        const updatedTask = await tasksAPI.toggleComplete(task.id);
        setTasks(prev => prev.map(t => t.id === task.id ? updatedTask : t));

        const newBotMessage = {
          id: messages.length + 1,
          text: `Task "${task.title}" has been marked as completed!`,
          sender: "bot",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, newBotMessage]);
        return;
      }

      const updatedTask = await tasksAPI.toggleComplete(taskToComplete.id);
      setTasks(prev => prev.map(t => t.id === taskToComplete.id ? updatedTask : t));

      const newBotMessage = {
        id: messages.length + 1,
        text: `Task "${taskToComplete.title}" has been marked as completed!`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      const newBotMessage = {
        id: messages.length + 1,
        text: `Sorry, I couldn't complete the task. Error: ${(error as Error).message}`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  // Function to delete a task
  const deleteTask = async (taskTitle: string) => {
    try {
      const taskToDelete = tasks.find(t => t.title.toLowerCase().includes(taskTitle.toLowerCase()));

      if (!taskToDelete) {
        // Try to find in API directly if not in local state
        const allTasks = await tasksAPI.listTasks();
        const task = allTasks.find(t => t.title.toLowerCase().includes(taskTitle.toLowerCase()));

        if (!task) {
          const newBotMessage = {
            id: messages.length + 1,
            text: `I couldn't find a task with "${taskTitle}". Try showing tasks first with 'show tasks'.`,
            sender: "bot",
            timestamp: new Date()
          };
          setMessages(prev => [...prev, newBotMessage]);
          return;
        }

        await tasksAPI.deleteTask(task.id);
        setTasks(prev => prev.filter(t => t.id !== task.id));

        const newBotMessage = {
          id: messages.length + 1,
          text: `Task "${task.title}" has been deleted!`,
          sender: "bot",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, newBotMessage]);
        return;
      }

      await tasksAPI.deleteTask(taskToDelete.id);
      setTasks(prev => prev.filter(t => t.id !== taskToDelete.id));

      const newBotMessage = {
        id: messages.length + 1,
        text: `Task "${taskToDelete.title}" has been deleted!`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      const newBotMessage = {
        id: messages.length + 1,
        text: `Sorry, I couldn't delete the task. Error: ${(error as Error).message}`,
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const newUserMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newUserMessage]);
    const userMessage = inputValue.toLowerCase().trim();
    setInputValue("");

    // Handle different commands
    if (userMessage.includes('show') && userMessage.includes('task')) {
      await loadTasks();
    } else if (userMessage.includes('add') && userMessage.includes('task')) {
      // Extract task title from message
      const titleMatch = inputValue.match(/(?:add task|task to add|create task)\s+(.+)/i);
      if (titleMatch && titleMatch[1]) {
        await addTask(titleMatch[1].trim());
      } else {
        // Ask for task details
        const newBotMessage = {
          id: messages.length + 2,
          text: "What would you like to name your new task?",
          sender: "bot",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, newBotMessage]);
      }
    } else if ((userMessage.includes('complete') || userMessage.includes('finish') || userMessage.includes('done')) && userMessage.includes('task')) {
      // Extract task title from message
      const titleMatch = inputValue.match(/(?:complete task|finish task|done task|mark as done)\s+(.+)/i);
      if (titleMatch && titleMatch[1]) {
        await completeTask(titleMatch[1].trim());
      } else {
        // Ask for task details
        const newBotMessage = {
          id: messages.length + 2,
          text: "Which task would you like to mark as complete? Please provide the task name.",
          sender: "bot",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, newBotMessage]);
      }
    } else if ((userMessage.includes('delete') || userMessage.includes('remove')) && userMessage.includes('task')) {
      // Extract task title from message
      const titleMatch = inputValue.match(/(?:delete task|remove task)\s+(.+)/i);
      if (titleMatch && titleMatch[1]) {
        await deleteTask(titleMatch[1].trim());
      } else {
        // Ask for task details
        const newBotMessage = {
          id: messages.length + 2,
          text: "Which task would you like to delete? Please provide the task name.",
          sender: "bot",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, newBotMessage]);
      }
    } else if (userMessage.includes('hello') || userMessage.includes('hi')) {
      const newBotMessage = {
        id: messages.length + 2,
        text: "Hello! How can I help you with your tasks today? You can ask me to show tasks, add a new task, complete a task, or delete a task.",
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    } else {
      // Default response
      const newBotMessage = {
        id: messages.length + 2,
        text: "I can help you manage your tasks! You can ask me to:\n- Show your tasks (type 'show tasks')\n- Add a new task (type 'add task [name]')\n- Complete a task (type 'complete task [name]')\n- Delete a task (type 'delete task [name]')",
        sender: "bot",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, newBotMessage]);
    }
  };

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-indigo-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-xs text-white animate-pulse">
            1
          </span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-20 right-6 z-50 w-80 h-[500px] bg-gray-900 rounded-2xl shadow-2xl border border-gray-700 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-gray-800 text-white p-4 flex items-center justify-between border-b border-gray-700">
            <div className="flex items-center gap-2">
              <Bot size={20} className="text-indigo-400" />
              <h3 className="font-bold tracking-wider uppercase text-sm">TodoPro Assistant</h3>
            </div>
            <button
              onClick={toggleChat}
              className="text-gray-400 hover:text-white focus:outline-none transition-colors"
              aria-label="Close chat"
            >
              <X size={20} />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-900">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                    message.sender === "user"
                      ? "bg-indigo-600 text-white rounded-br-none"
                      : "bg-gray-800 text-gray-200 rounded-bl-none border border-gray-700"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {message.sender === "bot" && (
                      <Bot size={14} className="mt-0.5 flex-shrink-0 text-indigo-400" />
                    )}
                    <div className="whitespace-pre-line">
                      <span>{message.text}</span>
                    </div>
                    {message.sender === "user" && (
                      <User size={14} className="mt-0.5 flex-shrink-0" />
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="border-t border-gray-700 p-3 bg-gray-800">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me to show/add/complete/delete tasks..."
                className="flex-1 bg-gray-700 border border-gray-600 rounded-xl px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                aria-label="Type your message"
              />
              <button
                type="submit"
                disabled={!inputValue.trim()}
                className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  inputValue.trim()
                    ? "bg-indigo-600 text-white hover:bg-indigo-700"
                    : "bg-gray-700 text-gray-500 cursor-not-allowed"
                } transition-colors`}
                aria-label="Send message"
              >
                <Send size={16} />
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}