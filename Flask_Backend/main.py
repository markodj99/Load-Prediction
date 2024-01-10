from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from service import InvokerService

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['REQUEST_TIMEOUT'] = 30
CORS(app, origins="http://localhost:3000")

SERVICE = InvokerService(load_data_path=os.path.join(app.root_path, 'raw_training_data', 'load_data'), 
                         weather_data_path=os.path.join(app.root_path, 'raw_training_data', 'weather_data'), 
                         holidays_data_path=os.path.join(app.root_path, 'raw_training_data', 'holidays_data'),
                         test_data_path=os.path.join(app.root_path, 'raw_test_data'),
                         train_data_base_name='database/trainDataDb.db',
                         train_score_data_base_name='database/modelTrainScoreDb.db',
                         test_data_base_name='database/testDataDb.db',
                         test_score_data_base_name='database/modelTestScoreDb.db',
                         model_name='e120bs1_new',
                         share_for_training=0.8,
                         epoch_number=120)


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
    trsm, tssm, trsr, tssr  = SERVICE.train_model(request.form.get('startDate')[:10], request.form.get('endDate')[:10])
    return {"train_score_mape": trsm, "test_score_mape": tssm, "train_score_rmse": trsr, "test_score_rmse": tssr}


@app.route('/upload_and_prepare_test_files', methods=['POST'])
def upload_and_prepare_test_files():
    response = SERVICE.upload_and_prepare_test_files(request.files.getlist('file'))
    return jsonify({"num_processed_and_writen_instance": response})


@app.route('/test_model', methods=['POST'])
def test_model():
    response = SERVICE.test_model()
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug = True)

