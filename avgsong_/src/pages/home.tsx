import React from 'react';
import { Box, Typography, Button } from '@mui/material';


const HomePage: React.FC = () => {
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
        explore the average songs of billboard's top 200 and your own playlists...
      </Typography>
      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}></div>
      <Button variant="contained" color="primary" href="/top200" style={{ marginTop: '20px' }}>
        top albums
      </Button>
      <Button variant="contained" color="primary" href="/youravg" style={{ marginTop: '20px' }}>
        your playlists
      </Button>
      </div>

    </Box>
  );
};

export default HomePage;
