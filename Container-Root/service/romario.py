# Main imports
import kfp
import kfp.dsl as dsl
from kfp.gcp import use_gcp_secret
from kubernetes import client as k8s_client
from flask import Flask, request,  send_file
from flasgger import Swagger
from werkzeug.utils import secure_filename
import datetime
import os

app = Flask(__name__)
swag = Swagger(app)

def create_rom_client():
    # Defining a client
    # client = kfp.Client()
    return kfp.Client()

def create_rom_experiment(experiment_name = 'romario_test',client=None):
    # Creating Experiment
    # exp = client.create_experiment(name=EXPERIMENT_NAME)
    nowStr = str(datetime.datetime.now())
    try:
        exp = client.create_experiment(name=experiment_name + nowStr)
    except:
        exp = None
        raise Exception('Client { } not defined'.format(client))


    return exp

def run_rom_pipeline(pipeline_name='romario_pipeline_run_',
                    pipeline_path=None,
                    client=None,
                    experiment=None,
                    timeout=None):
    # Run
    # run = client.run_pipeline(exp.id, 'hypertune-arun1', 'hypertune.tar.gz',
    #                          params={'arch': ARCH})
    # Checking for pipeline path
    if not pipeline_path:
        raise Exception('Pipeline TAR file path not defined!')
    if not experiment:
        raise Exception('Exeriment not defined!')
    if not client:
        raise Exception('Client not defined!')
    # Running the pipeline
    nowStr = str(datetime.datetime.now())
    try:
        run = client.run_pipeline(experiment.id, pipeline_name + nowStr, pipeline_path)
        #if not timeout:
        #    results = client.wait_for_run_completion(run.id, timeout=timeout)
    except:
        run = None
        raise Exception('Client { } not defined'.format(client))

    return run

# Tar-ing an ARGO YAML
# TODO: implement a tar for a given YAML

# Compile
# TODO: Provide a server to compile a python script pipeline

@app.route("/hello_romario")
def hello_romario():
    """
    Hello World, from Romario
    This is a simple hello world from Romario... and some links.
    ---
    reponese:
        500:
            description: Error on Romario Service
        200:
            description: ASCII ART
    """
    return send_file('/service/romarioArt.html')

@app.route("/print_filename", methods=['POST','PUT'])
def print_filename():
    file = request.files['file']
    filename=secure_filename(file.filename)
    file.save(filename)
    with open(filename, 'r') as fin:
        returning = fin.read()
    return returning

@app.route("/test_run_pipeline", methods=['POST','PUT'])
def test_run_pipeline():
    """
    Test Romario Running
    This is the test POST that runs a tar.gz Pipeline in your cluster
    ---
    parameters:
      - name: Pipeline file
        description: The only required information is the tar.gz file for romario to run.
        in: formData
        required: true
        type: file

    reponese:
        500:
            description: Error on Run Creation
        200:
            description: Successfully created the RUN
    """
    file = request.files['file']
    filename=secure_filename(file.filename)
    file.save(filename)
    try:
        client = create_rom_client()
        returning = 'Success!! - KF client was created\n\n'
    except:
        returning = 'Failed: Client creation not working!\n\n'
        raise Exception(returning)
    try:
        exp = create_rom_experiment(client=client)
        returning = returning + 'Success!! - Experiment was created\n\n'
    except:
        returning = 'Failed: Experiment creation Failed!\n\n'
        raise Exception(returning)

    try:
        ran = run_rom_pipeline(pipeline_path=filename,
            client=client,
            experiment=exp)
        returning = returning + 'Success!! - your pipeline should be running by now!\n\n'
    except:
        returning = 'Failed: Run creation failed!\n\n'
        raise Exception(returning)

    return returning


if __name__ == '__main__':
    app.run(port=6966, debug=True, host='0.0.0.0')
