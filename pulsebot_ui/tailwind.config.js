/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          50: '#F7F6F6',
          100: '#EFEDF5',
          200: '#D7D4E2',
          300: '#B8B4C7',
          400: '#9994AC',
          500: '#7A7591',
          600: '#5C5775',
          700: '#3D3852',
          800: '#1F1B2E',
          900: '#120F1A',
        },
        pink: {
          light: '#FED7E2',
          hover: '#B83280',
          primary: '#D53F8C',
          400: '#B83280',
          500: '#D53F8C',
        },
        error: {
          hover: '#751025',
          primary: '#D12D50',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
