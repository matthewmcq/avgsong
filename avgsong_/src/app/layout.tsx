import { AppBar, Toolbar, Typography } from '@mui/material';
import React from 'react';
import styles from '/styles/Layout.module.css';
import Link from 'next/link';
import './globals.css';
import { LayoutProps } from '../../.next/types/app/layout';

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <AppBar position="static" style={{ backgroundColor: '#1e293b', cursor: 'pointer' }}>
        <Toolbar>
          <nav style={{ marginRight: 'auto', display: 'flex', alignItems: 'center' }}>
            <Typography 
            variant="h5"
            
            >
              <Link href="/home" passHref>
                <div className={`${styles.textWrapper} ${styles.scrollAnimation} ${styles.navLink}`}>
                <span className={`${styles.avgText} ${styles.scrollAnimation}`}>avg<span className={styles.songText}>song</span> </span>
                
                </div>
                
            
              </Link>
            </Typography>
            <Typography
              variant="body1"
              className={`${styles.textWrapper} ${styles.scrollAnimation} ${styles.navLink}`}
            >
              <Link href="/top200" passHref>
                <span className={styles.navLink}>top albums</span>
              </Link>
            </Typography>
            <Typography
              variant="body1"
              className={`${styles.textWrapper} ${styles.scrollAnimation} ${styles.navLink}`}
            >
              <Link href="/youravg" passHref>
                <span className={styles.navLink}>your avgs</span>
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
