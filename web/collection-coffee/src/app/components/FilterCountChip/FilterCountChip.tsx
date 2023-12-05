import "./filter-count-chip.css";

interface FilterCountChipProps {
  count: number;
}

export const FilterCountChip = ({ count }: FilterCountChipProps) => {
  return <div className={"filter-count"}>{count}</div>;
};
