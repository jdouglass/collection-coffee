import "./product-results-count.css";

type ProductResultsCountProps = {
  totalCount: number;
};

const ProductResultsCount = ({ totalCount }: ProductResultsCountProps) => {
  return (
    <div className="product-results-count">
      <div className="product-results-count-value">{totalCount}</div>
      &nbsp;products found
    </div>
  );
};

export default ProductResultsCount;
