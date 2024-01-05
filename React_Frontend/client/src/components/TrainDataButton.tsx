//import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';

function TrainDataButton() {

    const handleTrainData = async () => {
      const uploadEndpoint = 'http://localhost:5000/trainData';
      const formData = new FormData();
  
      try {
          const response = await fetch(uploadEndpoint, {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            const data = await response.json();
            console.log(data);
          } else {
            console.error('Error preparing training data:', response.statusText);
          }
          } catch (error) {
           console.error('rror preparing training data:', error);
          }
    };
  
    return (
      <button type="button" className="btn btn-outline-primary" onClick={handleTrainData}>Train Data</button>
    );
  }
  
  export default TrainDataButton;