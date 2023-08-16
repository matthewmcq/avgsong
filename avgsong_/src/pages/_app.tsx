import React from 'react';
import { AppProps } from 'next/app';
import Layout from '../app/layout'; // Update the import path
import theme from '../../styles/theme';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';


function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
        <ThemeProvider theme={theme}>
            <CssBaseline />
      <Component {...pageProps} />
      </ThemeProvider>
    </Layout>
  );
}

export default MyApp;