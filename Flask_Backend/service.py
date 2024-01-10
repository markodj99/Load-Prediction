import re
import os
from preprocessing.data_loader import DataLoaderService
from preprocessing.preprocess_data import DataProcessingService
from database.data_base_handler import DataBaseService
from training.train_model import TrainModelService
from datetime import datetime


class InvokerService():

    def __init__(self, 
                 load_data_path, weather_data_path, holidays_data_path, test_data_path, 
                 train_data_base_name, train_score_data_base_name, test_data_base_name, test_score_data_base_name,
                 model_name, share_for_training):
        self.__model_name = model_name

        self.__load_data_path = load_data_path
        self.__weather_data_path = weather_data_path
        self.__holidays_data_path = holidays_data_path
        self.__test_data_path = test_data_path

        self.__data_loader_service = DataLoaderService(load_data_path, weather_data_path, holidays_data_path, test_data_path)
        self.__data_processing_service = DataProcessingService()
        self.__data_base_service = DataBaseService(train_data_base_name, train_score_data_base_name, test_data_base_name, test_score_data_base_name)
        self.__model_service = TrainModelService(model_name, share_for_training)

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
        response = self.__data_base_service.save_processed_test_data(data_frame)

        return response

    def train_model(self, start_date, end_date):
        if datetime(2018, 1, 2, 0, 0, 0) > datetime.strptime(start_date, '%Y-%m-%d'): start_date = '2018-02-01'
        if datetime.strptime(end_date, '%Y-%m-%d') > datetime(2021, 9, 6, 23, 59, 59): end_date = '2021-08-06'
        if datetime.strptime(start_date, '%Y-%m-%d') > datetime.strptime(end_date, '%Y-%m-%d'): start_date, end_date = '2018-02-01', '2021-08-06'
    
        data_frame = self.__data_base_service.load_training_data(start_date, end_date)
        train_score_mape, test_score_mape, train_score_rmse, test_score_rmse = self.__model_service.train_new_model(data_frame)
        self.__data_base_service.save_train_model_score(self.__model_name, train_score_mape, test_score_mape, train_score_rmse, test_score_rmse)

        return {"train_score_mape": train_score_mape, "test_score_mape": test_score_mape, 
                "train_score_rmse": train_score_rmse, "test_score_rmse": test_score_rmse}

    def upload_and_prepare_training_files(self, files):
        self.__upload_test_files(files)
        data_frame = self.__data_loader_service.get_test_data_frame()
        data_frame = self.__data_processing_service.get_processed_test_data(data_frame)
        response = self.__data_base_service.save_processed_train_data(data_frame)

        return response

    def __upload_test_files(self, files):
        for file in files:
            safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)
            file.save(os.path.join(self.__test_data_path, safe_filename))