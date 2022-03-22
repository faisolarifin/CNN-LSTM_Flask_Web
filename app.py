import os
from flask import Flask, render_template, request, redirect, url_for, abort

import numpy as np
#from keras.preprocessing import image
#from keras.models import load_model


app = Flask(__name__)

target_class = ['COVID-19', 'Normal', 'Pneumonia']
# my_model = load_model("model/A_model_fold-1.h5")

imgs = 'static/img.jpg'

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def normalization(image):
 image = ((image - np.min(image)) / (np.max(image) - np.min(image)))
 return image


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
  os.remove(imgs)
  uploaded_file = request.files['citra']
  if uploaded_file.filename != '':
    uploaded_file.save(imgs)
    
  return render_template('index.html')
    
app.run(debug=True)
