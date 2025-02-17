/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    '../../theme/static_src/**/*.js',
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
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
