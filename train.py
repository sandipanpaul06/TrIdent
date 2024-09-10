import argparse

parser = argparse.ArgumentParser(description= 'Train TrIdent model')
parser.add_argument('trS', type=str, help= 'Sweep file')
parser.add_argument('trN', type=str, help= 'Neutral file')
parser.add_argument('splt', type=float, help= 'Train/test split')
parser.add_argument('modelName', type=str, help= 'Name of model')
args = parser.parse_args()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2, VGG16, EfficientNetB7, EfficientNetB0, InceptionResNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Input
from tensorflow import random as tf_random
from tensorflow.keras.models import load_model, Sequential, Model
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
import pickle


model_name = args.modelName +'.pkl'
spl = args.splt

neutral = np.load("./Image_datasets/" + args.trN +'.npy')
sweep = np.load("./Image_datasets/" + args.trS +'.npy')

nSplit = int(neutral.shape[0]*spl)
sSplit = int(sweep.shape[0]*spl)

train_neutral = neutral[:nSplit]
train_sweep = sweep[:nSplit]

test_neutral = neutral[nSplit:]
test_sweep = sweep[nSplit:]

X_train_img = np.concatenate(( train_sweep, train_neutral), axis = 0)
X_test_img = np.concatenate(( test_sweep, test_neutral), axis = 0)
mean = np.mean(X_train_img, axis=0)
SD = np.std(X_train_img, axis=0)

mean_fileName = './Image_datasets/' + args.modelName + '_mean.npy'
SD_fileName = './Image_datasets/' + args.modelName + '_SD.npy'
np.save(mean_fileName, mean)
np.save(SD_fileName, SD)

X_train_img = (X_train_img - mean)/(SD)
X_test_img = (X_test_img - mean)/(SD)

Y_train = np.array([1]*train_sweep.shape[0] + [0]*train_neutral.shape[0])
Y_test = np.array([1]*test_sweep.shape[0] + [0]*test_neutral.shape[0])

### Architecture part 1
pt_model = InceptionResNetV2(include_top = False, input_shape= X_test_img.shape[1:], weights='imagenet')#EfficientNetB7(include_top=False, weights='imagenet', input_shape= X_train_img.shape[1:])
inp = Input(X_test_img.shape[1:])
inp2 = tf.keras.applications.inception_resnet_v2.preprocess_input(inp)
x = pt_model(inp2) #inp2
x = GlobalAveragePooling2D()(x)
x.trainable = False
model = Model(inp2, x)

X_train = model.predict(X_train_img)
X_test = model.predict(X_test_img)

logreg = LogisticRegression(penalty= 'elasticnet', max_iter= 20000, solver = 'saga', C=0.05, l1_ratio= 0.5)
logreg.fit(X_train, Y_train)

y_pred = logreg.predict_proba(X_test)
print('Accuracy of logistic regression classifier on test set using elastic net penalty with l1 ratio of 0.5: {:.2f}'.format(logreg.score(X_test, Y_test)))

np.save(args.modelName + '_test_prediction.npy', y_pred)

with open(model_name,'wb') as f:
    pickle.dump(logreg,f)

