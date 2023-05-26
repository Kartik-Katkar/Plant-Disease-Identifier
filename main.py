#Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

#load model
model =load_model("model/model1.h5")

print('@@ Model loaded')


def pred_cot_dieas(plant):
  test_image = load_img(plant, target_size = (128, 128)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image) # predict diseased plant or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)# get the index of max value
  print(pred)
  print('@@ Raw result2 = ', pred)

  if pred == 0:
    return "Cherry Powdery Mildew Detected", 'Cherry_powdery_mildew.html' # if index 0 burned leaf
  elif pred == 1:
      return 'Healthy Cherry Leaf Detected', 'healthy_plant.html'  # if index 1
  elif pred == 2:
      return 'Peach Bacterial Spot Detected', 'Peach_Bacterial_Spot.html'  # if index 2  fresh leaf
  elif pred == 3:
      return 'Healthy Peach Leaf Detected', 'healthy_plant.html'  # if index 3  fresh leaf
  elif pred == 4:
      return 'Bell Pepper Bacterial Spot Detected', 'Bell_Pepper_Bacterial_Spot.html'  # if index 4  fresh leaf
  elif pred == 5:
      return 'Healthy Bell Pepper Leaf Detected', 'healthy_plant.html'  # if index 5  fresh leaf
  elif pred == 6:
      return 'Strawberry Leaf scorch Detected', 'Strawberry_Leaf_scorch.html'  # if index 6  fresh leaf
  elif pred == 7:
      return 'Healthy Strawberry Leaf Detected', 'healthy_plant.html'  # if index 7  fresh leaf
  elif pred == 8:
      return 'Tomato mosaic virus Detected', 'Tomato_mosaic_virus.html'  # if index 8  fresh leaf
  else:
    return "Healthy Tomato Leaf Detected", 'Tomato-Healthy.html' # if index 9

#------------>>pred_dieas<<--end
    

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/aboutp")
def aboutp():
        return render_template('about.html')

@app.route("/infor")
def infor():
        return render_template('explore.html')

@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded/', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_cot_dieas(plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,) 
    
    