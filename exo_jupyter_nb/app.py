#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import sys
import os
import glob
import re
import cv2
import numpy as np
from gtts import gTTS
from io import BytesIO
from subprocess import Popen, PIPE
from subprocess import call
from pygame import mixer
from flask_socketio import SocketIO, send, emit


mytexta = 'Attack detected'
mytextna = 'Normal Traffic'
language = 'en'

# Keras

from keras.applications.imagenet_utils import preprocess_input, \
    decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app

app = Flask(__name__)
socketio = SocketIO(app)

# Model saved with Keras model.save()

MODEL_PATH = \
    '/home/deepak/Downloads/AI_Project/new-keras/models/model.h5'

# Load your trained model

model = load_model(MODEL_PATH)
model._make_predict_function()  # Necessary
print('Model loaded. Start serving...')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(100, 100))  # , color_mode = "grayscale")

    # img = np.reshape(img, (28,28,1))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Preprocessing the image

    x = image.img_to_array(img)

    # x = np.true_divide(x, 255)

    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!

    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():

    # Main page

    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        # Get the file from post request

        f = request.files['file']

        # Save the file to ./uploads

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads',
                                 secure_filename(f.filename))
        f.save(file_path)

        # Make prediction

        preds = model_predict(file_path, model)

        # Process your result for human

        pred_class = preds.argmax(axis=-1)  # Simple argmax

        # pred_class = decode_predictions(preds, top=0)   # ImageNet Decode

        result = str(pred_class[0])
        s = 'Exoplanet'  # Convert to string
        if result == str(0):
            mixer.init()  # call(['vlc', 'malware_traffic.mp3', '--play-and-exit', '--fullscreen'], shell=False)
            mixer.music.load('Exoplanet_Detected.mp3')  # close('malware_traffic.mp3')    #close(os.getcwd()+'/'+file)
            mixer.music.play()
        else:
            s = 'Not an Exoplanet'
            mixer.init()

            # call(['vlc', 'malware_traffic.mp3', '--play-and-exit', '--fullscreen'], shell=False)

            mixer.music.load('Not_Exoplanet.mp3')

            # close('malware_traffic.mp3')    #close(os.getcwd()+'/'+file)

            mixer.music.play()

            # myobj = gTTS(text=mytexta, lang=language, slow=False)

            # call(['vlc', 'normal_traffic.mp3'])

            # myobj = gTTS(text=mytextna, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named

        # classifier = myobj.save('welcome.mp3')

    # Playing the converted file

        # os.system('welcome.mp3')

        emit('res', s)
        return result
    return render_template('index.html', payload=s)

if __name__ == '__main__':

    socketio.run(app,port=5000, debug=True)
    # Serve the app with gevent

    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()

# if upload() == str(0):

