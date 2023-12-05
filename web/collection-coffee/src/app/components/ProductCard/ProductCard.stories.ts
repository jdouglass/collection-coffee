import type { Meta, StoryObj } from "@storybook/react";

import { ProductCard } from "./ProductCard";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/ProductCard",
  component: ProductCard,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof ProductCard>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {
  args: {
    productId: 1,
    variantId: 100,
    productSize: "250",
    productPrice: "25.00",
    isSoldOut: false,
    title: "Milkshake Espresso",
    process: "Washed",
    productUrl: "https://google.com",
    imageUrl:
      "https://september.coffee/cdn/shop/files/candycane.jpg?v=1701385006&width=700",
    discoveredDateTime: new Date("2023-10-17 14:59:44"),
    productHandle: "milkshake-espresso",
    isDecaf: false,
    brand: "Traffic Coffee",
    continent: "South America",
    country: "Colombia",
    processCategory: "Washed",
    tastingNotes: [
      "Apricot",
      "Pink Grapefruit",
      "Raspberry",
      "Peach",
      "Elderflowers",
    ],
    varieties: ["Typica", "Caturra", "Castillo", "Colombia", "Catimor"],
    vendor: "Traffic Coffee",
  },
};

export const Secondary: Story = {
  args: {
    productId: 1,
    variantId: 100,
    productSize: "250",
    productPrice: "25.00",
    isSoldOut: false,
    title: "Milkshake Espresso",
    process: "Washed",
    productUrl: "https://google.com",
    imageUrl:
      "https://september.coffee/cdn/shop/files/candycane.jpg?v=1701385006&width=700",
    discoveredDateTime: new Date("2023-10-17 14:59:44"),
    productHandle: "milkshake-espresso",
    isDecaf: false,
    brand: "Traffic Coffee",
    continent: "South America",
    country: "Colombia",
    processCategory: "Washed",
    tastingNotes: [
      "Apricot",
      "Pink Grapefruit",
      "Raspberry",
      "Peach",
      "Elderflowers",
    ],
    varieties: ["Typica", "Caturra", "Castillo", "Colombia", "Catimor"],
    vendor: "Traffic Coffee",
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {
  args: {
    productId: 1,
    variantId: 100,
    productSize: "250",
    productPrice: "25.00",
    isSoldOut: false,
    title: "Milkshake Espresso",
    process: "Washed",
    productUrl: "https://google.com",
    imageUrl:
      "https://september.coffee/cdn/shop/files/candycane.jpg?v=1701385006&width=700",
    discoveredDateTime: new Date("2023-10-17 14:59:44"),
    productHandle: "milkshake-espresso",
    isDecaf: false,
    brand: "Traffic Coffee",
    continent: "South America",
    country: "Colombia",
    processCategory: "Washed",
    tastingNotes: [
      "Apricot",
      "Pink Grapefruit",
      "Raspberry",
      "Peach",
      "Elderflowers",
    ],
    varieties: ["Typica", "Caturra", "Castillo", "Colombia", "Catimor"],
    vendor: "Traffic Coffee",
  },
};

export const SecondaryActive: Story = {
  args: {
    productId: 1,
    variantId: 100,
    productSize: "250",
    productPrice: "25.00",
    isSoldOut: false,
    title: "Milkshake Espresso",
    process: "Washed",
    productUrl: "https://google.com",
    imageUrl:
      "https://september.coffee/cdn/shop/files/candycane.jpg?v=1701385006&width=700",
    discoveredDateTime: new Date("2023-10-17 14:59:44"),
    productHandle: "milkshake-espresso",
    isDecaf: false,
    brand: "Traffic Coffee",
    continent: "South America",
    country: "Colombia",
    processCategory: "Washed",
    tastingNotes: [
      "Apricot",
      "Pink Grapefruit",
      "Raspberry",
      "Peach",
      "Elderflowers",
    ],
    varieties: ["Typica", "Caturra", "Castillo", "Colombia", "Catimor"],
    vendor: "Traffic Coffee",
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
