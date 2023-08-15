import React from 'react';
import { Button } from '@mui/material';

const Authenticate: React.FC = () => {
  const handleAuthenticate = () => {
    // Redirect the user to the FastAPI authentication endpoint
    window.location.href = 'http://localhost:8000/';
  };

  return (
    <div>
      <h1>Authenticate with Spotify</h1>
      <Button variant="contained" color="primary" onClick={handleAuthenticate}>
        Authenticate
      </Button>
    </div>
  );
};

export default Authenticate;
