import type { Meta, StoryObj } from "@storybook/react";

import { FilterCountChip } from "./FilterCountChip";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/FilterCountChip",
  component: FilterCountChip,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof FilterCountChip>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {
  args: {
    count: 20,
  },
};

export const Secondary: Story = {
  args: {
    count: 20,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {
  args: {
    count: 20,
  },
};

export const SecondaryActive: Story = {
  args: {
    count: 20,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
