import { HomePage } from "./components/HomePage/HomePage";
import { ILastUpdatedResponse } from "./lib/interfaces/ILastUpdatedResponse";
import { IProductResponse } from "./lib/interfaces/IProductResponse";
import { IReferenceDataResponse } from "./lib/interfaces/IReferenceDataResponse";
import "./page.css";

export interface ProductFetchResponse {
  products: IProductResponse[];
  totalCount: number;
}

async function getReferenceData(): Promise<IReferenceDataResponse> {
  try {
    const res = await fetch(
      `${process.env.API_BASE_URL}/api/v1/reference-data`,
      { cache: "no-store" }
    );
    if (!res.ok) {
      throw new Error("Failed to fetch reference data");
    }
    return res.json();
  } catch (error) {
    console.error(error);
    return {
      brands: [""],
      vendors: [""],
      tastingNotes: [""],
      varieties: [""],
      continents: [""],
      countries: [""],
      processCategories: [""],
    };
  }
}

async function getProducts(
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
  try {
    const res = await fetch(
      `${process.env.API_BASE_URL}/api/v1/products?${params.toString()}${
        params.toString() !== "" ? "&" : ""
      }${page ? `page=${page}` : ""}`,
      { cache: "no-store" }
    );

    if (!res.ok) {
      throw new Error("Failed to fetch products");
    }

    return res.json();
  } catch (error) {
    console.error(error);
    return { products: [], totalCount: 0 };
  }
}

async function getLastUpdatedDetails(): Promise<ILastUpdatedResponse> {
  try {
    const res = await fetch(`${process.env.API_BASE_URL}/api/v1/last-updated`, {
      cache: "no-store",
    });

    if (!res.ok) {
      throw new Error("Failed to fetch products");
    }

    return res.json();
  } catch (error) {
    console.error(error);
    return {
      lastUpdatedDateTime: new Date(),
      isScraperRunning: false,
    };
  }
}

const Home = async ({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {
  const products = await getProducts(searchParams);
  const lastUpdatedDetails = await getLastUpdatedDetails();
  const referenceData = await getReferenceData();

  return (
    <main className="home-container">
      <HomePage
        initialProducts={products}
        lastUpdatedDetails={lastUpdatedDetails}
        searchParams={searchParams}
        getProducts={getProducts}
        referenceData={referenceData}
      />
    </main>
  );
};

export default Home;
