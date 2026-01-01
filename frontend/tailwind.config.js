/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#8B9DC3',
        'marlin': '#3E4C66',
        'port-gore': '#1F2937',
        'rajah': '#F8AF8C',
      },
      
      fontFamily: {
        'raleway': ['Raleway', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
