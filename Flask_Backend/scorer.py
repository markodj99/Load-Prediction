import math
from sklearn.metrics import mean_squared_error
import numpy as np


class Scorer:
        
    def get_mape(self, trainY, trainPredict, testY, testPredict):
        trainY, trainPredict = np.array(trainY), np.array(trainPredict)
        testY, testPredict = np.array(testY), np.array(testPredict)

        trainResult = np.mean(np.abs((trainY - trainPredict) / trainY)) * 100
        testResult = np.mean(np.abs((testY - testPredict) / testY)) * 100
        
        return trainResult, testResult