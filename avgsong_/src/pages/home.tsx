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
        Welcome to My App
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        Explore the Top 200 and Your Averages
      </Typography>
      <Button variant="contained" color="primary" href="/top200" style={{ marginTop: '20px' }}>
        Go to Top 200
      </Button>
    </Box>
  );
};

export default HomePage;
