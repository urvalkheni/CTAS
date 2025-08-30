import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class", // enable dark mode with class strategy
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#2563eb", // blue-600
          light: "#3b82f6",   // blue-500
          dark: "#1e40af",    // blue-800
        },
        cyan: {
          DEFAULT: "#06b6d4", // cyan-500
          light: "#22d3ee",
          dark: "#0891b2",
        },
        background: {
          light: "#ffffff",
          dark: "#0f172a", // slate-900
        },
        foreground: {
          light: "#0f172a", // dark text for light mode
          dark: "#f8fafc", // light text for dark mode
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        heading: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
