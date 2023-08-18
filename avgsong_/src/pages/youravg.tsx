import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, CircularProgress } from '@mui/material';
import { useRouter } from 'next/router'; // Import the router hook
import styles from '/styles/styles.module.css';
import theme from '../../styles/theme';
import { ThemeProvider } from '@mui/material/styles';

interface PlaylistItem {
  playlist_name: string;
  song_name: string;
  artist: string;
  image_url: string;
  top_track_image: string; // New field
  playlist_genre_count: number; // New field
  playlist_top_genres: string; // New field (as JSON string)
}

const YourAvg: React.FC = () => {
  const router = useRouter();
  const [playlistData, setPlaylistData] = useState<PlaylistItem[] | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true); // New state for loading
  const [hoveredPlaylistIndex, setHoveredPlaylistIndex] = useState<number | null>(null);
  
  useEffect(() => {
    const jsonData = router.query.data;

    if (jsonData) {
      const jsonDataString = Array.isArray(jsonData) ? jsonData[0] : jsonData;
      const decodedJsonData = decodeURIComponent(jsonDataString);
      console.log(decodedJsonData);
      try {
        setPlaylistData(JSON.parse(decodedJsonData) as PlaylistItem[]);
      } catch (error) {
        console.error('Error parsing JSON:', error);
      }
      setIsLoading(false); // move this inside the condition
    }
  }, [router.query]);

  const handleAuthenticate = () => {
    window.location.href = 'http://localhost:8000/';
  };

  const [expandedPlaylistIndex, setExpandedPlaylistIndex] = useState<number | null>(null);

  const toggleInfoPanel = (index: number) => {
    if (expandedPlaylistIndex === index) {
      setExpandedPlaylistIndex(null);
    } else {
      setExpandedPlaylistIndex(index);
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="80vh"
      textAlign="center"
      overflow-y="scroll"
      flex="1"
      bgcolor={theme.palette.background.default}
    >
      <div style={{marginTop: "0px"}}>
      <Typography variant="h3" gutterBottom>
        your
        <span style={{ color: '#0d9488' }}> avgs</span>
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        get the average song for each of your playlists
      </Typography>
      </div>
      {playlistData ? (
      <div className={styles.playlistsContainer}>
        {playlistData.map((playlist, index) => {
          const topGenres: string[] = JSON.parse(playlist.playlist_top_genres);

          return (
            <div
            key={index}
            className={`${styles.playlistBlock} ${
              expandedPlaylistIndex === index ? styles.expanded : ''
            }`}
            onMouseEnter={() => setHoveredPlaylistIndex(index)}
            onMouseLeave={() => setHoveredPlaylistIndex(null)}
            >
              <div className={styles.playlistColumns}>
                  <div className={styles.infoRow}
                  data-playlist-name={playlist.playlist_name}
                    >
                    <div className={styles.playlistImageContainer}
                    data-playlist-name={playlist.playlist_name}
                    >
                      <img
                        src={playlist.image_url}
                        alt={playlist.playlist_name}
                        className={styles.playlistImage}
                      />
                    </div>
                    <div className={styles.songInfo}>
                      <p>
                        {" "}
                        <strong>"{playlist.song_name}"</strong> by
                        <strong> {playlist.artist}</strong>
                      </p>
                      <p>
                        Incorporates{" "}
                        <strong>{playlist.playlist_genre_count} sub-genres</strong>
                      </p>
                      <p>
                        Most common {" "}
                        <strong>{topGenres.join(', ')}</strong>
                      </p>
                    </div>
                    <div className={styles.playlistImageContainer}
                    data-playlist-name={playlist.song_name}
                    >
                    <img
                      src={playlist.top_track_image}
                      alt={playlist.artist}
                      className={styles.topTrackImage}
                    />
                  </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <>
          {/* <Typography variant="subtitle2" color="error" gutterBottom>
            An error occurred while fetching your playlists. Please try again.
          </Typography> */}
          <Button
            variant="contained"
            color="primary"
            onClick={handleAuthenticate}
            style={{ marginTop: '20px' }}
          >
            authenticate with spotify
          </Button>
        </>
      )}
    </Box>
  );
};

export default YourAvg;
