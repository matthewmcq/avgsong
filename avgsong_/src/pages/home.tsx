import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useRouter } from 'next/router';

const HomePage: React.FC = () => {
  const router = useRouter();

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="80vh"
      textAlign="center"
    >
      <Typography variant="h3" gutterBottom>
        welcome to
        <span style={{ color: '#64748b' }}> avg</span>
        <span style={{ color: '#0d9488' }}>song</span>
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        explore average songs of billboard's top 200 and your own playlists...
      </Typography>
      <div style={{ marginTop: '20px', display: 'flex', gap: '10px', alignItems: 'stretch' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => router.push('/top200')}
        >
           top 200 
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={() => router.push('/youravg')}
        >
          your avgs
        </Button>
      </div>
    </Box>
  );
};

export default HomePage;
