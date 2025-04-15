import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from sklearn.linear_model import LogisticRegression
import pickle

# Argument parser
parser = argparse.ArgumentParser(description='Train TrIdent model')
parser.add_argument('Sw', type=str, help='Sweep file')
parser.add_argument('Ne', type=str, help='Neutral file')
parser.add_argument('split', type=float, help='Train/test split')
parser.add_argument('modelName', type=str, help='Name of model')
args = parser.parse_args()

# Load data
neutral = np.load("./Image_datasets/" + args.Ne + '.npy')
sweep = np.load("./Image_datasets/" + args.Sw + '.npy')

# Split data
nSplit = int(neutral.shape[0] * args.split)
sSplit = int(sweep.shape[0] * args.split)

train_neutral = neutral[:nSplit]
train_sweep = sweep[:nSplit]

test_neutral = neutral[nSplit:]
test_sweep = sweep[sSplit:]

# Concatenate and standardize
X_train_img = np.concatenate((train_sweep, train_neutral), axis=0)
X_test_img = np.concatenate((test_sweep, test_neutral), axis=0)
mean = np.mean(X_train_img, axis=0)
SD = np.std(X_train_img, axis=0)

mean_fileName = './Image_datasets/' + args.modelName + '_mean.npy'
SD_fileName = './Image_datasets/' + args.modelName + '_SD.npy'
np.save(mean_fileName, mean)
np.save(SD_fileName, SD)

X_train_img = (X_train_img - mean) / SD
X_test_img = (X_test_img - mean) / SD

Y_train = np.array([1] * train_sweep.shape[0] + [0] * train_neutral.shape[0])
Y_test = np.array([1] * test_sweep.shape[0] + [0] * test_neutral.shape[0])

# Model Architecture
pt_model = InceptionResNetV2(include_top=False, input_shape=X_test_img.shape[1:], weights='imagenet')
inp = Input(X_test_img.shape[1:])
inp2 = tf.keras.applications.inception_resnet_v2.preprocess_input(inp)
x = pt_model(inp2)
x = GlobalAveragePooling2D()(x)
x.trainable = False
model = Model(inp, x)

# Train and Predict
X_train = model.predict(X_train_img)
X_test = model.predict(X_test_img)

def binary_crossentropy(y_true, y_pred, epsilon=1e-7):
    """
    Compute the binary cross-entropy loss.
   
    Parameters:
        y_true (np.ndarray): Ground truth labels (0 or 1), shape (n_samples,)
        y_pred (np.ndarray): Predicted probabilities, shape (n_samples,)
        epsilon (float): Small value to avoid log(0)
   
    Returns:
        float: Binary cross-entropy loss
    """
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # avoid log(0)
    loss = - (y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return np.mean(loss)

losses = []
l_1s = []
c_s = []

for l_1 in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    for c_ in [10**-4, 10**-3, 10**-2, 10**-1, 10**0, 10**1, 10**2, 10**3, 10**4]:
        logreg = LogisticRegression(penalty='elasticnet', max_iter=20000, solver='saga', C=c_, l1_ratio=l_1)
        logreg.fit(X_train, Y_train)
        y_pred = logreg.predict_proba(X_test)
        loss = binary_crossentropy(Y_test, y_pred[:, 1])
        losses.append(loss)
        l_1s.append(l_1)
        c_s.append(c_)
best_index = losses.index(min(losses))
print(f'l1: {l_1s[best_index]}, C: {c_s[best_index]}')

logreg = LogisticRegression(penalty='elasticnet', max_iter=20000, solver='saga', C=c_s[best_index], l1_ratio=l_1s[best_index])
logreg.fit(X_train, Y_train)

y_pred = logreg.predict_proba(X_test)
print('Accuracy of logistic regression classifier on test set using elastic net penalty with l1 ratio of 0.5: {:.2f}'.format(logreg.score(X_test, Y_test)))

np.savetxt(args.modelName + '_test_prediction.txt', y_pred[:, 1])

with open(args.modelName + '.pkl', 'wb') as f:
    pickle.dump(logreg, f)

