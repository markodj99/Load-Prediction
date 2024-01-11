import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';
import Select from 'react-select';

interface Props{
  setPredictData: Function,
  setFirtDay: Function,
  setNumberOfDays: Function
}

function TestModelButton({setPredictData, setFirtDay, setNumberOfDays}:Props) {

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
          setPredictData(data);
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

  const dates = [
                  { value: 1, label: '07.09.2021.' },
                  { value: 2, label: '08.09.2021.' },
                  { value: 3, label: '09.09.2021.' },
                  { value: 4, label: '10.09.2021.' },
                  { value: 5, label: '11.09.2021.' },
                  { value: 6, label: '12.09.2021.' },
                  { value: 7, label: '13.09.2021.' }
                ];
  
  const days = [
                  { value: 1, label: '1' },
                  { value: 2, label: '2' },
                  { value: 3, label: '3' },
                  { value: 4, label: '4' },
                  { value: 5, label: '5' },
                  { value: 6, label: '6' },
                  { value: 7, label: '7' }
               ];
  
  return (
      <div className="btn-group">
        <div className="btn btn-outline-primary">
          <Select
            options={dates}
            onChange={(selectedOption) => {setFirtDay(selectedOption)}}
            isSearchable={false}
            placeholder='Pick a date'
          />
          <Select
            options={days}
            onChange={(selectedOption) => {setNumberOfDays(selectedOption)}}
            isSearchable={false}
            placeholder='Pick number'
          />
        </div>
        <button type="button" className="btn btn-outline-primary" onClick={handlePrepareTrainingData}>Predict</button>
      </div>
    );
}

export default TestModelButton;