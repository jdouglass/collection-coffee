import { FilterBar } from "./components/FilterBar/FilterBar";
import { ProductCard } from "./components/ProductCard/ProductCard";
import { IProductResponse } from "./lib/interfaces/IProductResponse";
import "./page.css";

async function getProducts() {
  const API_BASE_URL = `${process.env.API_BASE_URL}`;
  const res = await fetch(`${API_BASE_URL}/api/v1/all-products`);
  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }
  return res.json();
}

export default async function Home() {
  const products: IProductResponse[] = await getProducts();
  return (
    <main className="home-container">
      <div className="filter-bar__container">
        <FilterBar />
      </div>
      <div className="products__container">
        {products &&
          products.map((product) => {
            return <ProductCard product={product} key={product.productId} />;
          })}
      </div>
    </main>
  );
}
