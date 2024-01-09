import pandas as pd
import numpy as np


def invoke_preproccessing(training_data):
    training_data = remove_duplicates(training_data)
    training_data = drop_weather_features(training_data)
    training_data = interpolate_missing_values(training_data)
    training_data = fill_missing_temperature(training_data)
    training_data = create_season_column(training_data)
    training_data = create_day_type_column(training_data)
    training_data = normalize_missing_value(training_data)
    training_data = create_load_column_for_prev_day(training_data)
    training_data = create_hour_column(training_data)
    training_data = create_avg_temperature_column(training_data)
    training_data = create_avg_temperature_day_before_column(training_data)
    training_data = create_avg_load_day_before_column(training_data)

    return training_data


def remove_duplicates(data_frame):
    data_frame.sort_values(by='date', inplace=True)
    data_frame.drop_duplicates(subset='date', keep='last', inplace=True)
    data_frame.reset_index(drop=True, inplace=True)

    return data_frame


def drop_weather_features(data_frame):
    featureDrop = ['dew', 'precip', 'precipprob', 'preciptype', 'snow', 'snowdepth', 
                   'sealevelpressure', 'visibility', 'solarenergy',
                   'uvindex', 'severerisk', 'feelslike', 'windgust', 'winddir', 'conditions']
    data_frame = data_frame.drop(featureDrop, axis=1)

    return data_frame


def interpolate_missing_values(data_frame):
    data_frame['windspeed'] = data_frame['windspeed'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    data_frame['humidity'] = data_frame['humidity'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    data_frame['cloudcover'] = data_frame['cloudcover'].astype(float).interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
    data_frame['solarradiation'] = data_frame['solarradiation'].fillna(0)

    return data_frame


def fill_missing_temperature(data_frame):
    temp = data_frame.loc[data_frame['temp'] >= 122]
    temp = pd.concat([temp, data_frame.loc[data_frame['temp'] <= -23]])

    for index, row in temp.iterrows():
        temp_sum = data_frame.iloc[index-1]['temp'] + data_frame.iloc[index+1]['temp']
        new_temp = temp_sum / 2

        data_frame.at[index, 'temp'] = round(new_temp, 1)

    return data_frame
    

def create_season_column(data_frame):
    month = data_frame['date'].dt.month
    seasons = pd.DataFrame()
    seasons['seasons'] = month.apply(get_seasons)

    seasons_encoded = pd.get_dummies(seasons.seasons, prefix='season')

    for name in seasons_encoded.columns:
        data_frame.insert(1, name, seasons_encoded[name])

    return data_frame


def get_seasons(month):
    if month == 12 or month == 1 or month == 2:
        return 'winter'
    elif month == 3 or month == 4 or month == 5:
        return 'spring'
    elif month == 6 or month == 7 or month == 8:
        return 'summer'
    else:
        return 'autumn'


def create_day_type_column(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    
    data_frame.insert(5, 'monday', (data_frame['date'].dt.day_name() == 'Monday').astype(int))
    data_frame.insert(6, 'friday', (data_frame['date'].dt.day_name() == 'Friday').astype(int))
    data_frame.insert(7, 'saturday', (data_frame['date'].dt.day_name() == 'Saturday').astype(int))
    data_frame.insert(8, 'sunday', (data_frame['date'].dt.day_name() == 'Sunday').astype(int))
    data_frame.insert(9, 'othey_days', ((data_frame['date'].dt.day_name() != 'Monday') & 
                                       (data_frame['date'].dt.day_name() != 'Friday') & 
                                       (data_frame['date'].dt.day_name() != 'Saturday') & 
                                       (data_frame['date'].dt.day_name() != 'Sunday')).astype(int))

    return data_frame


def normalize_missing_value(data_frame):
    ratios = [ratio for ratio in (data_frame.isna().sum()/len(data_frame))]
    for pair in list(zip(data_frame.columns, ratios)):
        if pair[1] > 0:
            data_frame = data_frame.drop([pair[0]], axis=1)

    return data_frame


def create_load_column_for_prev_day(data_frame):
    data_frame = data_frame.reset_index(drop=True)
    data_frame.insert(16, column='load_day_before', value=data_frame['load'].shift(24))
    data_frame.loc[:23, 'load_day_before'] = data_frame.loc[:23, 'load']

    return data_frame


def create_regular_hour_column(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    data_frame['hour'] = data_frame['date'].dt.hour
    data_frame.insert(11, 'hour', data_frame.pop('hour'))   

    return data_frame


def create_hour_column(data_frame):
    seconds_in_day = 24*60*60

    hours = data_frame['date'].dt.hour
    seconds = hours.apply(lambda x: x*60*60)

    sin_date = np.sin(seconds*(2*np.pi/seconds_in_day))
    cos_time = np.cos(seconds*(2*np.pi/seconds_in_day))

    data_frame.insert(11, 'sin_hour', sin_date)
    data_frame.insert(12, 'cos_hour', cos_time)

    return data_frame


def create_avg_temperature_column(data_frame):
    data_frame.reset_index(drop=True, inplace=True)
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    data_frame['avg_temp'] = data_frame.groupby(data_frame['date'].dt.date)['temp'].transform('mean')
    data_frame.insert(14, 'avg_temp', data_frame.pop('avg_temp'))

    return data_frame


def create_avg_temperature_day_before_column(data_frame):
    data_frame.reset_index(drop=True, inplace=True)
    daily_avg_temp = data_frame.groupby(data_frame['date'].dt.date)['temp'].mean()
    data_frame['avg_temp_day_before'] = data_frame['date'].dt.date.map(daily_avg_temp.shift())

    data_frame.loc[:23, 'avg_temp_day_before'] = data_frame.loc[:23, 'temp'].mean()
    data_frame.insert(15, 'avg_temp_day_before', data_frame.pop('avg_temp_day_before'))

    return data_frame


def create_avg_load_day_before_column(data_frame):
    data_frame.reset_index(drop=True, inplace=True)
    daily_avg_load = data_frame.groupby(data_frame['date'].dt.date)['load'].mean()
    data_frame['avg_load_day_before'] = data_frame['date'].dt.date.map(daily_avg_load.shift())

    data_frame.loc[:23, 'avg_load_day_before'] = data_frame.loc[:23, 'load'].mean()
    data_frame.insert(21, 'avg_load_day_before', data_frame.pop('avg_load_day_before'))

    return data_frame

