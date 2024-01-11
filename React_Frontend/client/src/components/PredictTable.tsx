import 'bootstrap/dist/css/bootstrap.css';

interface Props{
    predictData: PredictData,
    firtDay: number,
    numberOfDays: number
}

interface DayData {
    date: string[];
    load: number[][];
}
  
interface PredictData {
    day1: DayData;
    day2: DayData;
    day3: DayData;
    day4: DayData;
    day5: DayData;
    day6: DayData;
    day7: DayData;
}

interface UnpackedData {
    date: string[];
    load: number[];
}
  
function PredictTable({predictData, firtDay, numberOfDays}: Props)
{
    let arrayOfPredictData = [predictData.day1, predictData.day2, predictData.day3, predictData.day4, 
                              predictData.day5, predictData.day6, predictData.day7];
    
    //arrayOfPredictData = arrayOfPredictData.slice(firtDay, arrayOfPredictData.length);

    //if (numberOfDays > arrayOfPredictData.length) numberOfDays = arrayOfPredictData.length;
    //else arrayOfPredictData = arrayOfPredictData.slice(0, numberOfDays);
    //const maxNumberOfDays = arrayOfPredictData.length - firtDay;
    //if (numberOfDays > maxNumberOfDays) numberOfDays = maxNumberOfDays;
    let unpackedData:UnpackedData = {date: [], load: []};
    
    if (arrayOfPredictData[0].date.length !== 0)
    {
        for(let i = 0; i < arrayOfPredictData.length; i++)
        {
            for(let j = 0; j < 24; j++)
            {
                unpackedData.date.push(arrayOfPredictData[i].date[0][j]);
                unpackedData.load.push(arrayOfPredictData[i].load[0][j]);
            }
        }
    }
    
    const displayData = unpackedData.date.map((date, idx) => (
        <tr key={idx} className="table-dark">
            <th scope="row">{idx + 1}</th>
            <td>{date.slice(0, -3)} h</td>
            <td>{unpackedData.load[idx].toFixed(2)}</td>
        </tr>
    ));

    return(
        <table className="table table-striped-columns">
            <thead>
                <tr className="table-dark">
                    <th scope="col">#</th>
                    <th scope="col">Date</th>
                    <th scope="col">Load</th>
                </tr>
            </thead>
            <tbody>
                {displayData}
            </tbody>
        </table>
    );
}

export default PredictTable;