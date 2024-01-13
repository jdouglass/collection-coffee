"use client";

import "./filter-bar.css";
import { filterBarCategories } from "../../lib/data/filterBarCategories";
import { ClearFilterButton } from "../ClearFilterButton/ClearFilterButton";
import FilterIcon from "../../../../public/filterIcon.svg";
import { FilterButton } from "../FilterButton/FilterButton";
import { IReferenceDataResponse } from "@/app/lib/interfaces/IReferenceDataResponse";
import ExitIcon from "../../../../public/exitIcon.svg";
import SortSelect from "../SortSelect/SortSelect";
import { useEffect, useRef } from "react";

type FilterBarProps = {
  referenceData: IReferenceDataResponse;
  isFilterBarOpen: boolean;
  toggleMobileFilterBar: () => void;
};

export const FilterBar = ({
  referenceData,
  isFilterBarOpen,
  toggleMobileFilterBar,
}: FilterBarProps) => {
  const filterBarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: { target: any }) => {
      if (
        filterBarRef.current &&
        !filterBarRef.current.contains(event.target)
      ) {
        toggleMobileFilterBar();
      }
    };

    if (isFilterBarOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isFilterBarOpen, toggleMobileFilterBar]);
  return (
    <>
      {isFilterBarOpen && <div className="overlay"></div>}
      <div
        className={`filter-bar scrollbar ${isFilterBarOpen ? "isOpen" : ""}`}
        ref={filterBarRef}
      >
        <div className="filter-bar-header">
          <div className="filter-bar-title">
            <FilterIcon className="filter-bar-icon" />
            <h1>Filters</h1>
          </div>
          <ClearFilterButton />
          <button
            type="button"
            onClick={toggleMobileFilterBar}
            className="mobile-filter-exit-button"
          >
            <ExitIcon />
          </button>
        </div>
        <div
          className={`mobile-sort-select ${
            isFilterBarOpen ? "mobile-sort-select-open" : ""
          }`}
        >
          <SortSelect />
        </div>
        {filterBarCategories.map((filterCategory) => (
          <FilterButton
            key={filterCategory.category}
            label={filterCategory.category}
            filterValues={
              referenceData[
                filterCategory.referenceDataKey as keyof typeof referenceData
              ]
            }
          />
        ))}
      </div>
    </>
  );
};
