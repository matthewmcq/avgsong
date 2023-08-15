import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">My App</Typography>
          <div>
            <Link href="/home" passHref>
              Home
            </Link>
            <Link href="/top200" passHref>
              Top 200
            </Link>
            <Link href="/youravg" passHref>
              Your Averages
            </Link>
          </div>
        </Toolbar>
      </AppBar>
      {children}
    </div>
  );
};

export default Layout;
