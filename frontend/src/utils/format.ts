/**
 * Utility functions for formatting data.
 */

/**
 * Format price with currency symbol.
 */
export function formatPrice(price: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(price);
}

/**
 * Format rating display.
 */
export function formatRating(rating: number): string {
  return `${rating.toFixed(1)}`;
}

/**
 * Format timestamp to readable date.
 */
export function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleString();
}
