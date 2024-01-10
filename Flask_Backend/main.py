from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from service import InvokerService

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30
CORS(app, origins="http://localhost:3000")

UPLOAD_FOLDER = os.path.join(app.root_path, 'raw_training_data')
LOAD_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'load_data')
WEATHER_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'weather_data')
HOLIDAYS_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'holidays_data')
TEST_DATA_PATH = os.path.join(app.root_path, 'raw_test_data')

SERVICE = InvokerService(LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH, TEST_DATA_PATH,
                         'database/trainDataDb.db','database/modelTrainScoreDb.db', 'database/testDataDb.db', 'database/modelTestScoreDb.db',
                         'testtest', 0.8)


@app.route('/upload_training_files', methods=['POST'])
def upload_training_files():
    response = SERVICE.upload_training_files(request.files.getlist('file'))
    return jsonify({"num_received_files": response})


@app.route('/prepare_training_data', methods=['POST'])
def prepare_training_data():
    response = SERVICE.prepare_training_data()
    return jsonify({"num_processed_writen_instance": response})


@app.route('/train_model', methods=['POST'])
def train_model():
    response = SERVICE.train_model(request.form.get('startDate')[:10], request.form.get('endDate')[:10])
    return jsonify(response)


@app.route('/upload_and_prepare_training_files', methods=['POST'])
def upload_and_prepare_training_files():
    response = SERVICE.upload_and_prepare_training_files(request.files.getlist('file'))
    return jsonify({"num_processed_and_writen_instance": response})


@app.route('/test_model', methods=['POST'])
def test_model():
    return '1'


if __name__ == "__main__":
    app.run(debug = True)

