import React from 'react';
import { Box, Typography } from '@mui/material';

const Top200: React.FC = () => {
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
        Top 200
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        This is the Your Averages page content.
      </Typography>
    </Box>
  );
};

export default Top200;