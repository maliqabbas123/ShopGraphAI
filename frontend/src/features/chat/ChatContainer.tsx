/**
 * Main chat container component.
 *
 * Manages chat state and orchestrates chat UI.
 */

import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage } from '../../components/chat/ChatMessage';
import { ChatInput } from '../../components/chat/ChatInput';
import { ProductList } from '../../components/products/ProductList';
import { sendChatMessage } from '../../services/api';
import type { ChatMessage as ChatMessageType, Product } from '../../types';

export const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [threadId, setThreadId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message immediately
    const userMessage: ChatMessageType = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send to backend
      const response = await sendChatMessage(content, threadId);

      // Update thread ID if new
      if (!threadId) {
        setThreadId(response.thread_id);
      }

      // Add assistant message
      const assistantMessage: ChatMessageType = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Update products if provided
      if (response.products) {
        setProducts(response.products);
      }

      // Handle order confirmation
      if (response.order_confirmation) {
        console.log('Order placed:', response.order_confirmation);
      }
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);

      // Add error message
      const errorMessage: ChatMessageType = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-6xl mx-auto bg-white shadow-lg">
      {/* Header */}
      <div className="p-5 border-b border-gray-200 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <h1 className="text-2xl font-bold mb-1">ShopGraph AI</h1>
        <p className="text-sm opacity-90">
          Your AI Shopping Assistant powered by LangGraph
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-5 bg-gray-50 scrollbar-custom">
        {messages.length === 0 && (
          <div className="max-w-2xl mx-auto my-10 text-center">
            <h2 className="text-3xl mb-4">👋 Welcome!</h2>
            <p className="mb-4 text-gray-600">I'm your AI shopping assistant. I can help you:</p>
            <ul className="list-none text-left max-w-md mx-auto my-5 space-y-2">
              <li className="py-2 text-base">🔍 Find products based on your preferences</li>
              <li className="py-2 text-base">⚖️ Compare multiple products</li>
              <li className="py-2 text-base">🛒 Place orders</li>
              <li className="py-2 text-base">💬 Answer product questions</li>
            </ul>
            <p className="mt-6 py-3 px-5 bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg font-medium text-blue-500">
              Try: "Find gaming laptops under $1500"
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}

        {products.length > 0 && <ProductList products={products} />}

        {isLoading && (
          <div className="flex gap-2 p-4 justify-center">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.32s]"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.16s]"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
          </div>
        )}

        {error && (
          <div className="py-3 px-5 mx-4 my-4 bg-red-50 border border-red-500 rounded-lg text-red-500 text-center">
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
};
