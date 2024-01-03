//import React, {useState, useEffect} from "react";
import PrepareTrainingDataButton from "./components/PrepareTrainingDataButton";
import SendTrainingDataButton from "./components/SendTrainingDataButton";

function App()
{
  return (
          <div>
            <SendTrainingDataButton/>
            <PrepareTrainingDataButton/>
          </div>
          );
}

export default App;