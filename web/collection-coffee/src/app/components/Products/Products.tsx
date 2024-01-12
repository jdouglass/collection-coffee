"use client";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { ProductCard } from "../ProductCard/ProductCard";
import { IProductResponse } from "@/app/lib/interfaces/IProductResponse";
import { ProductFetchResponse } from "@/app/page";
import LoadingDots from "../LoadingSpinner/LoadingDots";
import "./products.css";

type ProductsProps = {
  searchParams: {
    [key: string]: string | string[] | undefined;
  };
  fetchProducts: (
    searchParams: {
      [key: string]: string | string[] | undefined;
    },
    page: number
  ) => Promise<ProductFetchResponse>;
};

const Products = ({ searchParams, fetchProducts }: ProductsProps) => {
  const [products, setProducts] = useState<IProductResponse[]>([]);
  const [page, setPage] = useState(1);
  const [hasMoreProducts, setHasMoreProducts] = useState(true);
  const loader = useRef(null);
  const isFetching = useRef(false);

  // Memoize loadProducts function
  const loadProducts = useCallback(
    async (currentPage: number) => {
      isFetching.current = true;
      try {
        const newProducts = await fetchProducts(searchParams, currentPage);
        setProducts((prev) =>
          currentPage === 1
            ? newProducts.products
            : [...prev, ...newProducts.products]
        );
        setHasMoreProducts(newProducts.products.length === 12); // Assuming 12 is your pagination size
        if (newProducts.products.length > 0) {
          setPage(currentPage + 1);
        }
      } catch (error) {
        console.error(error);
      } finally {
        isFetching.current = false;
      }
    },
    [fetchProducts, searchParams]
  );

  useEffect(() => {
    setProducts([]);
    loadProducts(1);
  }, [loadProducts]);

  useEffect(() => {
    const currentLoader = loader.current;
    const observer = new IntersectionObserver(
      (entries) => {
        if (
          entries[0].isIntersecting &&
          !isFetching.current &&
          hasMoreProducts
        ) {
          loadProducts(page); // Load next page of products
        }
      },
      { threshold: 1.0 }
    );

    if (currentLoader) {
      observer.observe(currentLoader);
    }

    return () => {
      if (currentLoader) {
        observer.unobserve(currentLoader);
      }
    };
  }, [loadProducts, page, hasMoreProducts]); // Removed unnecessary dependencies

  return (
    <div className="products-with-loading">
      <div className="products__container">
        {products.map((product) => (
          <ProductCard
            key={
              product.productId +
              product.variantId +
              product.productPrice +
              product.productSize +
              product.productHandle
            }
            product={product}
          />
        ))}
      </div>
      {hasMoreProducts && (
        <div ref={loader} className="loading-indicator">
          <LoadingDots />
        </div>
      )}
      {!hasMoreProducts && products.length > 0 && (
        <div className="end-of-results-message">End of results</div>
      )}
      {!hasMoreProducts && !products.length && (
        <div className="no-results-message">No results found</div>
      )}
    </div>
  );
};

export default Products;
