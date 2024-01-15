"use client";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { ProductCard } from "../ProductCard/ProductCard";
import { IProductResponse } from "@/app/lib/interfaces/IProductResponse";
import { ProductFetchResponse } from "@/app/page";
import LoadingDots from "../LoadingSpinner/LoadingDots";
import "./products.css";

type ProductsProps = {
  initialProducts: IProductResponse[];
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

const Products = ({
  initialProducts,
  searchParams,
  fetchProducts,
}: ProductsProps) => {
  const [products, setProducts] = useState<IProductResponse[]>(initialProducts);
  const [page, setPage] = useState(2);
  const [hasMoreProducts, setHasMoreProducts] = useState(true);
  const loader = useRef(null);
  const isFetching = useRef(false);

  console.log(hasMoreProducts);
  console.log(page);

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
        setHasMoreProducts(newProducts.products.length === 12);
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

  const loadMoreProducts = useCallback(() => {
    if (hasMoreProducts && !isFetching.current) {
      loadProducts(page);
    }
  }, [hasMoreProducts, page, loadProducts]);

  useEffect(() => {
    const currentLoader = loader.current;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMoreProducts();
        }
      },
      { threshold: 0.1 }
    );

    if (currentLoader) {
      observer.observe(currentLoader);
    }

    return () => {
      if (currentLoader) {
        observer.unobserve(currentLoader);
      }
    };
  }, [loadMoreProducts]);

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
