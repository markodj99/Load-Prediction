from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30
CORS(app, origins="http://localhost:3000")

@app.route("/test", methods=["GET"])
def test():
    return {"test1" : ["test1"], "test2" : ["test2"]}


@app.route('/uploadTrainingFiles', methods=['POST'])
def upload_training_files():
    upload_folder = os.path.join(app.root_path, 'rawTrainingData')

    loadDataPath = os.path.join(upload_folder, 'loadData')
    watherDataPath = os.path.join(upload_folder, 'weatherData')
    holidayDataPath = os.path.join(upload_folder, 'holidays')

    files = request.files.getlist('file')

    for file in files:
        safe_filename = get_safe_filename(file.filename)

        if 'Load' in safe_filename:
            file.save(os.path.join(loadDataPath, safe_filename))
        elif 'Weather' in safe_filename:
            file.save(os.path.join(watherDataPath, safe_filename))
        elif 'Holidays' in safe_filename:
            file.save(os.path.join(holidayDataPath, safe_filename))

    return jsonify({"num_received_files": len(files)})


def get_safe_filename(filename):
    return re.sub(r'[\\/:"*?<>|]+', '_', filename)


if __name__ == "__main__":
    app.run(debug = True)

