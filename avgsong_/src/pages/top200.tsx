import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { useRouter } from 'next/router'; // Import the router hook

const Top200: React.FC = () => {
  const router = useRouter(); // Initialize the router
  const [data, setData] = useState<string | null>(null);

  useEffect(() => {
    // Extract the data query parameter from the URL
    const { data: authData } = router.query;
    if (authData) {
      setData(authData as string);
    }
  }, [router.query]);
  const handleAuthenticate = () => {
    // Redirect to the FastAPI authentication endpoint
    window.location.href = 'http://localhost:8000/';
  };
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
        Top 200 Page
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        This is the Top 200 page content.
      </Typography>
      {data ? (
        <div>
          <p>{data}</p>
          {/* Display the data received from the callback */}
        </div>
      ) : (
        <Button
          variant="contained"
          color="primary"
          onClick={handleAuthenticate}
          style={{ marginTop: '20px' }}
        >
          Authenticate with Spotify
        </Button>
      )}
    </Box>
  );
};

export default Top200;
