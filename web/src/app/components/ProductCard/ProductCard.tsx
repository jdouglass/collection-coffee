import Link from "next/link";
import "./product-card.css";
import { IProductResponse } from "@/app/lib/interfaces/IProductResponse";
import Image from "next/image";
import { SoldOutChip } from "../SoldOutChip/SoldOutChip";

export const ProductCard = ({
  productId,
  variantId,
  productSize,
  productPrice,
  isSoldOut,
  title,
  process,
  productUrl,
  imageUrl,
  discoveredDateTime,
  productHandle,
  isDecaf,
  brand,
  continent,
  country,
  processCategory,
  tastingNotes,
  varieties,
  vendor,
}: IProductResponse) => {
  return (
    <div className="product-card-container">
      <Link href={productUrl} target="_blank">
        <div className="product-card">
          {isSoldOut ? (
            <div className="product-sold-out">
              <SoldOutChip />
            </div>
          ) : null}
          <Image
            src={imageUrl}
            height={260}
            width={300}
            blurDataURL={imageUrl}
            placeholder="blur"
            alt={`${brand} ${title} coffee beans`}
            className={`product-card-image ${
              brand === "Monogram" ||
              brand === "Manhattan" ||
              vendor === "Pallet Coffee Roasters"
                ? "object-contain"
                : "object-cover"
            }`}
          />
        </div>
      </Link>
      <div className="product-card-info-container">
        <p className="product-card-sold-by-info">Sold by {vendor}</p>
        <div className=""></div>
      </div>
    </div>
  );
};
