/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import "./product-card.css";
import { SoldOutChip } from "../SoldOutChip/SoldOutChip";
import { IProductCard } from "@/app/lib/interfaces/IProductCard";

export const ProductCard = (product: IProductCard) => {
  const {
    productSize,
    productPrice,
    isSoldOut,
    title,
    process,
    productUrl,
    imageUrl,
    discoveredDateTime,
    brand,
    country,
    tastingNotes,
    varieties,
    vendor,
  } = product.product;
  return (
    <div className="product-card-container">
      <Link href={productUrl} target="_blank">
        <div className="product-card__image-container">
          {isSoldOut ? (
            <div className="product-sold-out">
              <SoldOutChip />
            </div>
          ) : null}
          <img
            src={imageUrl}
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
        <Link href={productUrl} target="_blank" className="product-card-link">
          <div className="product-card-info-top">
            <div className="product-card-info-top-left">
              <div className="product-card-brand">{brand}</div>
              <div className="product-card-title">{title}</div>
              <div className="product-card-sold-by-info">
                Sold by&nbsp;
                <div className="product-card-sold-by-vendor">{vendor}</div>
              </div>
            </div>
            <div className="product-card-info-top-right">
              <div className="product-card-price">${productPrice}</div>
              <div className="product-card-size">
                for {productSize.split(".")[0]}g
              </div>
            </div>
          </div>
        </Link>
      </div>
      <div className="product-card-info-border" />
      <div className="product-card-info-container">
        <div className="product-card-main-info-container">
          <div className="product-card-main-info-header">Country of Origin</div>
          <div className="product-card-main-info">{country}</div>
          <div className="product-card-main-info-header">Process</div>
          <div className="product-card-main-info">{process}</div>
          <div className="product-card-main-info-header">Variety</div>
          <div className="product-card-main-info">{varieties.join(", ")}</div>
          <div className="product-card-main-info-header">Tasting Notes</div>
          <div className="product-card-main-info">
            {tastingNotes.join(", ")}
          </div>
          <div className="product-card-main-info-header">
            Discovered Date Time UTC
          </div>
          <div className="product-card-main-info">
            {discoveredDateTime.toString().replace("T", " ").split(".")[0]}
          </div>
        </div>
      </div>
    </div>
  );
};
