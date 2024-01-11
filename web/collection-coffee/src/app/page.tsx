import { FilterBar } from "./components/FilterBar/FilterBar";
import { FilterUtilityBar } from "./components/FilterUtilityBar/FilterUtilityBar";
import { ProductCard } from "./components/ProductCard/ProductCard";
import "./page.css";

async function getProducts(searchParams: {
  [key: string]: string | string[] | undefined;
}) {
  const params = new URLSearchParams();

  for (const key in searchParams) {
    const value = searchParams[key];
    if (Array.isArray(value)) {
      // Handle array values by appending each element separately
      value.forEach((element) => params.append(key, element));
    } else if (value) {
      // Handle string values
      params.append(key, value);
    }
  }
  const res = await fetch(
    `${process.env.API_BASE_URL}/api/v1/all-products?${params.toString()}`,
    { next: { revalidate: 60 } }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }

  return res.json();
}

async function getLastUpdatedDetails() {
  const res = await fetch(`${process.env.API_BASE_URL}/api/v1/last-updated`, {
    next: { revalidate: 60 },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }

  return res.json();
}

const Home = async ({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {
  const products = await getProducts(searchParams);
  const lastUpdatedDetails = await getLastUpdatedDetails();

  return (
    <main className="home-container">
      <div className="filter-bar__container">
        <FilterBar />
      </div>
      <div className="products-utility__container">
        <FilterUtilityBar
          searchParams={searchParams}
          lastUpdatedDetails={lastUpdatedDetails}
          totalCount={products.totalCount ? (products.totalCount as number) : 0}
        />
        <div className="products__container">
          {products.products &&
            products.products.map((product: any) => {
              return <ProductCard product={product} key={product.productId} />;
            })}
        </div>
      </div>
    </main>
  );
};

export default Home;
