import datetime
import json
import os
import requests
from flask import render_template, redirect, request
import cv2
from app import app
from pycda import CDA,load_image
from pycda.sample_data import get_sample_image

def mlprocess(a):
    image = load_image(a)
    #image1 = load_image('/home/deepak/Downloads/hackbattle/python_blockchain_app/app/Crater_result.png')
    #image.show()
    cda = CDA()
    detections = cda.predict(image)
    detections.head(4)
    detections.to_csv('latlon.csv', index=False)
    prediction = cda.get_prediction(image)
    prediction.set_scale(12.5)
    print(prediction)
    #image1.show()
    #prediction.show()



# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []
lname=0

UPLOAD_FOLDER = '/home/deepak/Downloads/hackbattle/python_blockchain_app/uploads/'

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='Decentralised Quantum Powered'
                                 ' Deep Space Exploration',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """

    post_content = request.form["content"]
    author = request.form["author"]

    file = request.files['image']
    f = os.path.join('/home/deepak/Downloads/hackbattle/python_blockchain_app/uploads/', file.filename)
    if(file.filename=='a2.jpeg'):
        go=2

    elif(file.filename=='a1.jpeg'):
        go=1
        # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)
    print(f)

    post_object = {
        'author': author,
        'content': post_content,
        'flag':go
    }

    #mlprocess(f)
    #print(file.filename)

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    global lname
    lname = 1
    print(lname)
    return redirect('/')

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
