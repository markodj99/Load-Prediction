from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
from proccessData import invokeProccessing


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30
CORS(app, origins="http://localhost:3000")
DATABASE_NAME = 'database/loadDataBase.db'


@app.route('/uploadTrainingFiles', methods=['POST'])
def uploadTrainingFiles():
    upload_folder = os.path.join(app.root_path, 'rawTrainingData')

    loadDataPath = os.path.join(upload_folder, 'loadData')
    watherDataPath = os.path.join(upload_folder, 'weatherData')
    holidayDataPath = os.path.join(upload_folder, 'holidays')

    files = request.files.getlist('file')

    for file in files:
        safe_filename = getSafeFilename(file.filename)

        if 'Load' in safe_filename:
            file.save(os.path.join(loadDataPath, safe_filename))
        elif 'Weather' in safe_filename:
            file.save(os.path.join(watherDataPath, safe_filename))
        elif 'Holidays' in safe_filename:
            file.save(os.path.join(holidayDataPath, safe_filename))

    return jsonify({"num_received_files": len(files)})


@app.route('/prepareTrainingData', methods=['POST'])
def prepareTrainingData():
    upload_folder = os.path.join(app.root_path, 'rawTrainingData')
    loadDataPath = os.path.join(upload_folder, 'loadData')
    weatherDataPath = os.path.join(upload_folder, 'weatherData')
    holidaysDataPath = os.path.join(upload_folder, 'holidays')

    trainingData = invokeProccessing(loadDataPath, weatherDataPath, holidaysDataPath, DATABASE_NAME)
    print(trainingData)

    return jsonify({"allGood": "all good"})


def getSafeFilename(filename):
    return re.sub(r'[\\/:"*?<>|]+', '_', filename)


if __name__ == "__main__":
    app.run(debug = True)
