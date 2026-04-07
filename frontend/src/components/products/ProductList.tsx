/**
 * Product list component.
 *
 * Displays a grid of product cards.
 */

import React from 'react';
import type { Product } from '../../types';
import { ProductCard } from './ProductCard';

interface ProductListProps {
  products: Product[];
}

export const ProductList: React.FC<ProductListProps> = ({ products }) => {
  if (products.length === 0) {
    return null;
  }

  return (
    <div className="my-5">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">
        {products.length} Product{products.length !== 1 ? 's' : ''} Found
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((product, index) => (
          <ProductCard key={product.id} product={product} index={index} />
        ))}
      </div>
    </div>
  );
};
