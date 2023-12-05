import type { Preview } from "@storybook/react";
import { themes } from "@storybook/theming";
import "../src/app/globals.css";

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    darkMode: {
      dark: { ...themes.dark, appBg: "#121212" },
      light: { ...themes.normal, appBg: "white" },
      current: "light",
      darkClass: "lights-out",
      lightClass: "lights-on",
      stylePreview: true,
    },
  },
};

export default preview;
