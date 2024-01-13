import "./filter-bar.css";
import { filterBarCategories } from "../../lib/data/filterBarCategories";
import { ClearFilterButton } from "../ClearFilterButton/ClearFilterButton";
import FilterIcon from "../../../../public/filterIcon.svg";
import { FilterButton } from "../FilterButton/FilterButton";
import { IReferenceDataResponse } from "@/app/lib/interfaces/IReferenceDataResponse";

type FilterBarProps = {
  referenceData: IReferenceDataResponse;
};

export const FilterBar = ({ referenceData }: FilterBarProps) => {
  return (
    <div className="filter-bar scrollbar">
      <div className="filter-bar-header">
        <div className="filter-bar-title">
          <FilterIcon className="filter-bar-icon" />
          <h1>Filters</h1>
        </div>
        <ClearFilterButton />
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
  );
};
