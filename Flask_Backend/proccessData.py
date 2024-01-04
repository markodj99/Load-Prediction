from dataLoader import *
from sklearn.preprocessing import LabelEncoder
import sqlite3


def invokeProccessing(loadDataPath, weatherDataPath, holidaysDataPath, dataBaseName):
    trainingData = combineData(loadDataPath, weatherDataPath)
    trainingData = removeHolidays(trainingData, holidaysDataPath)
    trainingData = dropWeatherFeatures(trainingData)
    trainingData = interpolateMissingValues(trainingData)
    trainingData = fillMissingTemperature(trainingData)
    trainingData = createSeasonColumn(trainingData)
    trainingData = normalizeConditions(trainingData)
    trainingData = normalizeMissingValue(trainingData)

    saveProccessedDataToDb(trainingData, dataBaseName)

    return trainingData


def saveProccessedDataToDb(dataFrame, dataBaseName):
    connection = sqlite3.connect(dataBaseName)
    dataFrame.to_sql(name='Load', con=connection, if_exists='replace')
    connection.close()


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


def dropWeatherFeatures(dataFrame):
    featureDrop = ['dew', 'precip' ,'precipprob','preciptype','snow','snowdepth', 'sealevelpressure', 'visibility','solarradiation','solarenergy','uvindex','severerisk']
    dataFrame = dataFrame.drop(featureDrop, axis=1)
    return dataFrame


def interpolateMissingValues(dataFrame):
    dataFrame['feelslike'] = dataFrame['feelslike'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['windspeed'] = dataFrame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['humidity'] = dataFrame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['windgust'] = dataFrame['windgust'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    dataFrame['winddir'] = dataFrame['winddir'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
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
        return 'autumn'
    else:
        return 'summer'


def normalizeConditions(dataFrame):
    labelEncoder = LabelEncoder()
    dataFrame['conditions'] = labelEncoder.fit_transform(dataFrame['conditions'])
    return dataFrame


def normalizeMissingValue(dataFrame):
    ratios = [ratio for ratio in (dataFrame.isna().sum()/len(dataFrame))]
    for pair in list(zip(dataFrame.columns, ratios)):
        if pair[1] > 0:
            dataFrame = dataFrame.drop([pair[0]], axis=1)

    return dataFrame

