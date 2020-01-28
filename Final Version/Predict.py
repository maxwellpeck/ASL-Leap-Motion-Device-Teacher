import matplotlib.pyplot as plt
import numpy as np
from knn import KNN
import os

knn = KNN()

path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 4/iris.csv"
knn.Load_Dataset(path)

trainX = knn.data[::2, 1:3]
trainy = knn.target[::2]

testX = knn.data[1::2, 1:3]
testy = knn.target[1::2]

knn.Use_K_Of(15)
knn.Fit(trainX, trainy)

colors = np.zeros((3, 3), dtype='f')
colors[0, :] = [1, 0.5, 0.5]
colors[1, :] = [0.5, 1, 0.5]
colors[2, :] = [0.5, 0.5, 1]

plt.figure()

[numItems, numFeatures] = knn.data.shape
for i in range(0, numItems / 2):
    itemClass = int(trainy[i])
    currColor = colors[itemClass, :]
    plt.scatter(trainX[i, 0], trainX[i, 1], facecolor=currColor, edgecolor=(0, 0, 0), s=50, lw=2)

numCorrect = 0
for i in range(0, numItems / 2):
    itemClass = int(testy[i])
    currColor = colors[itemClass, :]

    prediction = int(knn.Predict(testX[i, :]))
    edgeColor = colors[prediction, :]

    if (prediction == itemClass):
        numCorrect += 1

    plt.scatter(testX[i, 0], testX[i, 1], facecolor=currColor, edgecolor=edgeColor, s=50, lw=2)

percent = (float(numCorrect) / float(numItems / 2)) * 100
print(percent)

plt.show()