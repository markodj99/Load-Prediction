import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';

function TestModelButton() {

  const handlePrepareTrainingData = async () => {
    const uploadEndpoint = 'http://localhost:5000/test_model';
    const formData = new FormData();
    toast.loading('Preparing training data. Please be patient.');
    try {
        const response = await fetch(uploadEndpoint, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          toast.dismiss();
          toast.success(`Successfully tested model.` , {
            duration: 3000
          });
        } else {
          console.error('Error while testing model:', response.statusText);
          toast.dismiss();
          toast.error('Error while testing modela.');
        }
        } catch (error) {
          console.error('Error while testing model:', error);
          toast.dismiss();
          toast.error('Error while testing model.');
        }
  };

  return (
      <button type="button" className="btn btn-outline-primary mx-5" onClick={handlePrepareTrainingData}>Test Model</button>
    );
}

export default TestModelButton;