import time
from training.annRegression import AnnRegression
from training.preparer import Preparer
from training.scorer import Scorer


def trainModel(dataFrame, shareForTraining, modelName):
    numberOfColumns = 20

    preparer = Preparer(dataFrame, numberOfColumns, shareForTraining)
    trainX, trainY, testX, testY = preparer.prepare_for_training()

    ann_regression = AnnRegression()
    ann_regression.set_model_name(modelName)

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
        
