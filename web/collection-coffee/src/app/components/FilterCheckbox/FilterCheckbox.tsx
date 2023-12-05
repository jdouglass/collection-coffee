"use client";

import { useSearchParams } from "next/navigation";
import "./filter-checkbox.css";

interface FilterCheckboxProps {
  filterCategory: string;
  label: string;
  onChange: any;
}

export const FilterCheckbox = ({
  filterCategory,
  label,
  onChange,
}: FilterCheckboxProps) => {
  const formattedCategory = filterCategory.toLowerCase().replaceAll(" ", "_");
  const searchParams = useSearchParams();
  const params = new URLSearchParams(searchParams!.toString());
  const lowercaseLabel = label.toLowerCase().replaceAll(" ", "-");

  return (
    <span className="filter-option" key={lowercaseLabel}>
      <input
        key={`${formattedCategory}-${lowercaseLabel}-checkbox`}
        type="checkbox"
        id={`${formattedCategory}-${lowercaseLabel}-checkbox`}
        name={label}
        className="filter-checkbox"
        checked={params.getAll(formattedCategory).includes(label)}
        onChange={(e) => onChange(e)}
        value={label}
      />
      <div className="filter-info">
        <label
          className="filter-label"
          key={`${formattedCategory}-${lowercaseLabel}-lowercaseLabel`}
          htmlFor={`${formattedCategory}-${lowercaseLabel}-checkbox`}
        >
          {label}
        </label>
      </div>
    </span>
  );
};
