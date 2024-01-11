import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Preparer:
    
    def __init__(self, data_frame, number_of_columns, share_for_training=0.80):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.dataset_values = data_frame.values
        self.dataset_values = self.dataset_values.astype('float32')

        self.number_of_columns = number_of_columns
        self.predictor_column_no = self.number_of_columns - 1
        self.share_for_training = share_for_training
    
    def prepare_for_training(self):
        dataset = self.scaler.fit_transform(self.dataset_values)

        train_size = int(len(dataset) * self.share_for_training)
        train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

        trainX, trainY = self.create_dataset(train, self.number_of_columns)
        testX, testY = self.create_dataset(test, self.number_of_columns)

        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY

        return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()

    def inverse_transform(self, train_predict, test_predict):
        train_predict = np.reshape(train_predict, (train_predict.shape[0], train_predict.shape[1]))
        test_predict = np.reshape(test_predict, (test_predict.shape[0], test_predict.shape[1]))

        self.trainX = np.reshape(self.trainX, (self.trainX.shape[0], self.trainX.shape[2]))
        self.testX = np.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))

        trainXAndPredict = np.concatenate((self.trainX, train_predict),axis=1)
        testXAndPredict = np.concatenate((self.testX, test_predict),axis=1)

        trainY = np.reshape(self.trainY, (self.trainY.shape[0], 1))
        testY = np.reshape(self.testY, (self.testY.shape[0], 1))

        trainXAndY = np.concatenate((self.trainX, trainY),axis=1)
        testXAndY = np.concatenate((self.testX, testY),axis=1)

        trainXAndPredict = self.scaler.inverse_transform(trainXAndPredict)
        trainXAndY = self.scaler.inverse_transform(trainXAndY)

        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
        testXAndY = self.scaler.inverse_transform(testXAndY)

        train_predict = trainXAndPredict[:,self.predictor_column_no]
        trainY = trainXAndY[:,self.predictor_column_no]
        test_predict = testXAndPredict[:,self.predictor_column_no]
        testY = testXAndY[:,self.predictor_column_no]

        return train_predict, trainY, test_predict, testY
    
    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []

        for i in range(len(dataset) - 1):
            a = dataset[i, 0:look_back - 1]
            dataX.append(a)
            dataY.append(dataset[i, look_back - 1])

        return np.array(dataX), np.array(dataY)

    def prepare_for_predict(self):
        normalized_data = self.scaler.transform(self.dataset_values)

        testX = self.create_dataset_for_predict(normalized_data, self.number_of_columns)
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        self.testX = testX

        return testX.copy()

    def inverse_transform_predict(self, test_predict):
        test_predict = np.reshape(test_predict, (test_predict.shape[0], test_predict.shape[1]))
        self.testX = np.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))

        testXAndPredict = np.concatenate((self.testX, test_predict),axis=1)
        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)

        test_predict = testXAndPredict[:,self.predictor_column_no]

        return test_predict

    def create_dataset_for_predict(self, dataset, look_back):
        dataX = []

        for i in range(len(dataset)):
            a = dataset[i, 0:look_back - 1]
            dataX.append(a)

        return np.array(dataX)

    def fit_min_max_scaler(self):
        self.scaler.fit(self.dataset_values)

    def init_for_predict(self, data_frame):
        self.dataset_values = data_frame.values
        self.dataset_values = self.dataset_values.astype('float32')

