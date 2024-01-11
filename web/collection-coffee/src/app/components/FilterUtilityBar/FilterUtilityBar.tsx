"use client";

import useScroll from "@/app/lib/hooks/useScroll";
import SortSelect from "../SortSelect/SortSelect";
import "./filter-utility-bar.css";
import ProductResultsCount from "../ProductResultsCount/ProductResultsCount";
import LastUpdatedDetails from "../LastUpdatedDetails/LastUpdatedDetails";

type FilterUtilityBarProps = {
  searchParams: { [key: string]: string | string[] | undefined };
  lastUpdatedDetails: { lastUpdatedDateTime: Date; isScraperRunning: boolean };
  totalCount: number;
};

export const FilterUtilityBar = ({
  searchParams,
  lastUpdatedDetails,
  totalCount,
}: FilterUtilityBarProps) => {
  const scrolled = useScroll(10);
  return (
    <div className={`filter-utility-container ${scrolled ? "scrolled" : ""}`}>
      <SortSelect />
      <LastUpdatedDetails {...lastUpdatedDetails} />
      <ProductResultsCount totalCount={totalCount ? totalCount : 0} />
    </div>
  );
};
