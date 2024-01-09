//import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';

function PrepareTrainingDataButton() {

  const handlePrepareTrainingData = async () => {
    const uploadEndpoint = 'http://localhost:5000/prepare_training_data';
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
      <button type="button" className="btn btn-outline-primary mx-5" onClick={handlePrepareTrainingData}>Prepare Training Data</button>
    );
}

export default PrepareTrainingDataButton;