export interface IProductResponse {
  productId: number;
  variantId: number;
  productSize: string;
  productPrice: string;
  isSoldOut: boolean;
  title: string;
  process: string;
  productUrl: string;
  imageUrl: string;
  discoveredDateTime: Date;
  productHandle: string;
  isDecaf: boolean;
  brand: string;
  continent: string;
  country: string;
  processCategory: string;
  tastingNotes: string[];
  varieties: string[];
  vendor: string;
}
