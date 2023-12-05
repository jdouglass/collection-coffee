import type { Meta, StoryObj } from "@storybook/react";

import { NavButton } from "./NavButton";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/NavButton",
  component: NavButton,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof NavButton>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {
  args: {
    href: "/",
    label: "NavButton",
    isActive: false,
  },
};

export const Secondary: Story = {
  args: {
    href: "/",
    label: "NavButton",
    isActive: false,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {
  args: {
    href: "/",
    label: "NavButton",
    isActive: true,
  },
};

export const SecondaryActive: Story = {
  args: {
    href: "/",
    label: "NavButton",
    isActive: true,
  },
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
