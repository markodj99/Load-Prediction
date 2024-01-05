//import React, {useState, useEffect} from "react";
import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import SendTrainingDataButton from "./components/SendTrainingDataButton";
import TrainDataButton from "./components/TrainDataButton";
import 'bootstrap/dist/css/bootstrap.css';

function App()
{
  return(
      <div className="btn-group d-flex container" role="group" aria-label="Basic example">
        <SendTrainingDataButton/>
        <PrepareTrainingDataButton/>
        <TrainDataButton/>
      </div>
  );
}

export default App;