import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Link from 'next/link';
import './globals.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <AppBar position="static" style={{ backgroundColor: '#1e293b' , cursor: 'pointer'}}>
        <Toolbar>
        <nav style={{ marginRight: 'auto', display: 'flex', alignItems: 'center', textDecoration: 'none'}}>
          <Typography variant="h5">
          <Link href="/home" passHref>
            <span style={{ color: '#e5e5e5' }}>avg</span>
            <span style={{ color: '#0d9488' }}>song</span>
            </Link>
          </Typography>
          
          <Typography variant="body1" style={{textDecoration: 'none'}} >
            <Link href="/top200" passHref>
            <span style={{ color: '#e5e5e5', verticalAlign: 'middle', marginLeft: '15px'}}>top 200 </span>
            </Link>
            <Link href="/youravg" passHref>
              
            <span style={{ color: '#e5e5e5', verticalAlign: 'middle', marginLeft: '10px'}}>your avgs</span>
              
            </Link>
            </Typography>
          </nav>
        </Toolbar>
      </AppBar>
      {children}
    </div>
  );
};

export default Layout;
