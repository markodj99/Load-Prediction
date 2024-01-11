import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import ImportTrainingDataButton from "./components/ImportTrainingDataButton";
import TrainModelButton from "./components/TrainModelButton";
import ImportAndPrepareTestDataButton from "./components/ImportAndPrepareTestDataButton";
import TestModelButton from "./components/TestModelButton";
import { Toaster } from "react-hot-toast";
import PredictTable from "./components/PredictTable";
import { useState } from "react";
import 'bootstrap/dist/css/bootstrap.css';

function App()
{ 
  const [firstDay, setFirstDay] = useState(1);
  const [numberOfDays, setNumberOfDays] = useState(7);
  const [predictData, setPredictData] = useState({
                                                    'day1': {'date':[], 'load':[]},
                                                    'day2': {'date':[], 'load':[]},
                                                    'day3': {'date':[], 'load':[]},
                                                    'day4': {'date':[], 'load':[]},
                                                    'day5': {'date':[], 'load':[]},
                                                    'day6': {'date':[], 'load':[]},
                                                    'day7': {'date':[], 'load':[]}
                                                  }
                                                );

  const [hideTable, setHideTable] = useState(true);

  return(
    <>
      <div className="btn-group-justified d-flex justify-content-center" role="group" aria-label="Basic example">
        <ImportTrainingDataButton/>
        <PrepareTrainingDataButton/>
        <TrainModelButton/>
        <ImportAndPrepareTestDataButton/>
        <TestModelButton setPredictData={setPredictData} setFirstDay={setFirstDay} setNumberOfDays={setNumberOfDays}/>
        <button type="button" className="btn btn-outline-warning" onClick={() => {setHideTable(!hideTable)}}>Show Predict</button>
      </div>
      <div className={`container d-flex justify-content-center ${hideTable ? 'd-none' : ''}`}>
        <PredictTable predictData={predictData} firstDay={firstDay} numberOfDays={numberOfDays}/>
      </div>
      <Toaster position="bottom-right" 
        toastOptions={{
              success: {
                style: {
                  border: '2px solid black',
                  background: 'green',
                  width: '500px',
                  height: '100px',
                  fontSize: "20px",
                  color: "black"
                },
                duration: 6000
              },
              error: {
                style: {
                  border: '2px solid black',
                  background: 'red',
                  width: '500px',
                  height: '100px',
                  fontSize: "20px",
                  color: "black"
                },
                duration: 6000
              },
              loading: {
                style: {
                  border: '2px solid black',
                  background: 'lightgray',
                  width: '500px',
                  height: '100px',
                  fontSize: "20px",
                  color: "black"
                }
              }
            }}/>
    </>
  );
}

export default App;