import 'bootstrap/dist/css/bootstrap.css';

interface Props{
    predictData: PredictData,
    firstDay: number,
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
  
function PredictTable({predictData, firstDay, numberOfDays}: Props)
{
    let arrayOfPredictData = [predictData.day1, predictData.day2, predictData.day3, predictData.day4, 
                              predictData.day5, predictData.day6, predictData.day7];
    
    arrayOfPredictData = arrayOfPredictData.slice(firstDay - 1, arrayOfPredictData.length);

    if (numberOfDays > arrayOfPredictData.length) numberOfDays = arrayOfPredictData.length;
    else arrayOfPredictData = arrayOfPredictData.slice(0, numberOfDays);

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

    const getFormatedDate = (dateString:string) => {
        let date = new Date(dateString);
        
        let day = date.getDate() < 10 ? `0${date.getDate()}` : `${date.getDate()}`;
        let month = date.getMonth() < 9 ? `0${date.getMonth() + 1}` : `${date.getMonth() + 1}`;
        let hour = date.getHours() < 10 ? `0${date.getHours()}` : `${date.getHours()}`;
        let minutes = date.getMinutes() < 10 ? `0${date.getMinutes()}` : `${date.getMinutes()}`;

        return `${day}.${month}.${date.getFullYear()}. ${hour}.${minutes} h`;
    };

    const displayData = unpackedData.date.map((date, idx) => (
        <tr key={idx} className="table-dark">
            <th scope="row">{idx + 1}</th>
            <td>{getFormatedDate(date.slice(0, -3))}</td>
            <td>{unpackedData.load[idx].toFixed(2)}</td>
        </tr>
    ));

    return(
        <div className="table-container">
            <table className="table table-hover table-bordered table-responsive-md">
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
        </div>
    );
}

export default PredictTable;