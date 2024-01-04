import time
from annRegression import AnnRegression
from preparer import Preparer
from scorer import Scorer

def trainModel(dataFrame, shareForTraining):
    NUMBER_OF_COLUMNS = 13

    preparer = Preparer(dataFrame, NUMBER_OF_COLUMNS, shareForTraining)
    trainX, trainY, testX, testY = preparer.prepare_for_training()

    ann_regression = AnnRegression()
    time_begin = time.time()
    trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)
    time_end = time.time()
    print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

    trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

    scorer = Scorer()
    trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
    print('Train Score: %.2f RMSE' % (trainScore))
    print('Test Score: %.2f RMSE' % (testScore))

