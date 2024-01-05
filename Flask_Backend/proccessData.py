from dataLoader import *
import sqlite3


def invokeProccessing(loadDataPath, weatherDataPath, holidaysDataPath, dataBaseName):
    trainingData = combineData(loadDataPath, weatherDataPath)
    trainingData = removeDuplicates(trainingData)
    trainingData = removeHolidays(trainingData, holidaysDataPath)
    trainingData = dropWeatherFeatures(trainingData)
    trainingData = interpolateMissingValues(trainingData)
    trainingData = fillMissingTemperature(trainingData)
    trainingData = createSeasonColumn(trainingData)
    trainingData = createDayTypeColumn(trainingData)
    trainingData = normalizeMissingValue(trainingData)
    trainingData = createLoadColumnForPrevDay(trainingData)

    saveProccessedDataToDb(trainingData, dataBaseName)


def combineData(loadDataPath, weatherDataPath):
    loadDataFrame = loadLoadData(loadDataPath)
    loadDataFrame = loadDataFrame.reset_index(drop=True)

    weatherDataFrame = loadWeatherData(weatherDataPath, loadDataFrame['date'].min(), loadDataFrame['date'].max())
    weatherDataFrame = weatherDataFrame.reset_index(drop=True)
    
    combinedData = pd.merge_asof(weatherDataFrame, loadDataFrame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
    combinedData = combinedData[combinedData['load'].notna()]
    combinedData = combinedData.reset_index(drop=True)

    return combinedData


def removeDuplicates(dataFrame):
    dataFrame.sort_values(by='date', inplace=True)
    dataFrame.drop_duplicates(subset='date', keep='last', inplace=True)
    dataFrame.reset_index(drop=True, inplace=True)

    return dataFrame


def removeHolidays(dataFrame, holidaysDataPath):
    holidays = loadHolidays(holidaysDataPath)
    
    dataFrame['date'] = pd.to_datetime(dataFrame['date'])
    holidays['date'] = pd.to_datetime(holidays['date'])

    dataFrame['dateColumnPartial'] = dataFrame['date'].dt.date
    holidays['dateColumnPartial'] = holidays['date'].dt.date

    dataFrame = dataFrame[~dataFrame['dateColumnPartial'].isin(holidays['dateColumnPartial'])]
    dataFrame = dataFrame.drop('dateColumnPartial', axis=1)

    return dataFrame


def dropWeatherFeatures(dataFrame):
    featureDrop = ['dew', 'precip', 'precipprob', 'preciptype', 'snow', 'snowdepth', 
                   'sealevelpressure', 'visibility', 'solarradiation', 'solarenergy',
                   'uvindex', 'severerisk', 'feelslike', 'windgust', 'winddir', 'conditions']
    dataFrame = dataFrame.drop(featureDrop, axis=1)
    return dataFrame


def interpolateMissingValues(dataFrame):
    dataFrame['windspeed'] = dataFrame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['humidity'] = dataFrame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['cloudcover'] = dataFrame['cloudcover'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")

    return dataFrame


def fillMissingTemperature(dataFrame):
    
    temp = dataFrame.loc[dataFrame['temp'] >= 122]
    temp = pd.concat([temp, dataFrame.loc[dataFrame['temp'] <= -23]])

    for index, row in temp.iterrows():
        tempSum = dataFrame.iloc[index-1]['temp'] + dataFrame.iloc[index+1]['temp']
        newTemp = tempSum / 2

        dataFrame.at[index, 'temp'] = round(newTemp, 1)

    return dataFrame
    

def createSeasonColumn(dataFrame):
    month = dataFrame['date'].dt.month
    seasons = pd.DataFrame()
    seasons['seasons'] = month.apply(getSeasons)

    seasonsEncoded = pd.get_dummies(seasons.seasons, prefix='season')

    for name in seasonsEncoded.columns:
        dataFrame.insert(1, name, seasonsEncoded[name])

    return dataFrame


def getSeasons(month):
    if month == 12 or month == 1 or month == 2:
        return 'winter'
    elif month == 3 or month == 4 or month == 5:
        return 'spring'
    elif month == 6 or month == 7 or month == 8:
        return 'summer'
    else:
        return 'autumn'


def createDayTypeColumn(dataFrame):
    dataFrame['date'] = pd.to_datetime(dataFrame['date'])
    
    dataFrame.insert(5, 'monday', (dataFrame['date'].dt.day_name() == 'Monday').astype(int))
    dataFrame.insert(6, 'friday', (dataFrame['date'].dt.day_name() == 'Friday').astype(int))
    dataFrame.insert(7, 'saturday', (dataFrame['date'].dt.day_name() == 'Saturday').astype(int))
    dataFrame.insert(8, 'sunday', (dataFrame['date'].dt.day_name() == 'Sunday').astype(int))
    dataFrame.insert(9, 'othey_days', ((dataFrame['date'].dt.day_name() != 'Monday') & 
                                       (dataFrame['date'].dt.day_name() != 'Friday') & 
                                       (dataFrame['date'].dt.day_name() != 'Saturday') & 
                                       (dataFrame['date'].dt.day_name() != 'Sunday')).astype(int))

    return dataFrame


def normalizeMissingValue(dataFrame):
    ratios = [ratio for ratio in (dataFrame.isna().sum()/len(dataFrame))]
    for pair in list(zip(dataFrame.columns, ratios)):
        if pair[1] > 0:
            dataFrame = dataFrame.drop([pair[0]], axis=1)

    return dataFrame


def createLoadColumnForPrevDay(dataFrame):
    dataFrame = dataFrame.reset_index(drop=True)
    dataFrame.insert(15, column='load_day_before', value=dataFrame['load'].shift(24))
    dataFrame.loc[:23, 'load_day_before'] = dataFrame.loc[:23, 'load']

    return dataFrame


def saveProccessedDataToDb(dataFrame, dataBaseName):
    connection = sqlite3.connect(dataBaseName)
    dataFrame.to_sql(name='Load', con=connection, if_exists='replace')
    connection.close()


def loadDataFromDb(dataBaseName):
    connection = sqlite3.connect(dataBaseName)
    dataFrame = pd.read_sql_query('SELECT * FROM Load', connection)
    connection.close()

    dataFrame = dataFrame.drop('index', axis=1)
    dataFrame = dataFrame.drop('name', axis=1)
    dataFrame = dataFrame.drop('date', axis=1)

    return dataFrame