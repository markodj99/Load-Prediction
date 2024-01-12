import sqlite3
import pandas as pd


class DataBaseService():

    def __init__(self, train_data_base_name, train_score_data_base_name, test_data_base_name):
        self.__train_data_base_name = train_data_base_name
        self.__train_score_data_base_name = train_score_data_base_name
        self.__test_data_base_name = test_data_base_name

    def save_processed_train_data(self, data_frame):
        connection = sqlite3.connect(self.__train_data_base_name)
        data_frame.to_sql(name='Load', con=connection, if_exists='replace')
        connection.close()

        return data_frame.shape[0]

    def load_training_data(self, start_date, end_date, ignore2020=False):
        dates = (start_date + " 00:00:00", end_date + " 23:59:59")
        query = f"""
                    SELECT *
                    FROM Load
                    WHERE date >= '{dates[0]}' AND date <= '{dates[1]}';
                """

        connection = sqlite3.connect(self.__train_data_base_name)
        data_frame = pd.read_sql_query(query, connection)
        connection.close()

        if ignore2020:
            data_frame['date'] = pd.to_datetime(data_frame['date'])
            data_frame = data_frame[~data_frame['date'].dt.year.isin([2020])]

        data_frame = data_frame.drop('index', axis=1)
        data_frame = data_frame.drop('name', axis=1)
        data_frame = data_frame.drop('date', axis=1)
        data_frame = data_frame.drop('solarradiation', axis=1)

        return data_frame

    def save_train_model_score(self, model_name, train_score_mape, test_score_mape, train_score_rmse, test_score_rmse):
        conn = sqlite3.connect(self.__train_score_data_base_name)
        cursor = conn.cursor()

        data = (model_name, train_score_mape, test_score_mape, train_score_rmse, test_score_rmse)
        insert_query = '''
        INSERT INTO modelScore (name, mape_train, mape_test, rmse_train, rmse_test)
        VALUES (?, ?, ?, ?, ?);
        '''

        cursor.execute(insert_query, data)
        conn.commit()
        conn.close()


    def save_processed_test_data(self, data_frame):
        connection = sqlite3.connect(self.__test_data_base_name)
        data_frame.to_sql(name='Load', con=connection, if_exists='replace')
        connection.close()

        return data_frame.shape[0]

    def load_last_day(self):
        dates = ("2021-09-06 00:00:00", "2021-09-06 23:00:00")
        query = f"""
                    SELECT date, avg_temp, load
                    FROM Load
                    WHERE date >= '{dates[0]}' AND date <= '{dates[1]}';
                 """
        
        connection = sqlite3.connect(self.__train_data_base_name)
        data_frame = pd.read_sql_query(query, connection)
        connection.close()

        return data_frame
    
    def load_test_data(self):
        query = f"""
                    SELECT *
                    FROM Load;
                """

        connection = sqlite3.connect(self.__test_data_base_name)
        data_frame = pd.read_sql_query(query, connection)
        connection.close()

        data_frame = data_frame.drop('index', axis=1)

        return data_frame

