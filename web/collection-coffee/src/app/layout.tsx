import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "./lib/providers/ThemeProvider";
import "./globals.css";
import { TopNav } from "./components/TopNav/TopNav";
import { SpeedInsights } from "@vercel/speed-insights/next";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Collection Coffee",
  description: "The one and only aggregator for speciality coffee products",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning lang="en">
      <body>
        <ThemeProvider>
          <TopNav />
          {children}
          <SpeedInsights />
        </ThemeProvider>
      </body>
    </html>
  );
}
