import pandas as pd
import numpy as np


class DataProcessingService():

    def __init__(self):
        pass

    def get_processed_train_data(self, train_data_frame):
        train_data_frame = self.__remove_duplicates(train_data_frame)
        train_data_frame = self.__drop_weather_features(train_data_frame)
        train_data_frame = self.__interpolate_missing_values(train_data_frame)
        train_data_frame = self.__fill_missing_temperature(train_data_frame)
        train_data_frame = self.__create_month_column(train_data_frame)
        train_data_frame = self.__create_day_type_column(train_data_frame)
        train_data_frame = self.__normalize_missing_value(train_data_frame)
        train_data_frame = self.__create_load_column_for_prev_day(train_data_frame)
        train_data_frame = self.__create_hour_column(train_data_frame)
        train_data_frame = self.__create_avg_temperature_column(train_data_frame)
        train_data_frame = self.__create_avg_temperature_day_before_column(train_data_frame)
        train_data_frame = self.__create_avg_load_day_before_column(train_data_frame)

        return train_data_frame
    
    def get_processed_test_data(self, test_data_frame):
        test_data_frame = self.__remove_duplicates(test_data_frame)
        test_data_frame = self.__drop_weather_features(test_data_frame)
        test_data_frame = self.__interpolate_missing_values(test_data_frame, False)
        test_data_frame = self.__fill_missing_temperature(test_data_frame)
        test_data_frame = self.__create_month_column(test_data_frame)
        test_data_frame = self.__create_day_type_column(test_data_frame)
        test_data_frame = self.__normalize_missing_value(test_data_frame)

        load_day_before = pd.Series([-1.0] * len(test_data_frame), name='load_day_before')
        test_data_frame.insert(14, 'load_day_before', load_day_before)
        
        test_data_frame = self.__create_hour_column(test_data_frame)
        test_data_frame = self.__create_avg_temperature_column(test_data_frame)
        test_data_frame = self.__create_avg_temperature_day_before_column(test_data_frame)

        avg_load_day_before = pd.Series([-1.0] * len(test_data_frame), name='avg_load_day_before')
        test_data_frame.insert(19, 'avg_load_day_before', avg_load_day_before)

        load = pd.Series([5825.0788936801] * len(test_data_frame), name='load')
        test_data_frame['load'] = load

        return test_data_frame

    def __remove_duplicates(self, data_frame):
        data_frame.sort_values(by='date', inplace=True)
        data_frame.drop_duplicates(subset='date', keep='last', inplace=True)
        data_frame.reset_index(drop=True, inplace=True)

        return data_frame

    def __drop_weather_features(self, data_frame):
        featureDrop = ['dew', 'precip', 'precipprob', 'preciptype', 'snow', 'snowdepth', 
                    'sealevelpressure', 'visibility', 'solarenergy',
                    'uvindex', 'severerisk', 'feelslike', 'windgust', 'winddir', 'conditions']
        data_frame = data_frame.drop(featureDrop, axis=1)

        return data_frame

    def __interpolate_missing_values(self, data_frame, interpolate_load = True):
        data_frame['windspeed'] = data_frame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['humidity'] = data_frame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['cloudcover'] = data_frame['cloudcover'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
        data_frame['solarradiation'] = data_frame['solarradiation'].fillna(0)

        if interpolate_load:
            data_frame['load'] = data_frame['load'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")

        return data_frame

    def __fill_missing_temperature(self, data_frame):
        temp = data_frame.loc[data_frame['temp'] >= 122]
        temp = pd.concat([temp, data_frame.loc[data_frame['temp'] <= -23]])

        for index, row in temp.iterrows():
            temp_sum = data_frame.iloc[index-1]['temp'] + data_frame.iloc[index+1]['temp']
            new_temp = temp_sum / 2

            data_frame.at[index, 'temp'] = round(new_temp, 1)

        return data_frame
    
    def __create_month_column(self, train_data_frame):
        month = train_data_frame['date'].dt.month

        sin_month = np.sin(month*(2.*np.pi/12))
        cos_month = np.cos(month*(2.*np.pi/12))

        train_data_frame.insert(1, 'sin_month', sin_month)
        train_data_frame.insert(1, 'cos_month', cos_month)

        return train_data_frame

    def __create_day_type_column(self, data_frame):
        data_frame['date'] = pd.to_datetime(data_frame['date'])
        
        data_frame.insert(3, 'monday', (data_frame['date'].dt.day_name() == 'Monday').astype(int))
        data_frame.insert(4, 'friday', (data_frame['date'].dt.day_name() == 'Friday').astype(int))
        data_frame.insert(5, 'saturday', (data_frame['date'].dt.day_name() == 'Saturday').astype(int))
        data_frame.insert(6, 'sunday', (data_frame['date'].dt.day_name() == 'Sunday').astype(int))
        data_frame.insert(7, 'othey_days', ((data_frame['date'].dt.day_name() != 'Monday') & 
                                        (data_frame['date'].dt.day_name() != 'Friday') & 
                                        (data_frame['date'].dt.day_name() != 'Saturday') & 
                                        (data_frame['date'].dt.day_name() != 'Sunday')).astype(int))

        return data_frame

    def __normalize_missing_value(self, data_frame):
        ratios = [ratio for ratio in (data_frame.isna().sum()/len(data_frame))]
        for pair in list(zip(data_frame.columns, ratios)):
            if pair[1] > 0:
                data_frame = data_frame.drop([pair[0]], axis=1)

        return data_frame

    def __create_load_column_for_prev_day(self, data_frame):
        data_frame = data_frame.reset_index(drop=True)
        data_frame.insert(14, column='load_day_before', value=data_frame['load'].shift(24))
        data_frame.loc[:23, 'load_day_before'] = data_frame.loc[:23, 'load']

        return data_frame

    def __create_hour_column(self, data_frame):
        seconds_in_day = 24*60*60

        hours = data_frame['date'].dt.hour
        seconds = hours.apply(lambda x: x*60*60)

        sin_date = np.sin(seconds*(2*np.pi/seconds_in_day))
        cos_time = np.cos(seconds*(2*np.pi/seconds_in_day))

        data_frame.insert(9, 'sin_hour', sin_date)
        data_frame.insert(10, 'cos_hour', cos_time)

        return data_frame

    def __create_avg_temperature_column(self, data_frame):
        data_frame.reset_index(drop=True, inplace=True)
        data_frame['date'] = pd.to_datetime(data_frame['date'])
        data_frame['avg_temp'] = data_frame.groupby(data_frame['date'].dt.date)['temp'].transform('mean')
        data_frame.insert(12, 'avg_temp', data_frame.pop('avg_temp'))

        return data_frame

    def __create_avg_temperature_day_before_column(self, data_frame):
        data_frame.reset_index(drop=True, inplace=True)
        daily_avg_temp = data_frame.groupby(data_frame['date'].dt.date)['temp'].mean()
        data_frame['avg_temp_day_before'] = data_frame['date'].dt.date.map(daily_avg_temp.shift())

        data_frame.loc[:23, 'avg_temp_day_before'] = data_frame.loc[:23, 'temp'].mean()
        data_frame.insert(13, 'avg_temp_day_before', data_frame.pop('avg_temp_day_before'))

        return data_frame

    def __create_avg_load_day_before_column(self, data_frame):
        data_frame.reset_index(drop=True, inplace=True)
        daily_avg_load = data_frame.groupby(data_frame['date'].dt.date)['load'].mean()
        data_frame['avg_load_day_before'] = data_frame['date'].dt.date.map(daily_avg_load.shift())

        data_frame.loc[:23, 'avg_load_day_before'] = data_frame.loc[:23, 'load'].mean()
        data_frame.insert(19, 'avg_load_day_before', data_frame.pop('avg_load_day_before'))

        return data_frame

