"use client";
import { useState } from "react";
import { FilterBar } from "../FilterBar/FilterBar";
import { FilterUtilityBar } from "../FilterUtilityBar/FilterUtilityBar";
import { ProductFetchResponse } from "@/app/page";
import { IReferenceDataResponse } from "@/app/lib/interfaces/IReferenceDataResponse";
import { ILastUpdatedResponse } from "@/app/lib/interfaces/ILastUpdatedResponse";
import Products from "../Products/Products";

type HomePageProps = {
  initialProducts: ProductFetchResponse;
  lastUpdatedDetails: ILastUpdatedResponse;
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
  initialProducts,
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
        <FilterBar
          referenceData={referenceData}
          isFilterBarOpen={isOpen}
          toggleMobileFilterBar={toggleMobileFilterBar}
        />
      </div>
      <div className="products-utility__container">
        <FilterUtilityBar
          lastUpdatedDetails={lastUpdatedDetails}
          totalCount={
            initialProducts.totalCount
              ? (initialProducts.totalCount as number)
              : 0
          }
          toggleMobileFilterBar={toggleMobileFilterBar}
        />
        <Products
          initialProducts={initialProducts.products}
          searchParams={searchParams}
          fetchProducts={getProducts}
        />
      </div>
    </>
  );
};
