"use client";

import { useRouter, useSearchParams } from "next/navigation";
import "./clear-filter-button.css";

export const ClearFilterButton = () => {
  const searchParams = useSearchParams();
  const router = useRouter();

  return (
    <button
      className="clear-filter-button"
      disabled={!searchParams.toString().length}
      onClick={() => router.push("/")}
    >
      Clear Filters
    </button>
  );
};
