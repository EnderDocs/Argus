/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        argus: {
          blue: {
            50: '#eff6ff',
            100: '#dbeafe',
            500: '#3b82f6',
            600: '#2563eb',
            700: '#1d4ed8',
            800: '#1e40af',
            900: '#1e3a8a',
            950: '#0f172a',
          },
          orange: {
            400: '#fb923c',
            500: '#f97316',
            600: '#ea580c',
          },
          dark: {
            bg: '#0a0f1d',
            surface: 'rgba(15, 23, 42, 0.75)',
            border: 'rgba(255, 255, 255, 0.1)',
          }
        }
      },
      backdropBlur: {
        glass: '16px',
      }
    },
  },
  plugins: [],
}
