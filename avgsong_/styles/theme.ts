import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0d9488', // Replace with your desired color
    },
    background: { default: '#f1f5f9'},
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        '@global': {
          body: {
            background: 'linear-gradient(135deg, black, #083344)',
            minHeight: '100vh',
          },
        },
      },
    },
  },
});

export default theme;