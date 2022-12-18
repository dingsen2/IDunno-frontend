from datetime import datetime
import os
from flask import Flask, request, session, jsonify
from werkzeug.utils import secure_filename
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path, ObjectType, publish
from flask_cors import CORS
from ariadne.constants import PLAYGROUND_HTML
import logging
import client
import socket
from glob import *
import json
import os
import threading
import glob

logger = logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')

class Client():
    '''
    Client class to receive input
    and incoming messages from coordinator
    '''
    def __init__(self) -> None:
        self.host = socket.gethostname()
        self.port = DEFAULT_PORT_COORDINATOR_INPUT
        self.addr = (self.host, self.port)
        self.job_to_testres = {}
    
    def run_app(self):
        self.app.run(port=8000)
    
    def store_all_result(self, image_folder_path_list:list):
        '''
        store all images and its classes to the job_to_testres
        '''
        for image_folder_path in image_folder_path_list:
            print(os.listdir(image_folder_path))
            self.store_all_result_in_current_path(image_folder_path, self.job_to_testres)

    def store_all_result_in_current_path(self, image_folder_path:str, job_to_testres):
        '''
        helper to store all test set result into a class dict
        '''
        for child in os.listdir(image_folder_path):
            path = os.path.join(image_folder_path, child)
            print(path)
            if os.path.isdir(path):
                self.store_all_result_in_current_path(path, job_to_testres)
            elif path.endswith('.png') or path.endswith('.jpg'):
                job_to_testres[child] = os.path.basename(os.path.dirname(path))
    
    def receiver(self):
        '''
        receive message from coordinator
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(self.addr)
            while True:
                data, server = s.recvfrom(4096)
                if data:
                    msg = json.loads(data.decode('utf-8'))
                    # msg_type = msg['type']

                    # if message is from client, distribute the work to other workers
                    # if msg_type == 'accomplish':
                    #     job_type = msg['job_type']
                    #     image_to_pred = msg['pred']
                    recv_int = msg['input']
                    publish(
                        'dataChanged',
                        {'users':recv_int}
                    )


    def run_client(self):
        self.store_all_result(['/Users/dingsen2/Desktop/uiuc-mcs/425/mp/mp4-other-version/mnist_testing', '/Users/dingsen2/Desktop/uiuc-mcs/425/mp/mp4-other-version/cat_dog_testing_set'])
        # app_thread = threading.Thread(target=self.run_app)
        t_receiver = threading.Thread(target=self.receiver)
        t_receiver.start()
        t_receiver.join()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['UPLOAD_FOLDER'] = '/Users/dingsen2/Desktop/IDunno/backend/uploads'
CORS(app, expose_headers='Authorization')

# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     return PLAYGROUND_HTML, 200

type_defs = load_schema_from_path('schema.graphql')
# Define a GraphQL object type for the DataType class using the @ObjectType decorator
@ObjectType
class DataType:
    users: int

# Define a GraphQL subscription type using the @ObjectType decorator
class SubscriptionType(ObjectType):
    @ObjectType
    class Subscription:
        data_changed = DataType.field

# Map resolver functions to schema
schema = make_executable_schema(type_defs, [SubscriptionType])
# Create an instance of the Ariadne GraphQL class
graphql = GraphQL(schema)


@app.route('/upload', methods=['POST'])
def monitor():
    '''
    monitor stdin input
    '''
    helper = '''
    ======  Command List  ======
    - [job type][file_list.txt]
    e.g. animal image_list.txt
            number image_list.txt
    ============================
    '''
    print(helper)
    file_obj = request.files['file']
    file_name = file_obj.filename
    job_type = request.form.get('job_type').lower()
    logger.info(file_name)
    logger.info(job_type)

    if not file_name.endswith('.txt') :
        logger.info("must be a .txt file!")
    elif job_type == "animal" or job_type == "number":
        input_handler(job_type, file_obj)
    else:
        logger.info("Unknown commands")
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Charlie'},
    ]
    response = jsonify(users)
    return response


def input_handler(job_type:str, flask_file):
    input_image_file = flask_file
    lines = input_image_file.readlines()
    image_list = []
    for line in lines:
        image_list.append(line.decode().strip())
    # 
    input_image_file.close()
    logger.info(image_list)
    # send the image set and job type to coordinator
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        client_input_msg = {
            'type':'from_client',
            'job_type': job_type,
            'job_id':datetime.now().strftime("%m-%d-%Y-%H-%M-%S"),
            'images':image_list,
            'client_addr':socket.gethostname()
        }
        logger.info(client_input_msg)
        # send message to both standby and current coordinator, 
        # if current doesn't die, standby do nothing
        for host in CANDIDATE_COORDINATORS:
            s.sendto(json.dumps(client_input_msg).encode('utf-8'), (host, DEFAULT_PORT_CLIENT_INPUT))

def run_app():
    app.run(port=8000, debug=True)

def main():
    client = Client()
    t_receiver = threading.Thread(target=client.receiver)
    t_file_upload = threading.Thread(target=run_app)
    t_receiver.start()
    t_file_upload.start()
    # run_app()

if __name__ == "__main__":
    main()