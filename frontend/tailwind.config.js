/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette: gray, black, white, dark green only
        green: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',   // green-600 (acceptable light green)
          700: '#15803d',   // green-700 (medium green)
          800: '#166534',   // green-800
          900: '#14532d',   // green-900 (dark green - primary)
          950: '#052e16',   // green-950 (very dark green)
        },
      },
      boxShadow: {
        'custom': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'custom-md': '0 4px 12px rgba(0, 0, 0, 0.15)',
        'custom-lg': '0 8px 24px rgba(0, 0, 0, 0.2)',
      },
      borderWidth: {
        '3': '3px',
      },
    },
  },
  plugins: [],
}
