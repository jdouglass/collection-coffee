"use client";

import { useState } from "react";
import { FilterBar } from "../FilterBar/FilterBar";
import { FilterUtilityBar } from "../FilterUtilityBar/FilterUtilityBar";
import Products from "../Products/Products";
import { ProductFetchResponse } from "@/app/page";

type HomePageProps = {
  products: ProductFetchResponse;
  lastUpdatedDetails: any;
  searchParams: { [key: string]: string | string[] | undefined };
  getProducts: any;
};

export const HomePage = ({
  products,
  lastUpdatedDetails,
  searchParams,
  getProducts,
}: HomePageProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMobileFilterBar = () => {
    setIsOpen((isOpen) => !isOpen);
  };
  return (
    <>
      <div className="filter-bar__container">
        <FilterBar isOpen={isOpen} />
      </div>
      <div className="products-utility__container">
        <FilterUtilityBar
          lastUpdatedDetails={lastUpdatedDetails}
          totalCount={products.totalCount ? (products.totalCount as number) : 0}
          toggleMobileFilterBar={toggleMobileFilterBar}
        />
        <Products searchParams={searchParams} fetchProducts={getProducts} />
      </div>
    </>
  );
};
