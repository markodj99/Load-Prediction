import re
import os
from preprocessing.data_preprocessing_service import DataProcessingService
from preprocessing.data_loading_service import DataLoaderService
from database.data_base_service import DataBaseService
from training.model_service import ModelService
from datetime import datetime
from time import time
import pandas as pd


class InvokerService():

    def __init__(self, 
                 load_data_path, weather_data_path, holidays_data_path, test_data_path,
                 output_path,
                 train_data_base_name, train_score_data_base_name, test_data_base_name,
                 model_name, share_for_training, epoch_number):
        
        self.__model_name = model_name

        self.__load_data_path = load_data_path
        self.__weather_data_path = weather_data_path
        self.__holidays_data_path = holidays_data_path
        self.__test_data_path = test_data_path

        self.__output_path = output_path

        self.__data_loader_service = DataLoaderService(load_data_path, weather_data_path, holidays_data_path, test_data_path)
        self.__data_processing_service = DataProcessingService()
        self.__data_base_service = DataBaseService(train_data_base_name, train_score_data_base_name, test_data_base_name)
        self.__model_service = ModelService(model_name, share_for_training, epoch_number)

    def upload_training_files(self, files):
        for file in files:
            safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)

            if 'Load' in safe_filename:
                file.save(os.path.join(self.__load_data_path, safe_filename))
            elif 'Weather' in safe_filename:
                file.save(os.path.join(self.__weather_data_path , safe_filename))
            elif 'Holidays' in safe_filename:
                file.save(os.path.join(self.__holidays_data_path, safe_filename))

        return len(files)

    def prepare_training_data(self):
        data_frame = self.__data_loader_service.get_train_data_frame()
        data_frame = self.__data_processing_service.get_processed_train_data(data_frame)
        response = self.__data_base_service.save_processed_train_data(data_frame)

        return response

    def train_model(self, start_date, end_date):
        if datetime(2018, 1, 2, 0, 0, 0) > datetime.strptime(start_date, '%Y-%m-%d'): start_date, end_date = '2018-01-02', '2021-09-06'
        if datetime.strptime(end_date, '%Y-%m-%d') > datetime(2021, 9, 6, 23, 59, 59): start_date, end_date = '2018-01-02', '2021-09-06'
        if datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'): start_date, end_date = '2018-01-02', '2021-09-06'
    
        data_frame = self.__data_base_service.load_training_data(start_date, end_date)
        train_score_mape, test_score_mape, train_score_rmse, test_score_rmse, total_time = self.__model_service.train_new_model(data_frame)
        self.__data_base_service.save_train_model_score(self.__model_name, train_score_mape, test_score_mape, train_score_rmse, test_score_rmse)

        return train_score_mape, test_score_mape, train_score_rmse, test_score_rmse, total_time

    def upload_and_prepare_test_files(self, files):
        self.__upload_test_files(files)
        data_frame = self.__data_loader_service.get_test_data_frame()
        data_frame = self.__data_processing_service.get_processed_test_data(data_frame)
        response = self.__data_base_service.save_processed_test_data(data_frame)

        return response

    def __upload_test_files(self, files):
        for file in files:
            safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)
            file.save(os.path.join(self.__test_data_path, safe_filename))

    def test_model(self):
        last_day_train_data_frame = self.__data_base_service.load_last_day()
        train_data_frame = self.__data_base_service.load_training_data('2018-01-02', '2021-09-06')
        test_data_frame = self.__data_base_service.load_test_data()

        test_data_frame_segments = self.__model_service.test_model(last_day_train_data_frame, train_data_frame, test_data_frame)

        test_data_frame = pd.concat(test_data_frame_segments, ignore_index=True)

        _ = self.__data_base_service.save_processed_test_data(test_data_frame)
        self.__write_test_results_to_csv(test_data_frame)

        predicted_load = {
            'day1': {'date':[test_data_frame_segments[0]['date'].tolist()], 'load':[test_data_frame_segments[0]['load'].tolist()]},
            'day2': {'date':[test_data_frame_segments[1]['date'].tolist()], 'load':[test_data_frame_segments[1]['load'].tolist()]},
            'day3': {'date':[test_data_frame_segments[2]['date'].tolist()], 'load':[test_data_frame_segments[2]['load'].tolist()]},
            'day4': {'date':[test_data_frame_segments[3]['date'].tolist()], 'load':[test_data_frame_segments[3]['load'].tolist()]},
            'day5': {'date':[test_data_frame_segments[4]['date'].tolist()], 'load':[test_data_frame_segments[4]['load'].tolist()]},
            'day6': {'date':[test_data_frame_segments[5]['date'].tolist()], 'load':[test_data_frame_segments[5]['load'].tolist()]},
            'day7': {'date':[test_data_frame_segments[6]['date'].tolist()], 'load':[test_data_frame_segments[6]['load'].tolist()]}
        }

        return predicted_load

    def __write_test_results_to_csv(self, test_data_frame):
        data_frame = pd.DataFrame()
        data_frame['date'] = test_data_frame['date']
        data_frame['load'] = test_data_frame['load']
        data_frame.to_csv(f'{self.__output_path}/output_{int(time())}.csv', index=False)
        #data_frame.to_csv(f'{self.__output_path}/Marko_Djurdjevic_5.csv', index=False)

