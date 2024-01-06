import sqlite3
import pandas as pd


def saveProcessedDataToDb(dataFrame, dataBaseName):
    connection = sqlite3.connect(dataBaseName)
    dataFrame.to_sql(name='Load', con=connection, if_exists='replace')
    connection.close()

    return dataFrame.shape[0]


def loadDataFromDb(dataBaseName, ignore2020=False):
    testQuery = """
                    SELECT *
                    FROM Load
                    WHERE date >= '2018-01-01 00:00:00' AND date <= '2018-06-30 23:59:59';
                """
    normalQuery = 'SELECT * FROM Load'

    connection = sqlite3.connect(dataBaseName)
    dataFrame = pd.read_sql_query(normalQuery, connection)
    connection.close()

    if ignore2020:
        dataFrame['date'] = pd.to_datetime(dataFrame['date'])
        dataFrame = dataFrame[~dataFrame['date'].dt.year.isin([2020])]

    dataFrame = dataFrame.drop('index', axis=1)
    dataFrame = dataFrame.drop('name', axis=1)
    dataFrame = dataFrame.drop('date', axis=1)

    return dataFrame


def saveModelScoreData(modelName, trainScoreMape, testScoreMape, trainScoreRmse, testScoreRmse, dataBaseName):
    conn = sqlite3.connect(dataBaseName)
    cursor = conn.cursor()

    data = (modelName, trainScoreMape, testScoreMape, trainScoreRmse, testScoreRmse)
    insert_query = '''
    INSERT INTO modelScore (name, mape_train, mape_test, rmse_train, rmse_test)
    VALUES (?, ?, ?, ?, ?);
    '''

    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

