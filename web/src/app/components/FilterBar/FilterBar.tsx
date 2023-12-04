import "./filter-bar.css";
import { filterBarCategories } from "../../lib/data/filterBarCategories";
import { ClearFilterButton } from "../ClearFilterButton/ClearFilterButton";
import FilterIcon from "../../../../public/filterIcon.svg";
import { FilterButton } from "../FilterButton/FilterButton";
import { IReferenceDataResponse } from "@/app/lib/interfaces/IReferenceDataResponse";

async function getReferenceData() {
  const API_BASE_URL = `${process.env.API_BASE_URL}`;
  const res = await fetch(`${API_BASE_URL}/api/v1/reference-data`);
  if (!res.ok) {
    throw new Error("Failed to fetch reference data");
  }
  return res.json();
}

export const FilterBar = async () => {
  const referenceData: IReferenceDataResponse = await getReferenceData();
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
