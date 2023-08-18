import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { Box, CircularProgress, Typography } from '@mui/material';
import theme from '../../styles/theme';

const Loading: React.FC = () => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const userId = router.query.user_id;
  const [redirected, setRedirected] = useState(false);


  const [currentMessage, setCurrentMessage] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const [currentMsgIndex, setCurrentMsgIndex] = useState(0);
  const [showCursor, setShowCursor] = useState(true);

  const messagesToAdd = [
    "scanning playlists...",
    "identifying top tracks...",
    "gathering genres...",
    "analyzing tracks...",
    "something something something...",
    "streamlining user interface...",
    "fetching user insights...",
    "blah blah blah...",
    "buffering music data...",
    "cross-checking results...",
    "analyzing listener trends...",
    "wasting your time...",
    "benchmarking performance...",
    "finalizing computations...",
    "optimizing algorithms...",
    "preparing visualization...",
    "generating insights...",
    "verifying user consent...",
    "testing synchronization...",
    "finalizing graphics...",
    "wasting more of your time...",
    "you're all set...",
    "almost there...",
    "just a little longer...",
    "just a little more...",
    "just a little bit more...",
    "just a little bit longer...",
    "give me a second...",
    "okay should be good now...",
    "wait nevermind...",
    "okay NOW it should be good...",
    "sorry about that...",
    "all of this is just filler text...",
    "these are all just on a timer...",
    "it should be done soon...",
  ];

  const addLetterByLetter = (msg: string) => {
    let msgIndex = -1;
    setCurrentMessage(''); // Clear the current message before typing the next one
    const typingInterval = setInterval(() => {
      setCurrentMessage(prev => prev + msg[msgIndex]);
      msgIndex++;

      if (msgIndex >= msg.length - 1) {
        clearInterval(typingInterval);
        // Go to the next message
        setCurrentMsgIndex(prev => (prev + 1) % messagesToAdd.length);
      }
    }, 50);
};

  
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 400); // 500ms for half a second interval
  
    // Cleanup on unmount to prevent memory leaks
    return () => clearInterval(interval);
  }, []);
  
  useEffect(() => {
    const interval = setInterval(() => {
        addLetterByLetter(messagesToAdd[currentMsgIndex]);
    }, 2000);

    return () => clearInterval(interval);
}, [currentMsgIndex]);

  

  
  useEffect(() => {
    
    if (userId) {
      const fetchData = async () => {
        try {
          const response = await fetch(`http://localhost:8000/checkData?user_id=${userId}`);
          const data = await response.json();

          if (response.ok) {
            if (router.isReady && data.ready) {
                console.log("Attempting to redirect...");
                setIsLoading(false);
                setRedirected(true);
                router.push('/youravg?data=' + data.result);
            }
          } else {
            console.error("Error fetching data:", data.detail);
          }
        } catch (error) {
          console.error("Failed to fetch:", error);
        }
      };
      
      const interval = setInterval(fetchData, 5000);  // Poll every 5 seconds

      // Cleanup the interval when the component unmounts
      return () => clearInterval(interval);
    }
  }, [userId]);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        width: '100%',
        overflowY: 'auto',
        overflowX: 'hidden',
        fontFamily: 'monospace',
        color: 'textSecondary',
        // paddingTop: '10rem'
        
      }}
    >
        
      <Box sx={{ textAlign: 'center', width: '100%', alignItems: "center"}}>
        
        <Typography variant="h3" gutterBottom>
            <span style={{ color: "textSecondary" }}>analyzing your</span>
        <span style={{ color: '#0d9488' }}> playlists...</span>
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
        this could take a few minutes
      </Typography>
      <CircularProgress color="primary" size={50} style={{ marginBottom: '1rem', marginTop: '2rem', alignSelf: "center"}} />
      <div style={{ textAlign: 'center', paddingBottom: "20px", alignItems: "center"}}>
          {/* Display current message being typed */}
          <Typography variant="body1">
            {currentMessage}
            <span style={{ opacity: showCursor ? 1 : 0 }}>|</span>
          </Typography>
        </div>
      </Box>
    </Box>
  );
};

export default Loading;