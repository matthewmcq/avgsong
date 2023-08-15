import React from 'react';
import { AppProps } from 'next/app';
import Layout from '../app/layout'; // Update the import path

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;