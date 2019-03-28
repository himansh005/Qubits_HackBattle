import datetime
import json
import os
import requests
from flask import render_template, redirect, request
import node_server as ns
from app import app
# from pycda import CDA,load_image
# from pycda.sample_data import get_sample_image
# import matplotlib.pyplot as plt
from flask import Markup
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:3000"

posts = []

class Session:
    uid=""
    pas=""
    coins=0

def ml_process(a):

    image = load_image(a)
    #image.show()
    cda = CDA()
    detections = cda.predict(image)
    detections.head(4)
    detections.to_csv('latlon.csv', index=False)
    prediction = cda.get_prediction(image)
    prediction.set_scale(12.5)
    #prediction.show()
    #prediction.show(save_plot='/home/deepak/Downloads/hackbattle/qSpace_Master/uploads/1.png')
    #plt.close("all")
    return detections.head(4).to_html(classes="results")

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
        #print(posts)
    return(posts)


@app.route('/logout',methods=['POST'])
def logout():
    Session.uid=""
    Session.pas=""
    Session.coins=0
    return redirect('/')

@app.route('/signup_action',methods=['POST'])
def signup():
    uname = request.form["username"]
    pswd = request.form["password"]
    post_object = {
        'username': uname,
        'password': pswd,
        'content':"placeholder",
        'coins':0
    }
    new_user = "{}/signup".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_user,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')

@app.route('/login_action',methods=['POST'])
def login1():
    uname = request.form["username"]
    pswd = request.form["password"]
    # post_object = {
    #     'username': uname,
    #     'password': pswd,
    # }
    # new_user = "{}/login".format(CONNECTED_NODE_ADDRESS)

    # requests.post(new_user,
    #               json=post_object,
    #               headers={'Content-type': 'application/json'})

    a = fetch_posts()
    for i in range(len(a)):
        if(a[i]["username"]==uname):
            if(a[i]["password"]==pswd):
                Session.uid=uname
                Session.pas=pswd
                return(render_template('dashboard.html',
                           title='Decentralised Quantum Powered'
                                 ' Deep Space Exploration',
                           posts=fetch_posts(),ima="",
                           node_address="http://127.0.0.1:5000",
                           readable_time=timestamp_to_string))
            else:
                return("Wrong PassWord")
        else:
            return("Username not Found")
    return redirect('/')


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def index():
    fetch_posts()
    return render_template('dashboard.html',
                           title='Decentralised Quantum Powered'
                                 ' Deep Space Exploration',
                           posts=posts,ima="",
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)




@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    print("yelo",post_content)

    post_object = {
        'username':Session.uid,
        'password':Session.pas,
        'content': post_content,
        'coins':Session.coins
    }
    Session.coins= Session.coins+0.2
    # Submit a transaction

    UPLOAD_FOLDER = os.path.basename('uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    file_render=""

    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    # file_render=Markup("<img src='{{ url_for("static", filename="images/{}")}}'>".format(file.filename))
    file_render=file.filename
    # b = Markup(ml_process(f))
    b=Markup("<table><tr>Hello</tr></table")
    file.save(f)
    

    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return render_template('dashboard.html',
                           title='Decentralised Quantum Powered'
                                 ' Deep Space Exploration',
                           posts=posts,table=b,ima=file_render,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
