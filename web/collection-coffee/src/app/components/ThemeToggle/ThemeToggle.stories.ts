import type { Meta, StoryObj } from "@storybook/react";
import ThemeToggle from "./ThemeToggle";
import SunIcon from "../../../../public/sunIcon.svg";
import MoonIcon from "../../../../public/moonIcon.svg";

const meta = {
  title: "Example/ThemeToggle",
  component: ThemeToggle,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/react/writing-docs/autodocs
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/react/configure/story-layout
    layout: "centered",
  },
} satisfies Meta<typeof ThemeToggle>;

export default meta;
type Story = StoryObj<typeof meta>;

export const ThemeToggleDark: Story = {};

export const ThemeToggleLight: Story = {
  parameters: {
    backgrounds: {
      default: "dark",
    },
  },
};
