import os
from flask import Flask, request, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
# import client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')

ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['UPLOAD_FOLDER'] = '/Users/dingsen2/Desktop/IDunno/backend/uploads'
CORS(app, expose_headers='Authorization')


@app.route('/upload', methods=['POST'])
def fileUpload():
    target = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
    logger.info("welcome to upload`")
    file = request.files['file']
    filename = file.filename
    job_type = request.form.get('job_type')
    logger.info(request.files)
    logger.info(f'file: {file.filename}; job_type: {job_type}')
    # c = client.Client(logger)
    # c.monitor(filename, file, job_type)
    # response = "Whatever you wish too return"
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Charlie'},
    ]
    response = jsonify(users)
    return response


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="localhost", port=8000, debug=True)