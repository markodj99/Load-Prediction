//import React, {useState, useEffect} from "react";
import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import SendTrainingDataButton from "./components/SendTrainingDataButton";
import TrainDataButton from "./components/TrainDataButton";

function App()
{
  return (
          <div>
            <SendTrainingDataButton/>
            <PrepareTrainingDataButton/>
            <TrainDataButton/>
          </div>
          );
}

export default App;