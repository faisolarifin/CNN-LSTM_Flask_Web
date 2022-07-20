import os
from flask import Flask, render_template, request, redirect, url_for, abort
import numpy as np

from keras.preprocessing import image
from keras.models import load_model

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
model_path = os.path.join(project_root, 'model')
print(model_path)

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = 'ini kunci rahasia'

target_class = ['COVID-19', 'Normal', 'Pneumonia']
my_model = load_model(f"{model_path}/A_model_fold-1.h5")

imgs = f"{static_path}/img.jpg"

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

# def myPredictor():
#   if os.path.exists(imgs):
#     img = image.load_img(imgs, target_size=(224,224))
#     img = image.img_to_array(img)
#     img = normalization(img)
#     img = img.reshape(1,224,224,3)
#     preds = my_model.predict(img)
#     i = np.argmax(preds[0])
#     return target_class[i], '{:.2f}'.format(preds[0][i]*100)

@app.route("/")
def home():
    return render_template('index.html')

# @app.route('/', methods=['POST'])
# def upload_file():
#   os.remove(imgs)
#   uploaded_file = request.files['citra']
#   if uploaded_file.filename != '':
#     uploaded_file.save(imgs)
    
#   predict = myPredictor()
#   return render_template('index.html', predict=predict[0], score=predict[1])
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)