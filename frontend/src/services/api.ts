/**
 * API service for backend communication.
 *
 * Centralizes all HTTP requests to the FastAPI backend.
 */

import type { ChatResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

/**
 * Send a chat message to the backend.
 *
 * @param message - User's message
 * @param threadId - Optional thread ID for conversation continuity
 * @returns Chat response with products/orders if applicable
 */
export async function sendChatMessage(
  message: string,
  threadId?: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}${API_PREFIX}/chat/message`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      thread_id: threadId || null,
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get conversation history for a thread.
 *
 * @param threadId - Thread identifier
 * @returns Conversation history
 */
export async function getChatHistory(threadId: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}${API_PREFIX}/chat/history/${threadId}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Health check endpoint.
 *
 * @returns Health status
 */
export async function checkHealth(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
