import pandas as pd
import os


def invokeDataLoading(loadDataPath, weatherDataPath, holidaysDataPath):
    dataFrame = combineData(loadDataPath, weatherDataPath)
    dataFrame = removeHolidays(dataFrame, holidaysDataPath)

    return dataFrame


def combineData(loadDataPath, weatherDataPath):
    loadDataFrame = loadLoadData(loadDataPath)
    loadDataFrame = loadDataFrame.reset_index(drop=True)

    weatherDataFrame = loadWeatherData(weatherDataPath, loadDataFrame['date'].min(), loadDataFrame['date'].max())
    weatherDataFrame = weatherDataFrame.reset_index(drop=True)
    
    combinedData = pd.merge_asof(weatherDataFrame, loadDataFrame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
    combinedData = combinedData[combinedData['load'].notna()]
    combinedData = combinedData.reset_index(drop=True)

    return combinedData


def removeHolidays(dataFrame, holidaysDataPath):
    holidays = loadHolidays(holidaysDataPath)
    
    dataFrame['date'] = pd.to_datetime(dataFrame['date'])
    holidays['date'] = pd.to_datetime(holidays['date'])

    dataFrame['dateColumnPartial'] = dataFrame['date'].dt.date
    holidays['dateColumnPartial'] = holidays['date'].dt.date

    dataFrame = dataFrame[~dataFrame['dateColumnPartial'].isin(holidays['dateColumnPartial'])]
    dataFrame = dataFrame.drop('dateColumnPartial', axis=1)

    return dataFrame


def loadLoadData(loadDataPath):
    dataFrame = pd.DataFrame()

    for filename in os.scandir(loadDataPath):
        if filename.is_file() and filename.name.endswith('.csv'):
            dataFrameTemp = pd.read_csv(filename.path, engine='python', sep=',', header=0, usecols=[0, 2, 4], names=['date', 'name', 'load'])
            dataFrame = pd.concat([dataFrame, dataFrameTemp], axis=0)

    dataFrame = dataFrame.loc[dataFrame['name'] == 'N.Y.C.']
    dataFrame = dataFrame.drop('name', axis=1)
    dataFrame = dataFrame[dataFrame['date'].str.endswith("00:00")]
    dataFrame['date'] = pd.to_datetime(dataFrame['date'], format='%m/%d/%Y %H:%M:%S')

    return dataFrame


def loadWeatherData(weatherDataPath, minDate, maxDate):
    dataFrame = pd.DataFrame()

    for filename in os.scandir(weatherDataPath):
        if filename.is_file() and filename.name.endswith('.csv'):
            dataFrameTemp = pd.read_csv(filename.path, engine='python', sep=',', header=0,
            dtype={'datetime':str,'temp':float,'feelslike':float,'dew':float,'humidity':float,'precip':float,'precipprob':float,'preciptype':float,'snow':float,
                        'snowdepth':float,'windgust':float,'windspeed':float,'winddir':float,'sealevelpressure':float,'cloudcover':float,'visibility':float,'solarradiation':float,
                        'solarenergy':float,'uvindex':float,'severerisk':float,'conditions':str})

            dataFrame = pd.concat([dataFrame, dataFrameTemp], axis=0)

    dataFrame.rename(columns={'datetime':'date'}, inplace=True)
    dataFrame['date'] = pd.to_datetime(dataFrame['date'], format='%Y-%m-%dT%H:%M:%S')
    dataFrame = dataFrame.loc[dataFrame['date'].between(minDate, maxDate)]

    return dataFrame


def loadHolidays(holidaysDataPath):
    dataFrame = pd.DataFrame()

    for filename in os.scandir(holidaysDataPath):
        if filename.is_file() and filename.name.endswith('.xlsx'):
            dataFrame = pd.read_excel(filename.path, header=None, names=['nan', 'day', 'date', 'event'], skiprows=1)

    dataFrame = dataFrame.drop('day', axis=1)
    dataFrame = dataFrame.drop('event', axis=1)
    dataFrame = dataFrame.drop('nan', axis=1)
    dataFrame = dataFrame.dropna(subset=['date'])
    dataFrame['date'] = pd.to_datetime(dataFrame['date']).dt.strftime('%Y-%m-%d')

    return dataFrame 

