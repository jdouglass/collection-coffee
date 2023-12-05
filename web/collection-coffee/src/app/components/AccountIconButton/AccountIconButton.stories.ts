import type { Meta, StoryObj } from "@storybook/react";
import AccountIconButton from "./AccountIconButton";

const meta = {
  title: "Example/AccountIconButton",
  component: AccountIconButton,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
} satisfies Meta<typeof AccountIconButton>;

export default meta;
type Story = StoryObj<typeof meta>;

export const AccountIconButtonDark: Story = {};

export const AccountIconButtonLight: Story = {
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
