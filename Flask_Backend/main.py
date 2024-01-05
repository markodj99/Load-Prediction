from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
from proccessData import invokeProccessing, loadDataFromDb
from trainData import trainModel

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30
CORS(app, origins="http://localhost:3000")
DATABASE_NAME = 'database/loadDataBase.db'

UPLOAD_FOLDER = os.path.join(app.root_path, 'rawTrainingData')
LOAD_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'loadData')
WEATHER_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'weatherData')
HOLIDAYS_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'holidays')


@app.route('/uploadTrainingFiles', methods=['POST'])
def uploadTrainingFiles():
    files = request.files.getlist('file')

    for file in files:
        safe_filename = re.sub(r'[\\/:"*?<>|]+', '_', file.filename)

        if 'Load' in safe_filename:
            file.save(os.path.join(LOAD_DATA_PATH, safe_filename))
        elif 'Weather' in safe_filename:
            file.save(os.path.join(WEATHER_DATA_PATH, safe_filename))
        elif 'Holidays' in safe_filename:
            file.save(os.path.join(HOLIDAYS_DATA_PATH, safe_filename))

    return jsonify({"num_received_files": len(files)})


@app.route('/prepareTrainingData', methods=['POST'])
def prepareTrainingData():
    invokeProccessing(LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH, DATABASE_NAME)
    return jsonify({"allGood": "all good"})


@app.route('/trainData', methods=['POST'])
def trainData():
    trainModel(loadDataFromDb(DATABASE_NAME), 0.85)
    return jsonify({"allGood": "all good"})


if __name__ == "__main__":
    app.run(debug = True)

