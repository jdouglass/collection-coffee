import type { Meta, StoryObj } from "@storybook/react";

import SignUpForm from "./SignUpForm";

// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
const meta = {
  title: "Example/SignUpForm",
  component: SignUpForm,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
} satisfies Meta<typeof SignUpForm>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/react/writing-stories/args
export const Primary: Story = {};

export const Secondary: Story = {
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};

export const PrimaryActive: Story = {};

export const SecondaryActive: Story = {
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
