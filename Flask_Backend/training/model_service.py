import time
from training.ann_regression import AnnRegression
from training.preparer import Preparer
from training.scorer import Scorer
import numpy as np


class ModelService():

    def __init__(self, model_name, share_for_training, epoch_number):
        self.__model_name = model_name
        self.__share_for_training = share_for_training
        self.__epoch_number = epoch_number

    def train_new_model(self, data_frame):
        number_of_columns = data_frame.shape[1]

        preparer = Preparer(data_frame, number_of_columns, self.__share_for_training)
        trainX, trainY, testX, testY = preparer.prepare_for_training()

        ann_regression = AnnRegression()
        ann_regression.set_model_name(self.__model_name)
        ann_regression.set_number_of_train_columns(number_of_columns - 1)
        ann_regression.epoch_number = self.__epoch_number

        time_begin = time.time()
        trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
        time_end = time.time()

        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

        trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

        scorer = Scorer()

        trainScoreMape, testScoreMape = scorer.get_mape(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f%% MAPE' % (trainScoreMape))
        print('Test Score: %.2f%% MAPE' % (testScoreMape))

        trainScoreRmse, testScoreRmse = scorer.get_rmse(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScoreRmse))
        print('Test Score: %.2f RMSE' % (testScoreRmse))

        return trainScoreMape, testScoreMape, trainScoreRmse, testScoreRmse

    def test_model(self, last_day_train_data_frame, train_data_frame, test_data_frame):
        number_of_columns = test_data_frame.shape[1] - 3

        ann_regression = AnnRegression()
        ann_regression.set_model_name(self.__model_name)
        ann_regression.use_model_from_path()

        preparer = Preparer(train_data_frame, number_of_columns)
        preparer.fit_min_max_scaler()

        data_frame_segments = self.__split_test_data_frame(test_data_frame)

        for i in range(7):
            if i == 0:
                data_frame_segments[i].loc[:23, 'avg_temp_day_before'] = last_day_train_data_frame['avg_temp'].loc[0]
                data_frame_segments[i].loc[:23, 'load_day_before'] = last_day_train_data_frame.loc[:23, 'load'].values
                data_frame_segments[i].loc[:23, 'avg_load_day_before'] = last_day_train_data_frame.loc[:23, 'load'].mean()
            else:
                data_frame_segments[i]['load_day_before'] = data_frame_segments[i - 1]['load'].values
                data_frame_segments[i]['avg_load_day_before'] = data_frame_segments[i - 1]['load'].mean()

            test_data_frame = data_frame_segments[i].copy()
            test_data_frame = test_data_frame.drop('name', axis=1)
            test_data_frame = test_data_frame.drop('date', axis=1)
            test_data_frame = test_data_frame.drop('solarradiation', axis=1)

            preparer.init_for_predict(test_data_frame)
            test_data = preparer.prepare_for_predict()
            test_predict = ann_regression.get_test_predict(test_data)
            test_predict = preparer.inverse_transform_predict(test_predict)
            
            data_frame_segments[i]['load'] = test_predict

        return data_frame_segments
    
    def __split_test_data_frame(self, test_data_frame):
        segments = np.array_split(test_data_frame, 7)

        data_frame_segments = []
        for i, part_df in enumerate(segments):
            data_frame_segments.append(part_df)
        
        return data_frame_segments

