"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import "./sort-select.css";

const SortSelect = () => {
  const searchParams = useSearchParams();
  const params = new URLSearchParams(searchParams!.toString());
  const router = useRouter();
  const pathname = usePathname();
  const sortOptions = [
    { value: "newest", label: "Newest to Oldest" },
    { value: "oldest", label: "Oldest to Newest" },
    { value: "ascending", label: "Price Ascending" },
    { value: "descending", label: "Price Descending" },
  ];

  const handleSort = (e: any) => {
    params.delete("sort");
    params.append("sort", e.currentTarget.value);
    router.push(`${pathname}?${params.toString()}`);
  };

  return (
    <form className="sort-container">
      <label htmlFor="sort" className="sort-label">
        Sort by
      </label>
      <select
        name="sort"
        id="sort"
        value={params.get("sort") ? (params.get("sort") as string) : ""}
        onChange={(e) => handleSort(e)}
        className="sort-select"
      >
        {sortOptions.map((sortOption) => {
          return (
            <option key={sortOption.value} value={sortOption.value}>
              {sortOption.label}
            </option>
          );
        })}
      </select>
    </form>
  );
};

export default SortSelect;
