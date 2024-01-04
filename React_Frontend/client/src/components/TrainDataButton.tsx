//import React from 'react';

function TrainDataButton() {

    const handleTrainData = async () => {
      const uploadEndpoint = 'http://localhost:5000/trainData';
      const formData = new FormData();
      console.log('usao');
  
      try {
          const response = await fetch(uploadEndpoint, {
            method: 'POST',
            body: formData,
          });
          console.log('cekam');
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
      <section className="container">
        <div >
          <button onClick={handleTrainData}>Train Data</button>
        </div>
      </section>
    );
  }
  
  export default TrainDataButton;