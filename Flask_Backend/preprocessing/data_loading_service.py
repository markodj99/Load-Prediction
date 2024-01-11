import pandas as pd
import os


class DataLoaderService():

    def __init__(self, load_data_path, weather_data_path, holidays_data_path, test_data_path):
        self.__load_data_path = load_data_path
        self.__weather_data_path = weather_data_path
        self.__holidays_data_path = holidays_data_path
        self.__test_data_path = test_data_path

    def get_test_data_frame(self):
        test_data_frame = self.__load_weather_data(self.__test_data_path)
        test_data_frame = test_data_frame.reset_index(drop=True)

        return test_data_frame

    def get_train_data_frame(self):
        load_data_frame = self.__load_load_data()
        load_data_frame = load_data_frame.reset_index(drop=True)

        weather_data_frame = self.__load_weather_data(self.__weather_data_path)
        weather_data_frame = weather_data_frame.loc[weather_data_frame['date'].between(load_data_frame['date'].min(), load_data_frame['date'].max())]
        weather_data_frame = weather_data_frame.reset_index(drop=True)

        holidays_data_frame = self.__load_holidays()

        combined_data_frame = pd.merge_asof(weather_data_frame, load_data_frame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
        combined_data_frame = combined_data_frame[combined_data_frame['load'].notna()]
        combined_data_frame = combined_data_frame.reset_index(drop=True)

        combined_data_frame = self.__remove_holidays(combined_data_frame, holidays_data_frame)

        return combined_data_frame

    def __load_load_data(self):
        data_frame = pd.DataFrame()

        for file_name in os.scandir(self.__load_data_path):
            if file_name.is_file() and file_name.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(file_name.path, engine='python', sep=',', header=0, usecols=[0, 2, 4], names=['date', 'name', 'load'])
                data_frame = pd.concat([data_frame, data_frame_temp], axis=0)

        data_frame = data_frame.loc[data_frame['name'] == 'N.Y.C.']
        data_frame = data_frame.drop('name', axis=1)
        data_frame = data_frame[data_frame['date'].str.endswith("00:00")]
        data_frame['date'] = pd.to_datetime(data_frame['date'], format='%m/%d/%Y %H:%M:%S')

        return data_frame
    
    def __load_weather_data(self, path):
        data_frame = pd.DataFrame()

        for file_name in os.scandir(path):
            if file_name.is_file() and file_name.name.endswith('.csv'):
                data_frame_temp = pd.read_csv(file_name.path, engine='python', sep=',', header=0,
                dtype={'datetime':str,'temp':float,'feelslike':float,'dew':float,'humidity':float,'precip':float,'precipprob':float,'preciptype':float,'snow':float,
                            'snowdepth':float,'windgust':float,'windspeed':float,'winddir':float,'sealevelpressure':float,'cloudcover':float,'visibility':float,'solarradiation':float,
                            'solarenergy':float,'uvindex':float,'severerisk':float,'conditions':str})

                data_frame = pd.concat([data_frame, data_frame_temp], axis=0)

        data_frame.rename(columns={'datetime':'date'}, inplace=True)
        data_frame['date'] = pd.to_datetime(data_frame['date'], format='%Y-%m-%dT%H:%M:%S')

        return data_frame
    
    def __load_holidays(self):
        data_frame = pd.DataFrame()

        for file_name in os.scandir(self.__holidays_data_path):
            if file_name.is_file() and file_name.name.endswith('.xlsx'):
                data_frame = pd.read_excel(file_name.path, header=None, names=['nan', 'day', 'date', 'event'], skiprows=1)

        data_frame = data_frame.drop('day', axis=1)
        data_frame = data_frame.drop('event', axis=1)
        data_frame = data_frame.drop('nan', axis=1)
        data_frame = data_frame.dropna(subset=['date'])
        data_frame['date'] = pd.to_datetime(data_frame['date']).dt.strftime('%Y-%m-%d')

        return data_frame 
    
    def __remove_holidays(self, combined_data_frame, holidays_data_frame):
        combined_data_frame['date'] = pd.to_datetime(combined_data_frame['date'])
        holidays_data_frame['date'] = pd.to_datetime(holidays_data_frame['date'])

        combined_data_frame['dateColumnPartial'] = combined_data_frame['date'].dt.date
        holidays_data_frame['dateColumnPartial'] = holidays_data_frame['date'].dt.date

        combined_data_frame = combined_data_frame[~combined_data_frame['dateColumnPartial'].isin(holidays_data_frame['dateColumnPartial'])]
        combined_data_frame = combined_data_frame.drop('dateColumnPartial', axis=1)

        return combined_data_frame

