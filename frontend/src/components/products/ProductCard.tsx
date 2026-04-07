/**
 * Product card component.
 *
 * Displays product information in a card format.
 */

import React from 'react';
import type { Product } from '../../types';
import { formatPrice } from '../../utils/format';

interface ProductCardProps {
  product: Product;
  index?: number;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, index }) => {
  const { title, brand, price, rating, stock, attributes } = product;

  return (
    <div className="relative bg-white border border-gray-200 rounded-lg p-4 transition-all hover:shadow-lg hover:-translate-y-0.5">
      {index !== undefined && (
        <div className="absolute top-2 right-2 w-7 h-7 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold">
          {index + 1}
        </div>
      )}

      <div className="mb-3">
        <h3 className="text-base font-semibold mb-1 text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500">{brand}</p>
      </div>

      <div className="text-2xl font-bold text-blue-500 mb-3">
        {formatPrice(price)}
      </div>

      <div className="flex justify-between items-center py-2 border-t border-b border-gray-200 mb-3 text-sm">
        <div className="text-gray-500">⭐ {rating.toFixed(1)}/5</div>
        <div className={`font-medium ${stock === 0 ? 'text-red-500' : 'text-green-500'}`}>
          {stock > 0 ? `${stock} in stock` : 'Out of stock'}
        </div>
      </div>

      {Object.keys(attributes).length > 0 && (
        <div className="flex flex-col gap-1.5">
          {Object.entries(attributes).slice(0, 3).map(([key, value]) => (
            <div key={key} className="flex gap-2 text-xs">
              <span className="text-gray-500 font-medium capitalize">{key}:</span>
              <span className="text-gray-900">{value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
