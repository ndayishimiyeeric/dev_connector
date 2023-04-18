module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    fontFamily: {
      sans: ['Raleway', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
      display: ['IBM Plex Mono', 'Menlo', 'monospace'],
    },
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
}

