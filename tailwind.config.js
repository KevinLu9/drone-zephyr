import daisyui from "daisyui";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: [
      // "dark",
      {
        drone: {
          primary: "#78C3E3",
          secondary: "#1D3557",
          accent: "#90B693",
          neutral: "#0F1C2E",
          "base-100": "#05090F",
        },
      },
    ],
  },
};
