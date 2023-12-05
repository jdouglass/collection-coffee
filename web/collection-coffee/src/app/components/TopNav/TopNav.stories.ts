import type { Meta, StoryObj } from "@storybook/react";
import { TopNav } from "./TopNav";

const meta = {
  title: "Example/TopNav",
  component: TopNav,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/react/configure/story-layout
    layout: "fullscreen",
  },
} satisfies Meta<typeof TopNav>;

export default meta;
type Story = StoryObj<typeof meta>;

export const TopNavPrimary: Story = {};

export const TopNavSecondary: Story = {
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
