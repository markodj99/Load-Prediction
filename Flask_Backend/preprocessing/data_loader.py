import pandas as pd
import os


def invoke_data_loading(load_data_path, weather_data_path, holidays_data_path):
    data_frame = combine_data(load_data_path, weather_data_path)
    data_frame = remove_holidays(data_frame, holidays_data_path)

    return data_frame


def combine_data(load_data_path, weather_data_path):
    load_data_frame = load_load_data(load_data_path)
    load_data_frame = load_data_frame.reset_index(drop=True)

    weather_data_frame = load_weather_data(weather_data_path, load_data_frame['date'].min(), load_data_frame['date'].max())
    weather_data_frame = weather_data_frame.reset_index(drop=True)
    
    combined_data = pd.merge_asof(weather_data_frame, load_data_frame, on='date', direction='backward', tolerance=pd.Timedelta('0m'))
    combined_data = combined_data[combined_data['load'].notna()]
    combined_data = combined_data.reset_index(drop=True)

    return combined_data


def remove_holidays(data_frame, holidays_data_path):
    holidays = load_holidays(holidays_data_path)
    
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    holidays['date'] = pd.to_datetime(holidays['date'])

    data_frame['dateColumnPartial'] = data_frame['date'].dt.date
    holidays['dateColumnPartial'] = holidays['date'].dt.date

    data_frame = data_frame[~data_frame['dateColumnPartial'].isin(holidays['dateColumnPartial'])]
    data_frame = data_frame.drop('dateColumnPartial', axis=1)

    return data_frame


def load_load_data(load_data_path):
    data_frame = pd.DataFrame()

    for file_name in os.scandir(load_data_path):
        if file_name.is_file() and file_name.name.endswith('.csv'):
            data_frame_temp = pd.read_csv(file_name.path, engine='python', sep=',', header=0, usecols=[0, 2, 4], names=['date', 'name', 'load'])
            data_frame = pd.concat([data_frame, data_frame_temp], axis=0)

    data_frame = data_frame.loc[data_frame['name'] == 'N.Y.C.']
    data_frame = data_frame.drop('name', axis=1)
    data_frame = data_frame[data_frame['date'].str.endswith("00:00")]
    data_frame['date'] = pd.to_datetime(data_frame['date'], format='%m/%d/%Y %H:%M:%S')

    return data_frame


def load_weather_data(weather_data_path, min_date, max_date):
    data_frame = pd.DataFrame()

    for file_name in os.scandir(weather_data_path):
        if file_name.is_file() and file_name.name.endswith('.csv'):
            data_frame_temp = pd.read_csv(file_name.path, engine='python', sep=',', header=0,
            dtype={'datetime':str,'temp':float,'feelslike':float,'dew':float,'humidity':float,'precip':float,'precipprob':float,'preciptype':float,'snow':float,
                        'snowdepth':float,'windgust':float,'windspeed':float,'winddir':float,'sealevelpressure':float,'cloudcover':float,'visibility':float,'solarradiation':float,
                        'solarenergy':float,'uvindex':float,'severerisk':float,'conditions':str})

            data_frame = pd.concat([data_frame, data_frame_temp], axis=0)

    data_frame.rename(columns={'datetime':'date'}, inplace=True)
    data_frame['date'] = pd.to_datetime(data_frame['date'], format='%Y-%m-%dT%H:%M:%S')
    data_frame = data_frame.loc[data_frame['date'].between(min_date, max_date)]

    return data_frame


def load_holidays(holidays_data_path):
    data_frame = pd.DataFrame()

    for file_name in os.scandir(holidays_data_path):
        if file_name.is_file() and file_name.name.endswith('.xlsx'):
            data_frame = pd.read_excel(file_name.path, header=None, names=['nan', 'day', 'date', 'event'], skiprows=1)

    data_frame = data_frame.drop('day', axis=1)
    data_frame = data_frame.drop('event', axis=1)
    data_frame = data_frame.drop('nan', axis=1)
    data_frame = data_frame.dropna(subset=['date'])
    data_frame['date'] = pd.to_datetime(data_frame['date']).dt.strftime('%Y-%m-%d')

    return data_frame 

