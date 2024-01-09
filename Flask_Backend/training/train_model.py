import time
from training.ann_regression import AnnRegression
from training.preparer import Preparer
from training.scorer import Scorer


def train_new_model(data_frame, share_for_training, model_name):
    number_of_columns = 20

    preparer = Preparer(data_frame, number_of_columns, share_for_training)
    trainX, trainY, testX, testY = preparer.prepare_for_training()

    ann_regression = AnnRegression()
    ann_regression.set_model_name(model_name)

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
        
