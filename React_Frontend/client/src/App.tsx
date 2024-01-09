//import React, {useState, useEffect} from "react";
import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import ImportTrainingDataButton from "./components/ImportTrainingDataButton";
import TrainModelButton from "./components/TrainModelButton";
import ImportAndPrepareTestDataButton from "./components/ImportAndPrepareTestDataButton";
import 'bootstrap/dist/css/bootstrap.css';
import { Toaster } from "react-hot-toast";

function App()
{
  return(
    <div className="btn-group-justified d-flex justify-content-center" role="group" aria-label="Basic example">
      <ImportTrainingDataButton/>
      <PrepareTrainingDataButton/>
      <TrainModelButton/>
      <ImportAndPrepareTestDataButton/>
      <button> new </button>
      <Toaster/>
    </div>
  );
}

export default App;