import React, { useEffect } from 'react';

const Callback: React.FC = () => {
  useEffect(() => {
    // Parse the query parameter 'code' from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    // Use 'code' to trigger the callback in the FastAPI server
    // You can use fetch or any other HTTP client library here
    if (code) {
      fetch(`http://localhost:8000/callback?code=${code}`)
        .then((response) => response.text())
        .then((data) => {
          console.log(data); // Display the result from the FastAPI callback
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, []);

  return (
    <div>
      <h1>Callback</h1>
      <p>Processing...</p>
    </div>
  );
};

export default Callback;