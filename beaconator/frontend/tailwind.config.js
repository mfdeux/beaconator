// See default config https://github.com/tailwindcss/tailwindcss/blob/master/stubs/defaultConfig.stub.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#38B2AC',
        'primary-dark': '#319795',
      },
      borderColors: ['responsive', 'hover', 'focus', 'group-hover'],
      visibility: ['responsive', 'group-hover'],
      padding: {
        '28': '7rem',
        '34': '8.5rem',
        '36': '9rem',
      },
      height: {
        7: '1.75rem',
        11: '2.875rem',
        13: '3.25rem',
        14: '3.5rem',
        '36': '9rem',
        '3/8': '37%',
        '1/2': '50',
        '5/8': '63%',
        '3/4': '75%',
        '7/8': '88%',
      },
      width: {
        '7': '1.75rem',
        13: '3.25rem',
        14: '3.5rem',
        '18': '4.5rem',
        '28': '7rem',
        '52': '13rem',
        '95': '95%',
        '1/5': '20%',
        '1/4': '25%',
        '3/10': '30%',
        '3/8': '38%',
        '2/5': '40%',
        '1/2': '50%',
        '5/8': '63%',
        '3/4': '75%',
        '7/8': '88%',
      },
      fontSize: {
        md: '.935rem',
        mxl: '1.375rem',
      },
      borderRadius: {
        xl: '1rem',
      },
      borderWidth: {
        '3': '3px',
      },
      minWidth: {
        '0': '0',
        '1/4': '25%',
        '3/8': '38%',
        '1/2': '50%',
        '5/8': '63%',
        '3/4': '75%',
        '7/8': '88%',
        full: '100%',
      },
    },
  },
  variants: {
    borderCollapse: ['responsive', 'hover', 'focus'],
  },
};
