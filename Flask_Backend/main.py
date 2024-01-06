from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from utills import uploadTrainingFilesUtil
from preprocessing.dataLoader import invokeDataLoading
from preprocessing.preprocessData import invokePreproccessing
from database.dataBaseFuncs import *
from training.trainData import trainModel


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30

CORS(app, origins="http://localhost:3000")

DATABASE_LOAD_NAME = 'database/loadDataBase.db'
DATABASE_MODEL_SCORE_NAME = 'database/modelScore.db'

UPLOAD_FOLDER = os.path.join(app.root_path, 'rawTrainingData')
LOAD_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'loadData')
WEATHER_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'weatherData')
HOLIDAYS_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'holidays')

SHARE_FOR_TRAINING = 0.8
MODEL_NAME = "e150bs1w2020sft080"


@app.route('/uploadTrainingFiles', methods=['POST'])
def uploadTrainingFiles():
    response = uploadTrainingFilesUtil(request.files.getlist('file'), LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH)
    return jsonify(response)


@app.route('/prepareTrainingData', methods=['POST'])
def prepareTrainingData():
    dataFrame = invokeDataLoading(LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH)
    dataFrame = invokePreproccessing(dataFrame)
    response = saveProcessedDataToDb(dataFrame, DATABASE_LOAD_NAME)

    return jsonify({"num_processed_writen_instance": response})


@app.route('/trainData', methods=['POST'])
def trainData():
    dataFrame = loadDataFromDb(DATABASE_LOAD_NAME)

    trainScoreMape, testScoreMape, trainScoreRmse, testScoreRmse = trainModel(dataFrame, SHARE_FOR_TRAINING, MODEL_NAME)
    response = jsonify({"trainScoreMape": trainScoreMape, "testScoreMape": testScoreMape, 
                        "trainScoreRmse": trainScoreRmse, "testScoreRmse": testScoreRmse})

    saveModelScoreData(MODEL_NAME, trainScoreMape, testScoreMape, trainScoreRmse, testScoreRmse, DATABASE_MODEL_SCORE_NAME)

    return response


if __name__ == "__main__":
    app.run(debug = True)

