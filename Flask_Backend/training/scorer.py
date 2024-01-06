import math
from sklearn.metrics import mean_squared_error
import numpy as np


class Scorer:
        
    def get_rmse(self, trainY, trainPredict, testY, testPredict):
        trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
        testScore = math.sqrt(mean_squared_error(testY, testPredict))
        return trainScore, testScore

    def get_mape(self, trainY, trainPredict, testY, testPredict):
        trainY, trainPredict = np.array(trainY), np.array(trainPredict)
        testY, testPredict = np.array(testY), np.array(testPredict)

        trainResult = np.mean(np.abs((trainY - trainPredict) / trainY)) * 100
        testResult = np.mean(np.abs((testY - testPredict) / testY)) * 100
        
        return trainResult, testResult
    
