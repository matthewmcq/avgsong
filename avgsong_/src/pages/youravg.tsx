import React from 'react';
import { Box, Typography } from '@mui/material';

const YourAvg: React.FC = () => {
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
        Your Averages Page
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        This is the Your Averages page content.
      </Typography>
    </Box>
  );
};

export default YourAvg;
