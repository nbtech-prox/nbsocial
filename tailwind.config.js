/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./core/templates/**/*.html",
    "./users/templates/**/*.html",
    "./posts/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#1e40af',
        'secondary': '#3b82f6',
        'accent': '#60a5fa',
      },
    },
  },
  plugins: [],
}
