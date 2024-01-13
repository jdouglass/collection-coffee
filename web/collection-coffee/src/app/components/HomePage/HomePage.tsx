"use client";
import { useState } from "react";
import { FilterBar } from "../FilterBar/FilterBar";
import { FilterUtilityBar } from "../FilterUtilityBar/FilterUtilityBar";
import Products from "../Products/Products";
import { ProductFetchResponse } from "@/app/page";
import { IReferenceDataResponse } from "@/app/lib/interfaces/IReferenceDataResponse";

type HomePageProps = {
  products: ProductFetchResponse;
  lastUpdatedDetails: any;
  searchParams: { [key: string]: string | string[] | undefined };
  getProducts: (
    searchParams: {
      [key: string]: string | string[] | undefined;
    },
    page?: number
  ) => Promise<ProductFetchResponse>;
  referenceData: IReferenceDataResponse;
};

export const HomePage = ({
  products,
  lastUpdatedDetails,
  searchParams,
  getProducts,
  referenceData,
}: HomePageProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const toggleMobileFilterBar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <div className="filter-bar__container">
        <FilterBar referenceData={referenceData} />
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
