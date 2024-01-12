import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';
import Select from 'react-select';

interface Props{
  setPredictData: Function,
  setFirstDay: Function,
  setNumberOfDays: Function
}

function TestModelButton({setPredictData, setFirstDay, setNumberOfDays}:Props) {

  const handlePrepareTrainingData = async () => {
    const uploadEndpoint = 'http://localhost:5000/test_model';
    const formData = new FormData();
    toast.loading('Predicting the load. Please be patient.');
    try {
        const response = await fetch(uploadEndpoint, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setPredictData(data);
          toast.dismiss();
          toast.success(`Successfully predicted the load. Click on 'Show Predict' button to see the results.` , {duration: 8000});
        } else {
          console.error('Error while predicting the load:', response.statusText);
          toast.dismiss();
          toast.error('Error while predicting the load.', {duration: 8000});
        }
        } catch (error) {
          console.error('Error while predicting the load:', error);
          toast.dismiss();
          toast.error('Error while predicting the load.', {duration: 8000});
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
      <div id="test-data-button" className="btn-group w-90">
        <div className="w-70 btn btn-outline-warning d-flex justify-content-center align-items-center text-center flex-grow">
          <Select
            options={dates}
            onChange={(selectedOption) => {setFirstDay(selectedOption?.value)}}
            isSearchable={false}
            placeholder='Pick a date'
            styles={{
              control: (provided) => ({
                ...provided,
                minWidth: '161px',
                border: '5px #ffc107',
              })}}
          />
          <div className="mx-1"/>
          <Select
            options={days}
            onChange={(selectedOption) => {setNumberOfDays(selectedOption?.value)}}
            isSearchable={false}
            placeholder='Pick a number'
            styles={{
              control: (provided) => ({
                ...provided,
                minWidth: '161px',
                border: '5px #ffc107',
              })}}
          />
        </div>
        <button type="button" className="btn btn-outline-warning" onClick={handlePrepareTrainingData}>Predict</button>
      </div>
    );
}

export default TestModelButton;