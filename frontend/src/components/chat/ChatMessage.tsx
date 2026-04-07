/**
 * Chat message component.
 *
 * Displays a single message in the chat interface.
 */

import React from 'react';
import type { ChatMessage as ChatMessageType } from '../../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const { role, content } = message;

  return (
    <div
      className={`flex gap-3 p-4 animate-slide-in ${
        role === 'user' ? 'flex-row-reverse' : ''
      }`}
    >
      <div
        className={`w-9 h-9 rounded-full flex items-center justify-center text-xl flex-shrink-0 ${
          role === 'assistant' ? 'bg-blue-500' : 'bg-gray-100'
        }`}
      >
        {role === 'user' ? '👤' : '🤖'}
      </div>

      <div className={`flex-1 max-w-[70%] ${role === 'user' ? 'text-right' : ''}`}>
        <div className="text-xs font-semibold text-gray-500 mb-1">
          {role === 'user' ? 'You' : 'ShopGraph AI'}
        </div>
        <div
          className={`py-3 px-4 rounded-lg leading-relaxed whitespace-pre-wrap ${
            role === 'user'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          {content}
        </div>
      </div>
    </div>
  );
};
