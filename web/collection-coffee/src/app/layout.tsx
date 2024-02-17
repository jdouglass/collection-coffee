import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "./lib/providers/ThemeProvider";
import "./globals.css";
import { TopNav } from "./components/TopNav/TopNav";
import { SpeedInsights } from "@vercel/speed-insights/next";
import { PHProvider } from "./lib/providers/PostHogProvider";
import dynamic from "next/dynamic";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Collection Coffee",
  description: "The one and only aggregator for speciality coffee products",
};

const PostHogPageView = dynamic(
  () => import("./components/PostHogPageView/PostHogPageView"),
  {
    ssr: false,
  }
);

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning lang="en">
      <PHProvider>
        <body>
          <PostHogPageView />
          <ThemeProvider>
            <TopNav />
            {children}
            <SpeedInsights />
          </ThemeProvider>
        </body>
      </PHProvider>
    </html>
  );
}
