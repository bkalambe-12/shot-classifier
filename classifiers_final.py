# -*- coding: utf-8 -*-
"""classifiers-final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/bkalambe-12/shot-classifier/blob/main/classifiers_final.ipynb
"""

import warnings
warnings.filterwarnings("ignore")

import os
import shutil
import glob

!mkdir -p  ~/.kaggle
!cp kaggle.json ~/.kaggle

!kaggle datasets download -d aneesh10/cricket-shot-dataset

import zipfile
zip_ref = zipfile.ZipFile('/content/cricket-shot-dataset.zip','r')
zip_ref.extractall('/content')
zip_ref.close()

TRAIN_DIR = "./DATASET"

ORG_DIR = "./content/train"

CLASS = ['drive','legglance-flick','pullshot','sweep']

for C in CLASS:
  DEST = os.path.join(TRAIN_DIR,C)

   # if directory is mot present hen create one
  if not os.path.exists( DEST):
    os.makedirs(DEST)

    for img_path in glob.glob(os.path.join(ORG_DIR , C)+"*"):
      SRC = img_path

      shutil.copy(SRC , DEST)

"""# Model Building

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from keras.layers import Dense, Flatten
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
import keras

base_model = InceptionV3(input_shape=(256,256,3), include_top= False)

for layer in base_model.layers:
  layer.trainable = False

X = Flatten()(base_model.output)
X = Dense(units=4, activation='sigmoid')(X)

#final model
model = Model(base_model.input , X)

#compile the model
model.compile(optimizer='adam', loss= keras.losses.binary_crossentropy, metrics=['accuracy'])


#summary
model.summary()

"""#Pre-Process data using Data Generator

"""

train_datagen = ImageDataGenerator(featurewise_center= True ,
                                   rotation_range= 0.4,
                                   width_shift_range= 0.3,
                                   horizontal_flip= True,
                                   preprocessing_function= preprocess_input,
                                   zoom_range= 0.4,
                                   shear_range= 0.4
                                   )
train_data = train_datagen.flow_from_directory(directory= "/content/data",
                                               target_size=(256,256),
                                               batch_size=64)

train_data.class_indices

"""#Visualizing the data

"""

t_img , label= train_data.next()

def plotImages(img_arr , label):
   """
   input : image array
   output : plot images
   """

   for idx , img in enumerate( img_arr):

     if idx <= 10:

       plt.figure(figsize=(5,5))
       plt.imshow(img)
       plt.title(img.shape)
       plt.axis = False
       plt.show()

plotImages(t_img , label)

"""#Model Check Point

"""

from keras.callbacks import ModelCheckpoint , EarlyStopping

mc = ModelCheckpoint(filepath= "./best_model.h5",
                     monitor="accuracy",
                     verbose=1,
                     save_best_only=True)

es = EarlyStopping(monitor="accuracy",
                   min_delta=0.01,
                   patience=5,
                   verbose=1)

cb=[mc,es]

his= model.fit_generator(train_data,
                         steps_per_epoch=10,
                         epochs=30,
                         callbacks=cb)

from keras.models import load_model
model = load_model("/content/best_model.h5")

h = his.history
h.keys()

plt.plot(h['loss'],  'go--')
plt.plot(h['accuracy'], 'go--'  ,c= "red",)

plt.title("Loss vs Acc")
plt.show()

"""# Validate our model




"""

# path for the image to see if it predicts correct class
path = "/content/1-d.jpg"
img = load_img(path,target_size=(256,256))

i=img_to_array(img)

i= preprocess_input(i)

input_arr = np.array([i])
input_arr.shape

pred = np.argmax(model.predict(input_arr))
pred ==3
if pred ==0 and pred<1:
  print("The classified  shot is DRIVE")
elif pred >0 and pred<=1:
     print("The classified shot is LEGGLANCE-FLICK")
elif pred >1 and pred<=2:
    print("The classified shot is PULLSHOT")
else:
    print("The classified shot is SWEEP")




# TO DISPLAY THE IMAGE
plt.imshow(input_arr[0])
plt.title("input image")
plt.axis= False
plt.show()