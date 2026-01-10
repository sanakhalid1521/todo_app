"use client";

import { useState, useRef, useEffect } from "react";
import { MessageCircle, Send, X, Bot, User } from "lucide-react";
import { tasksAPI, Task } from "@/lib/tasks-api";

// Define types for chat messages
type ChatMessage = {
  id: number;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
};

type ChatResponse = {
  response: string;
  session_id: string;
  timestamp: string;
};

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: 1, text: "Hello! I'm your TodoPro assistant. How can I help you manage your tasks today?", sender: "bot", timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false); // Track loading state
  const [sessionId, setSessionId] = useState<string | null>(null); // Track session ID
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Function to send message to the AI chatbot backend
  const sendMessageToBackend = async (message: string) => {
    try {
      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          user_id: 'user-demo', // In a real app, this would come from auth context
          session_id: sessionId || undefined
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      // Update session ID if this is the first message in the session
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      return data.response;
    } catch (error) {
      console.error("Failed to send message to chatbot:", error);
      return "Sorry, I encountered an error processing your request. Please try again.";
    }
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();

    // Add user message to UI immediately
    const newUserMessage: ChatMessage = {
      id: messages.length + 1,
      text: userMessage,
      sender: "user",
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      // Send message to backend and get AI response
      const aiResponse = await sendMessageToBackend(userMessage);

      // Add AI response to UI
      const newBotMessage: ChatMessage = {
        id: messages.length + 2,
        text: aiResponse,
        sender: "bot",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, newBotMessage]);
    } catch (error) {
      console.error("Error handling message:", error);

      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: messages.length + 2,
        text: "Sorry, I encountered an error processing your request. Please try again.",
        sender: "bot",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
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

            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-[85%] rounded-2xl px-4 py-3 bg-gray-800 text-gray-200 rounded-bl-none border border-gray-700">
                  <div className="flex items-center gap-2">
                    <Bot size={14} className="mt-0.5 flex-shrink-0 text-indigo-400" />
                    <div className="text-sm">Thinking...</div>
                  </div>
                </div>
              </div>
            )}

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
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  inputValue.trim() && !isLoading
                    ? "bg-indigo-600 text-white hover:bg-indigo-700"
                    : "bg-gray-700 text-gray-500 cursor-not-allowed"
                } transition-colors`}
                aria-label="Send message"
              >
                {isLoading ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Send size={16} />
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}