import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';

function PrepareTrainingDataButton() {
  const handlePrepareTrainingData = async () => {
    const formData = new FormData();
    toast.loading('Preparing training data. Please be patient.');
    try {
        const response = await fetch('/prepare_training_data', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          toast.dismiss();
          toast.success(`Successfully processed and saved ${data.num_processed_writen_instance} instances.` , {duration: 8000});
        } else {
          console.error('Error while preparing the training data:', response.statusText);
          toast.dismiss();
          toast.error('Error while preparing the training data.', {duration: 8000});
        }
        } catch (error) {
          console.error('Error while preparing the training data:', error);
          toast.dismiss();
          toast.error('Error while preparing the training data.', {duration: 8000});
        }
  };

  return (
      <button type="button" className="btn btn-outline-primary" onClick={handlePrepareTrainingData}>Prepare Training Data</button>
    );
}

export default PrepareTrainingDataButton;