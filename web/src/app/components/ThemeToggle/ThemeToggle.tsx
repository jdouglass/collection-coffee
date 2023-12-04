"use client";

import { useState, useEffect } from "react";
import { useTheme } from "next-themes";
import SunIcon from "../../../../public/sunIcon.svg";
import MoonIcon from "../../../../public/moonIcon.svg";
import "./theme-toggle.css";

const ThemeToggle = () => {
  const [mounted, setMounted] = useState(false);
  const { resolvedTheme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <>
      {resolvedTheme === "light" ? (
        <MoonIcon className="toggle" onClick={() => setTheme("dark")} />
      ) : (
        <SunIcon className="toggle" onClick={() => setTheme("light")} />
      )}
    </>
  );
};

export default ThemeToggle;
