from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from utills import upload_training_files_util
from preprocessing.data_loader import invoke_data_loading
from preprocessing.preprocess_data import invoke_preproccessing
from database.data_base_handler import *
from training.train_model import train_new_model


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30

CORS(app, origins="http://localhost:3000")

DATABASE_LOAD_NAME = 'database/loadDataBase.db'
DATABASE_MODEL_SCORE_NAME = 'database/modelScore.db'

UPLOAD_FOLDER = os.path.join(app.root_path, 'raw_training_data')
LOAD_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'load_data')
WEATHER_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'weather_data')
HOLIDAYS_DATA_PATH = os.path.join(UPLOAD_FOLDER, 'holidays_data')

SHARE_FOR_TRAINING = 0.8
MODEL_NAME = "testtesttest"


@app.route('/upload_training_files', methods=['POST'])
def upload_training_files():
    response = upload_training_files_util(request.files.getlist('file'), LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH)
    return jsonify(response)


@app.route('/prepare_training_data', methods=['POST'])
def prepare_training_data():
    data_frame = invoke_data_loading(LOAD_DATA_PATH, WEATHER_DATA_PATH, HOLIDAYS_DATA_PATH)
    data_frame = invoke_preproccessing(data_frame)
    response = save_processed_data_to_db(data_frame, DATABASE_LOAD_NAME)

    return jsonify({"num_processed_writen_instance": response})


@app.route('/train_model', methods=['POST'])
def train_model():
    start_date = request.form.get('startDate')[:10]
    end_date = request.form.get('endDate')[:10]
    data_frame = load_training_data_from_db(DATABASE_LOAD_NAME, start_date, end_date)

    train_score_mape, test_score_mape, train_score_rmse, test_score_rmse = train_new_model(data_frame, SHARE_FOR_TRAINING, MODEL_NAME)
    response = jsonify({"train_score_mape": train_score_mape, "test_score_mape": test_score_mape, 
                        "train_score_rmse": train_score_rmse, "test_score_rmse": test_score_rmse})

    save_model_score_data(MODEL_NAME, train_score_mape, test_score_mape, train_score_rmse, test_score_rmse, DATABASE_MODEL_SCORE_NAME)

    return response


@app.route('/upload_and_prepare_training_files', methods=['POST'])
def upload_and_prepare_training_files():
    return '1'


@app.route('/test_model', methods=['POST'])
def test_model():
    return '1'


if __name__ == "__main__":
    app.run(debug = True)

