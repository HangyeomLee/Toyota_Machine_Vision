# -*- coding: utf-8 -*-
"""Hole_detecting_ML_Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rsWSg9vAPqZsPE4j3Da35tZsBA_qAX73
"""

!pip install tensorflow
!pip install labelbox
!pip install opencv-python-headless

#get data from google drive

from google.colab import drive
drive.mount('/content/gdrive')

#importing libraries

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import zipfile
from google.colab import files
import json
import urllib
import cv2
from labelbox import Client
from PIL import Image
from io import BytesIO
import requests
import random

#labelbox api setting

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbGhuaHljd2Qwa2diMDd6bzJvcG81NnVyIiwib3JnYW5pemF0aW9uSWQiOiJjbGhuaHljdzAwa2dhMDd6bzY5d2NnZ2RpIiwiYXBpS2V5SWQiOiJjbGhucGc5eG8waXgzMDcwOWV4b3IyeDdzIiwic2VjcmV0IjoiYzljMjMxNDA2MGY1OGE5M2NiNDFiZmM2MjFlZmQzMjQiLCJpYXQiOjE2ODQwODYyMTcsImV4cCI6MjMxNTIzODIxN30.lsfnwlRgij9iGfOlqjshZwgv_OOPdELq5UNRocNSjDM'
client = Client(API_KEY)
project_id = 'clhnnfzgh0gtc072k5ql6drhl'
project = client.get_project(project_id)

annotations = {}
for label in project.labels():
    j = json.loads(label.label)
    image_url = j.get('Labeled Data')
    
    label_objects = j.get('Label', {}).get('objects', [])
    objects = [obj.get('value').get('geometry') for obj in label_objects if obj.get('value')]
    
    annotations[image_url] = objects

# Save the datasets into train and vaildation files
train_ratio = 0.8
train_data = {}

output_dir = 'your_dataset_directory'
os.makedirs(output_dir, exist_ok=True)
subsets = ['train', 'val']
for subset in subsets:
    os.makedirs(os.path.join(output_dir, subset, 'holes'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, subset, 'stickers'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, subset, 'overlapped_stickers'), exist_ok=True)

images_url_list = list(annotations.keys())
random.shuffle(images_url_list)
train_url_list = images_url_list[:int(len(images_url_list) * train_ratio)]
val_url_list = images_url_list[int(len(images_url_list) * train_ratio):]

#training

for url in images_url_list:
    image = Image.open(BytesIO(requests.get(url).content))
    labels = annotations[url]
    subset = 'train' if url in train_url_list else 'val'
    for label in labels:
        category, geometry = label['title'], label['points']
        min_x = min([point['x'] for point in geometry])
        min_y = min([point['y'] for point in geometry])
        max_x = max([point['x'] for point in geometry])
        max_y = max([point['y'] for point in geometry])

        cropped_image = image.crop((min_x, min_y, max_x, max_y))
        file_name = f"{url.split('/')[-1].split('.')[0]}_{category}_{random.randint(10000, 99999)}.jpg"
        cropped_image.save(os.path.join(output_dir, subset, category.replace(" ", "_"), file_name))

train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest',
                                   validation_split=0.2)

train_dir = output_dir

train_generator = train_datagen.flow_from_directory(
        os.path.join(train_dir, 'train'),
        target_size=(150, 150),
        batch_size=20,
        class_mode='categorical') 

validation_generator = train_datagen.flow_from_directory(
        os.path.join(train_dir, 'val'),
        target_size=(150, 150),
        batch_size=20,
        class_mode='categorical')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

#model complie

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(
      train_generator,
      steps_per_epoch=train_generator.samples // train_generator.batch_size,
      epochs=10,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples // validation_generator.batch_size)