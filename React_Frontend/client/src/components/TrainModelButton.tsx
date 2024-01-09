import {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import toast from 'react-hot-toast';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

function TrainDataButton() {

    const handleTrainData = async () => {
      const uploadEndpoint = 'http://localhost:5000/train_model';
      const formData = new FormData();
      formData.append('startDate', selectedStartDate.toISOString());
      formData.append('endDate', selectedEndDate.toISOString());

      toast.loading('Please be patient. This will take a while.');
      try {
          const response = await fetch(uploadEndpoint, {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            const data = await response.json();
            toast.dismiss();
            toast.success(`Successfully trained new model.
                              MAPE Train: ${data.train_score_mape.toFixed(2)}%
                              MAPE test: ${data.test_score_mape.toFixed(2)}%
                              RMSE Train: ${data.train_score_rmse.toFixed(2)}
                              RMSE Test: ${data.test_score_rmse.toFixed(2)}` , {
                          duration: 8000
            });
          } else {
            console.error('Error while training a model:', response.statusText);
            toast.dismiss();
            toast.error('Error while training a model.');
          }
          } catch (error) {
            console.error('Error while training a model:', error);
            toast.dismiss();
            toast.error('Error while training a model.');
          }
    };
  
    const defaultStartDate = new Date('2018-01-02');
    const [selectedStartDate, setSelectedStartDate] = useState<Date>(defaultStartDate);

    const defaultEndDate = new Date('2021-09-06');
    const [selectedEndDate, setSelectedEndDate] = useState<Date>(defaultEndDate);
    
    const maxStartDate = new Date('2021-08-06')
    const minEndDate = new Date('2018-02-02');

    const handleStartDateChange = (date: Date | null) => {
      if (date == null) return;
      if(date >= selectedEndDate) toast.error('The start date cannot be greater that end date.');
      else if (date < defaultStartDate) toast.error('The oldest date you can pick for start date is 01-02-2018.');
      else if(date > maxStartDate) toast.error('The newest date you can pick for start date is 06-08-2021.');
      else setSelectedStartDate(date);
    };

    const handleEndDateChange = (date: Date | null) => {
      if (date == null) return;
      if(date <= selectedStartDate) toast.error('The end date cannot be lesser that start date.');
      else if (date > defaultEndDate) toast.error('The newest date you can pick for end date is 06-09-2021.');
      else if(date < minEndDate) toast.error('The oldest date you can pick for end date is 02-02-2018.');
      else setSelectedEndDate(date);
    };


    return (
      <div className="btn-group">
        <div className='btn btn-outline-primary d-flex justify-content-center align-items-center text-center flex-grow'>
          <DatePicker selected={selectedStartDate} onChange={(date) => handleStartDateChange(date)} dateFormat="dd/MM/yyyy"/>
          <DatePicker selected={selectedEndDate} onChange={(date) => handleEndDateChange(date)} dateFormat="dd/MM/yyyy"/>
        </div>
        <button type="button" className="btn btn-outline-primary" onClick={handleTrainData}>Train Model</button>
      </div>
    );
  }
  
  export default TrainDataButton;