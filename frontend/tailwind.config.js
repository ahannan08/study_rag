/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          50: "#f4f6fb",
          100: "#e8ecf6",
          200: "#cdd7ea",
          300: "#a3b4d9",
          400: "#7289c4",
          500: "#5069ad",
          600: "#3d5391",
          700: "#334476",
          800: "#2d3a62",
          900: "#293352",
          950: "#1a2135",
        },
        accent: {
          DEFAULT: "#6366f1",
          soft: "#818cf8",
          muted: "#c7d2fe",
        },
      },
      fontFamily: {
        sans: ["\"DM Sans\"", "system-ui", "sans-serif"],
        display: ["\"Fraunces\"", "Georgia", "serif"],
      },
      boxShadow: {
        card: "0 4px 24px -4px rgba(26, 33, 53, 0.12)",
        glow: "0 0 40px -10px rgba(99, 102, 241, 0.35)",
      },
    },
  },
  plugins: [],
};
