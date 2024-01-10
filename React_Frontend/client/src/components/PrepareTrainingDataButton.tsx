import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';

function PrepareTrainingDataButton() {

  const handlePrepareTrainingData = async () => {
    const uploadEndpoint = 'http://localhost:5000/prepare_training_data';
    const formData = new FormData();
    toast.loading('Preparing training data. Please be patient.');
    try {
        const response = await fetch(uploadEndpoint, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          toast.dismiss();
          toast.success(`Successfully processed and saved ${data.num_processed_writen_instance} objects.` , {
            duration: 3000
          });
        } else {
          console.error('Error while preparing training data:', response.statusText);
          toast.dismiss();
          toast.error('Error while preparing training data.');
        }
        } catch (error) {
          console.error('Error while preparing training data:', error);
          toast.dismiss();
          toast.error('Error while preparing training data.');
        }
  };

  return (
      <button type="button" className="btn btn-outline-primary mx-5" onClick={handlePrepareTrainingData}>Prepare Training Data</button>
    );
}

export default PrepareTrainingDataButton;