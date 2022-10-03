import os
from flask import Flask, render_template, request, redirect, url_for, abort
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import base64

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
model_path = os.path.join(project_root, 'model')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = 'ini kunci rahasia'

# No caching at all for API endpoints.
# @app.after_request
# def add_header(response):
#     # response.cache_control.no_store = True
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response

@app.route("/")
def home():
    return render_template('index.html', data={
      'status' : 'init'
    })

@app.route('/', methods=['POST'])
def upload():
  uploaded_file = request.files['citra']
  img = Image.open(uploaded_file.stream)
  img = img.convert("L")
  buffer = BytesIO()
  img.save(buffer, 'png')
  buffer.seek(0)

  data = buffer.read()
  data = base64.b64encode(data).decode()
  
  if uploaded_file.filename != '':
    try : 
      res = requests.post('http://shadowy-income-yme.domcloud.io/service', json={
          'msg' : 'success',
          'size' : img.size,
          'format' : img.format,
          'img' : data
        }, verify=False)
    except requests.exceptions.RequestException as e:
      return render_template('index.html', data={
        'status' : 'error',
        'msg' : 'HTTPConnectionPool to backend server is failure!',
        'err' : e,
      })

  if res.ok:
    return render_template('index.html', data={
      'status' : 'success',
      'img' : f'data:image/png;base64,{data}',
    }, res=res.json())

  return render_template('index.html', data={
      'status' : 'error',
      'msg' : 'Nothing respons from backend server!',
    })
    
if __name__ == '__main__':
  app.run(port=8000, debug=True)