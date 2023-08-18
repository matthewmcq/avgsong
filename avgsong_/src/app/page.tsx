import React from 'react';
import Layout from './layout';
import HomePage from '../pages/home';
import Top200 from '../pages/top200';
import YourAvg from '../pages/youravg';
import { Button } from '@mui/material';
import theme from '../../styles/theme';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppProps } from 'next/app';
import "./globals.css";

const AppPage: React.FC = () => {
  return (
    
      <HomePage />
  );
};

export default AppPage;