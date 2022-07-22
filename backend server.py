import os
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import numpy as np
from io import BytesIO
from PIL import Image
import base64

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
model_path = os.path.join(project_root, 'model')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = 'ini kunci rahasia'

target_class = ['COVID-19', 'Normal', 'Pneumonia']
my_model = load_model(f"{model_path}/A_model_fold-1.h5")

def normalization(image):
  image = ((image - np.min(image)) / (np.max(image) - np.min(image)))
  return image

@app.route('/service', methods=['GET', 'POST'])
def upload_file():
  #get post from api
  content = request.json
  if content['img']:
    #decode
    im_bytes = base64.b64decode(content['img'])
    im_file = BytesIO(im_bytes)
    img = Image.open(im_file).convert('RGB')
    img = img.resize((224,224), Image.ANTIALIAS)
    #convert to array
    img = np.asarray(img)
    img = normalization(img)
    img = img.reshape(1,224,224,3)
    preds = my_model.predict(img)
    i = np.argmax(preds[0])

    return jsonify({
      'status' : 'success',
      'predicted' :  target_class[i],
      'score' : '{:.2f}'.format(preds[0][i]*100)
    })

  return jsonify({
    'status' : 'failure'
  })
    
if __name__ == '__main__':
  app.run(port=7000, debug=True)