"use client";

import useScroll from "@/app/lib/hooks/useScroll";
import SortSelect from "../SortSelect/SortSelect";
import "./filter-utility-bar.css";

export const FilterUtilityBar = (searchParams: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {
  const scrolled = useScroll(10);
  return (
    <div className={`filter-utility-container ${scrolled ? "scrolled" : ""}`}>
      <SortSelect />
    </div>
  );
};
