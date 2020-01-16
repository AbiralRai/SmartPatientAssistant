#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 11:42:17 2020

@author: abiralrai
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('rowDataset')
X = dataset.iloc[:,2:-1]
y = dataset.iloc[:,1]


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state= 1)


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_2d = np.array(X_train).reshape(-1,1)
X_test_2d = np.array(X_test).reshape(-1,1)
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Importing Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Reshape, GlobalAveragePooling1D
from keras.layers import Conv1D, MaxPooling1D
from keras.utils import np_utils


# ====================================== ANN ==========================================================

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(1536, kernel_initializer='uniform', activation='relu', input_shape=(3071,)))

classifier.add(Dropout(0.5))

# Adding the second hidden layer
classifier.add(Dense(1536, kernel_initializer='uniform', activation='relu'))

classifier.add(Dropout(0.5))

# Adding the output layer
classifier.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))

# Compiling the ANN
classifier.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, epochs=30) # 10epo = 66% acc 


# Predicting the test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


# ====================================== CNN ==========================================================

model = Sequential()
# =======================================================================================================

