import type { Meta, StoryObj } from "@storybook/react";

import { ProductFavIcon } from "./ProductFavIcon";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/ProductFavIcon",
  component: ProductFavIcon,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof ProductFavIcon>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {
  args: {
    isFavourited: false,
  },
};

export const Secondary: Story = {
  args: {
    isFavourited: false,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {
  args: {
    isFavourited: true,
  },
};

export const SecondaryActive: Story = {
  args: {
    isFavourited: true,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
