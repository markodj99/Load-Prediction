import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import ImportTrainingDataButton from "./components/ImportTrainingDataButton";
import TrainModelButton from "./components/TrainModelButton";
import ImportAndPrepareTestDataButton from "./components/ImportAndPrepareTestDataButton";
import TestModelButton from "./components/TestModelButton";
import 'bootstrap/dist/css/bootstrap.css';
import { Toaster } from "react-hot-toast";
import PredictTable from "./components/PredictTable";
import { useState } from "react";

function App()
{ 
  const [firtDay, setFirtDay] = useState(1);
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
      <div className="btn-group-justified d-flex justify-content-center mb-5" role="group" aria-label="Basic example">
        <ImportTrainingDataButton/>
        <PrepareTrainingDataButton/>
        <TrainModelButton/>
        <ImportAndPrepareTestDataButton/>
        <TestModelButton setPredictData={setPredictData} setFirtDay={setFirtDay} setNumberOfDays={setNumberOfDays}/>
        <button type="button" className="btn btn-outline-primary" onClick={() => {setHideTable(!hideTable)}}>Show Predict</button>
        <Toaster/>
      </div>
      <div className={`container d-flex justify-content-center ${hideTable ? 'd-none' : ''}`}>
        <PredictTable predictData={predictData} firtDay={firtDay} numberOfDays={numberOfDays}/>
      </div>
    </>
  );
}

export default App;