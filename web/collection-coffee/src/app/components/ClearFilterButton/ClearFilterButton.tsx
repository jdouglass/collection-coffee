"use client";

import { useRouter, useSearchParams } from "next/navigation";
import "./clear-filter-button.css";

export const ClearFilterButton = () => {
  const readOnlySearchParams = useSearchParams();
  const searchParams = new URLSearchParams();
  const router = useRouter();

  const clearFilters = () => {
    searchParams.delete(searchParams.toString());
    router.push("/");
  };

  return (
    <button
      className="clear-filter-button"
      disabled={!readOnlySearchParams.toString().length}
      onClick={clearFilters}
    >
      Clear Filters
    </button>
  );
};
