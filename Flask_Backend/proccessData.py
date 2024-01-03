from dataLoader import *


def combineData(loadDataPath, weatherDataPath):
    loadDataFrame = loadLoadData(loadDataPath)
    loadDataFrame = loadDataFrame.reset_index(drop=True)

    weatherDataFrame = loadWeatherData(weatherDataPath, loadDataFrame['date'].min(), loadDataFrame['date'].max())
    weatherDataFrame = weatherDataFrame.reset_index(drop=True)
    
    combineData = pd.merge_asof(weatherDataFrame, loadDataFrame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
    combineData = combineData[combineData['load'].notna()]
    combineData = combineData.reset_index(drop=True)

    print(combineData)

    return combineData


def getTrainingData():
    pass