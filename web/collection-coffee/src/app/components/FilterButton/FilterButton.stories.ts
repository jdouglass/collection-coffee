import type { Meta, StoryObj } from "@storybook/react";

import { FilterButton } from "./FilterButton";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/FilterButton",
  component: FilterButton,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof FilterButton>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {
  args: {
    label: "FilterButton",
    filterValues: ["foo", "bar"],
  },
};

export const Secondary: Story = {
  args: {
    label: "FilterButton",
    filterValues: ["foo", "bar"],
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {
  args: {
    label: "FilterButton",
    filterValues: ["foo", "bar"],
  },
};

export const SecondaryActive: Story = {
  args: {
    label: "FilterButton",
    filterValues: ["foo", "bar"],
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
