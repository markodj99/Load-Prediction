//import React, {useState, useEffect} from "react";
import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import ImportTrainingDataButton from "./components/ImportTrainingDataButton";
import TrainModelButton from "./components/TrainModelButton";
import 'bootstrap/dist/css/bootstrap.css';

function App()
{
  return(
      <div className="btn-group d-flex container" role="group" aria-label="Basic example">
        <ImportTrainingDataButton/>
        <PrepareTrainingDataButton/>
        <TrainModelButton/>
      </div>
  );
}

export default App;