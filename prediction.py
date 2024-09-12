import argparse

parser = argparse.ArgumentParser(description= 'Prediction on Empirical Data')
parser.add_argument('fileName', type=str, help= 'Name of the file to predict on')
parser.add_argument('modelName', type=str, help= 'Model Name')

args = parser.parse_args()

fName = args.fileName
mName = args.modelName


'''
Importing packages
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import pickle

import tensorflow as tf


from tensorflow.keras.applications import MobileNetV2, VGG16, EfficientNetB7, EfficientNetB0, InceptionResNetV2


from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Input
from tensorflow import random as tf_random
from tensorflow.keras.models import load_model, Sequential, Model

from sklearn.linear_model import LogisticRegression, LogisticRegressionCV

from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve




#path = os.getcwd()

print('Importing packages ... done')

mean = np.load('./Image_datasets/'  + mName + "_mean.npy")
SD = np.load('./Image_datasets/'  + mName + "_SD.npy")



X_emp_img = np.load('./VCF_datasets/'+ fName+ ".npy")

print('Loading required dataset ... done')

'''
Standardizing empirical dataset
'''

X_emp_img = (X_emp_img - mean)/(SD)

print('Standardizing empirical dataset ... done')

'''
Loading pre-trained model
'''


pt_model = InceptionResNetV2(include_top=False, weights='imagenet', input_shape= X_emp_img.shape[1:])

inp = Input(X_emp_img.shape[1:])
inp2 = tf.keras.applications.inception_resnet_v2.preprocess_input(inp)
x = pt_model(inp2)
x = GlobalAveragePooling2D()(x)

x.trainable = False


model = Model(inp2, x) #out


X_emp = model.predict(X_emp_img)

print('Loading pre-trained model ... done')


'''
Training and testing logistic regression model
'''

with open(mName+'.pkl', 'rb') as f:
    logreg = pickle.load(f)


y_emp_proba = logreg.predict_proba(X_emp)
y_emp_sweep_proba = y_emp_proba[:, 1]

np.savetxt('./Predictions/' +'prediction_' +fName+'.txt', y_emp_sweep_proba)
