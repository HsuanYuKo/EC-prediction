# -*- coding: utf-8 -*-
import os
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.utils import np_utils, plot_model
from keras.datasets import mnist
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from keras.utils.data_utils import get_file
# isort: off
from tensorflow.python.util.tf_export import keras_export
import sys

original_stdout = sys.stdout


def load_data():
    #**x_train**: uint8 NumPy array of grayscale image data with shapes`(60000, 28, 28)`, containing the training data. Pixel values range from 0 to 255.
    x_train = np.zeros((500, 100, 20))
    path =  os.getcwd()+"/train" #目前所在資料夾
    files= os.listdir(path) #得到資料夾下的所有檔名稱
    i = 0
    for file in files: #遍歷資料夾train
       x_train[i] = np.genfromtxt(path+"/"+file, dtype= None, encoding='utf-8')
       i += 1
    
    
    #**y_train**: uint8 NumPy array of digit labels (integers in range 0-9) with shape `(60000,)` for the training data.
    y_train = np.zeros((500,))
    path =  os.getcwd()+"/labeltrain" #目前所在資料夾
    files= os.listdir(path) #得到資料夾下的所有檔名稱
    i = 0
    for file in files: #遍歷資料夾train
      y_train[i] = np.genfromtxt(path+"/"+file, dtype= None, encoding='utf-8')
      i += 1  
    
    #**x_test**: uint8 NumPy array of grayscale image data with shapes (10000, 28, 28), containing the test data. Pixel values range from 0 to 255.
    x_test = np.zeros((100, 100, 20))
    path =  os.getcwd()+"/test" #目前所在資料夾
    files= os.listdir(path) #得到資料夾下的所有檔名稱
    i = 0
    for file in files: #遍歷資料夾train
        x_test[i] = np.genfromtxt(path+"/"+file, dtype= None, encoding='utf-8')
        i += 1
    
    #**y_test**: uint8 NumPy array of digit labels (integers in range 0-9) with shape `(10000,)` for the test data.
    y_test = np.zeros((100,))
    path =  os.getcwd()+"/labeltest" #目前所在資料夾
    files= os.listdir(path) #得到資料夾下的所有檔名稱
    i = 0     
    for file in files: #遍歷資料夾train
        y_test[i] = np.genfromtxt(path+"/"+file, dtype= None, encoding='utf-8')
        i += 1
    
    return (x_train, y_train), (x_test, y_test)


with open('s1083314result.txt', 'w') as f:
    sys.stdout = f
    
    # Mnist Dataset
    (X_train, Y_train), (X_test, Y_test) = load_data()
    x_train = X_train.reshape(500, 1, 100, 20)/255
    x_test = X_test.reshape(100, 1, 100, 20)/255
    y_train = np_utils.to_categorical(Y_train)
    y_test = np_utils.to_categorical(Y_test)
    
    # Model Structure
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=3, input_shape=(1, 100, 20), activation='relu', padding='same'))
    model.add(MaxPool2D(pool_size=2, data_format='channels_first'))
    model.add(Flatten())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    print(model.summary())
    
    
    # Train
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, batch_size=4, verbose=1)
    
    # Test
    loss, accuracy = model.evaluate(x_test, y_test)
    
    print('Test:')
    print('Loss: %s\nAccuracy: %s' % (loss, accuracy))
    
    # Save model
    model.save('./CNN_Mnist.h5')
    
    # Load Model
    # model = load_model('./CNN_Mnist.h5')
    sys.stdout = original_stdout 


# Display
def plot_img(n):
    plt.imshow(X_test[n], cmap='gray')
    plt.show()


def all_img_predict(model):
    print(model.summary())
    loss, accuracy = model.evaluate(x_test, y_test)
    print('Loss:', loss)
    print('Accuracy:', accuracy)
    predict = model.predict_classes(x_test)
    print(pd.crosstab(Y_test.reshape(-1), predict, rownames=['Label'], colnames=['predict']))


def one_img_predict(model, n):
    predict = model.predict_classes(x_test)
    print('Prediction:', predict[n])
    print('Answer:', Y_test[n])
    plot_img(n)


sys.stdout = original_stdout
