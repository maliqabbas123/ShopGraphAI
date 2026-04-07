/**
 * TypeScript type definitions for the application.
 */

export interface Product {
  id: string;
  title: string;
  brand: string;
  price: number;
  rating: number;
  stock: number;
  category: string;
  attributes: Record<string, string>;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  thread_id: string;
  response: string;
  products?: Product[];
  comparison?: any;
  order_confirmation?: any;
  intent?: string;
}

export interface OrderConfirmation {
  order_id: string;
  product_title: string;
  total_amount: number;
  currency: string;
  status: string;
  message: string;
}
