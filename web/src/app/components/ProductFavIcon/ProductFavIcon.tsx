import "./product-fav-icon.css";
import HeartIcon from "../../../../public/heartIcon.svg";

interface ProductFavIconProps {
  isFavourited: boolean;
}

export const ProductFavIcon = ({ isFavourited }: ProductFavIconProps) => {
  return (
    <button className="product-fav-button">
      <HeartIcon
        className={`product-fav-icon ${isFavourited ? "favourited" : ""}`}
      />
    </button>
  );
};
