"use client";

import "./filter-button.css";
import ExpandMoreArrowIcon from "../../../../public/expandMoreArrow.svg";
import { useState, useEffect } from "react";
import { FilterCheckbox } from "../FilterCheckbox/FilterCheckbox";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { FilterCountChip } from "../FilterCountChip/FilterCountChip";

interface FilterButtonProps {
  label: string;
  filterValues: string[];
}

export const FilterButton = ({
  label,
  filterValues,
  ...props
}: FilterButtonProps) => {
  const router = useRouter();
  const pathname = usePathname() as string;
  const formattedCategory = label.toLowerCase().replaceAll(" ", "_");
  const searchParams = useSearchParams();
  const params = new URLSearchParams(searchParams!.toString());
  const [checkedCount, setCheckedCount] = useState<number>(
    params.getAll(formattedCategory).length
  );
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (!searchParams!.toString().length) {
      setCheckedCount(0);
    }
  }, [searchParams]);

  const handleSelectedChange = (e: any) => {
    if (!params.getAll(formattedCategory).includes(e.target.value)) {
      params.append(formattedCategory, e.target.value);
      setCheckedCount(checkedCount + 1);
    } else {
      const options = params
        .getAll(formattedCategory)
        .filter((value) => value !== e.target.value);
      params.delete(formattedCategory);
      for (const option of options) params.append(formattedCategory, option);
      setCheckedCount(params.getAll(formattedCategory).length);
    }
    router.push(`${pathname}?${params.toString()}`);
    setCheckedCount(params.getAll(formattedCategory).length);
  };

  return (
    <div className="filter-checkbox-options">
      <button
        className={"filter-button"}
        {...props}
        onClick={() => setExpanded(!expanded)}
      >
        {label}
        <div className="filter-button-right">
          {checkedCount ? <FilterCountChip count={checkedCount} /> : undefined}
          <ExpandMoreArrowIcon
            className={`expand-more-icon ${expanded ? "opened" : "closed"}`}
          />
        </div>
      </button>
      {expanded && (
        <div className="filter-options">
          {filterValues.map((option) => {
            return (
              <FilterCheckbox
                key={`${label}-${option}`}
                filterCategory={label}
                label={option}
                onChange={handleSelectedChange}
              />
            );
          })}
        </div>
      )}
    </div>
  );
};
