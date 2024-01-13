import { FilterBar } from "./components/FilterBar/FilterBar";
import { FilterUtilityBar } from "./components/FilterUtilityBar/FilterUtilityBar";
import Products from "./components/Products/Products";
import { IProductResponse } from "./lib/interfaces/IProductResponse";
import "./page.css";

export interface ProductFetchResponse {
  products: IProductResponse[];
  totalCount: number;
}

export async function getProducts(
  searchParams: {
    [key: string]: string | string[] | undefined;
  },
  page = 1
): Promise<ProductFetchResponse> {
  "use server";
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
    `${process.env.API_BASE_URL}/api/v1/products?${params.toString()}${
      params.toString() !== "" ? "&" : ""
    }${page ? `page=${page}` : ""}`,
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
          lastUpdatedDetails={lastUpdatedDetails}
          totalCount={products.totalCount ? (products.totalCount as number) : 0}
        />
        <Products searchParams={searchParams} fetchProducts={getProducts} />
      </div>
    </main>
  );
};

export default Home;
