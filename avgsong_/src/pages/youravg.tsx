import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { useRouter } from 'next/router'; // Import the router hook
import styles from '/styles/styles.module.css';

interface PlaylistItem {
  playlist_name: string;
  song_name: string;
  artist: string;
  image_url: string;
}

const YourAvg: React.FC = () => {
  const router = useRouter(); // Initialize the router
  const [playlistData, setPlaylistData] = useState<PlaylistItem[] | null>(null);

  useEffect(() => {
    // Extract the JSON data from the URL query parameter
    const jsonData = router.query.data;

    if (jsonData) {
      // Ensure we're working with a single string, not an array
      const jsonDataString = Array.isArray(jsonData) ? jsonData[0] : jsonData;

      // Decode and parse the JSON data
      const decodedJsonData = decodeURIComponent(jsonDataString);
      setPlaylistData(JSON.parse(decodedJsonData) as PlaylistItem[]);
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
        your 
        <span style={{ color: '#64748b' }}> avgs</span>
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        get the average song for each of your playlists
      </Typography>
      {playlistData ? (
  <div className={styles.columns}>
    {playlistData.map((playlist, index) => (
      <div className={styles.column} key={index}>
        <h4>{playlist.playlist_name}</h4>
        <img
          src={playlist.image_url}
          alt={playlist.playlist_name}
          className={`${styles.image} ${styles.imageResize}`}
          style={{ maxWidth: '100%', height: 'auto' }}
        />
        <p>
          {playlist.song_name} by {playlist.artist}
        </p>
      </div>
    ))}
  </div>
) : (
  <Button
    variant="contained"
    color="primary"
    onClick={handleAuthenticate}
    style={{ marginTop: '20px' }}
  >
    authenticate with spotify
  </Button>
)}
    </Box>
  );
};

export default YourAvg;
