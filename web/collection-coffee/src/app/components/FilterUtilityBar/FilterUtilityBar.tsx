"use client";

import useScroll from "@/app/lib/hooks/useScroll";
import SortSelect from "../SortSelect/SortSelect";
import "./filter-utility-bar.css";
import ProductResultsCount from "../ProductResultsCount/ProductResultsCount";
import LastUpdatedDetails from "../LastUpdatedDetails/LastUpdatedDetails";
import FilterIcon from "../../../../public/filterAltIcon.svg";
import { ILastUpdatedResponse } from "@/app/lib/interfaces/ILastUpdatedResponse";

type FilterUtilityBarProps = {
  lastUpdatedDetails: ILastUpdatedResponse;
  totalCount: number;
  toggleMobileFilterBar: () => void;
};

export const FilterUtilityBar = ({
  lastUpdatedDetails,
  totalCount,
  toggleMobileFilterBar,
}: FilterUtilityBarProps) => {
  const scrolled = useScroll(10);
  return (
    <div className={`filter-utility-container ${scrolled ? "scrolled" : ""}`}>
      <div className="sort-select-section">
        <SortSelect />
      </div>
      <div className="mobile-filter-toggle" onClick={toggleMobileFilterBar}>
        <div className="mobile-filter-icon">
          <FilterIcon />
        </div>
        <div>Product Filters</div>
      </div>
      <div className="last-updated-details-section">
        <LastUpdatedDetails {...lastUpdatedDetails} />
      </div>
      <div className="product-results-count-section">
        <ProductResultsCount totalCount={totalCount ? totalCount : 0} />
      </div>
      <div className="combined-filter-utility-data">
        <ProductResultsCount totalCount={totalCount ? totalCount : 0} />
        <div className="smaller-last-updated-details-section">
          <LastUpdatedDetails {...lastUpdatedDetails} />
        </div>
      </div>
    </div>
  );
};
