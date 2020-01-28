import os
import numpy as np
import pickle
# import matplotlib.pyplot as plt
from knn import KNN

# ======================================================================================================================

def ReduceData(X):
    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    return X

# ======================================================================================================================

def CenterData(X):
    allXCoordinates = X[:, :, 0, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 0, :] = allXCoordinates - meanValue

    allXCoordinates = X[:, :, 1, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 1, :] = allXCoordinates - meanValue

    allXCoordinates = X[:, :, 2, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 2, :] = allXCoordinates - meanValue
    return X

# ======================================================================================================================

def ReshapeData(set0, set1, set2, set3, set4, set5, set6, set7, set8, set9):
    setList = [set0, set1, set2, set3, set4, set5, set6, set7, set8, set9]
    X = np.zeros((10000,5*2*3),dtype='f')
    y = np.zeros((10000), dtype='f')
    for row in range(0,1000):
        for ASLNum in range(0, 10):
            y[row + (ASLNum * 1000)] = ASLNum
        col = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    for setNum in range(0, 10):
                            X[row + (setNum * 1000), col] = setList[setNum][j, k, m, row]
                    col = col + 1
    return X, y

# ======================================================================================================================

path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 6/userData/"

# train5 = pickle.load(open(path + "train5.p", "r"))
# train6 = pickle.load(open(path + "train6.p", "r"))
# test5 = pickle.load(open(path + "test5.p", "r"))
# test6 = pickle.load(open(path + "test6.p", "r"))

# ----------------------------------------------------------------------------------------------------------------------

train0 = pickle.load(open(path + "Soccorsi_train0.p", "r"))
test0 = pickle.load(open(path + "Soccorsi_test0.p", "r"))
train1 = pickle.load(open(path + "Newton_train1.p", "r"))
test1 = pickle.load(open(path + "Newton_test1.p", "r"))
train2 = pickle.load(open(path + "Newton_train2.p", "r"))
test2 = pickle.load(open(path + "Newton_test2.p", "r"))
train3 = pickle.load(open(path + "Beatty_train3.p", "r"))
test3 = pickle.load(open(path + "Beatty_test3.p", "r"))
train4 = pickle.load(open(path + "Ortigara_train4.p", "r"))
test4 = pickle.load(open(path + "Ortigara_test4.p", "r"))
train5 = pickle.load(open(path + "train5.p", "r"))
test5 = pickle.load(open(path + "test5.p", "r"))
train6 = pickle.load(open(path + "train6.p", "r"))
test6 = pickle.load(open(path + "test6.p", "r"))
train7 = pickle.load(open(path + "MacMaster_train7.p", "r"))
test7 = pickle.load(open(path + "MacMaster_test7.p", "r"))
train8 = pickle.load(open(path + "Zhang_train8.p", "r"))
test8 = pickle.load(open(path + "Zhang_test8.p", "r"))
train9 = pickle.load(open(path + "Childs_train9.p", "r"))
test9 = pickle.load(open(path + "Childs_test9.p", "r"))

# ======================================================================================================================

# train5 = ReduceData(train5)
# train6 = ReduceData(train6)
# test5 = ReduceData(test5)
# test6 = ReduceData(test6)

# ----------------------------------------------------------------------------------------------------------------------

train0 = ReduceData(train0)
test0 = ReduceData(test0)
train1 = ReduceData(train1)
test1 = ReduceData(test1)
train2 = ReduceData(train2)
test2 = ReduceData(test2)
train3 = ReduceData(train3)
test3 = ReduceData(test3)
train4 = ReduceData(train4)
test4 = ReduceData(test4)
train5 = ReduceData(train5)
test5 = ReduceData(test5)
train6 = ReduceData(train6)
test6 = ReduceData(test6)
train7 = ReduceData(train7)
test7 = ReduceData(test7)
train8 = ReduceData(train8)
test8 = ReduceData(test8)
train9 = ReduceData(train9)
test9 = ReduceData(test9)

# ======================================================================================================================

# train5 = CenterData(train5)
# train6 = CenterData(train6)
# test5 = CenterData(test5)
# test6 = CenterData(test6)

# ----------------------------------------------------------------------------------------------------------------------

train0 = CenterData(train0)
test0 = CenterData(test0)
train1 = CenterData(train1)
test1 = CenterData(test1)
train2 = CenterData(train2)
test2 = CenterData(test2)
train3 = CenterData(train3)
test3 = CenterData(test3)
train4 = CenterData(train4)
test4 = CenterData(test4)
train5 = CenterData(train5)
test5 = CenterData(test5)
train6 = CenterData(train6)
test6 = CenterData(test6)
train7 = CenterData(train7)
test7 = CenterData(test7)
train8 = CenterData(train8)
test8 = CenterData(test8)
train9 = CenterData(train9)
test9 = CenterData(test9)

# ======================================================================================================================

trainX, trainY = ReshapeData(train0, train1, train2, train3, train4, train5, train6, train7, train8, train9)
testX, testY = ReshapeData(test0, test1, test2, test3, test4, test5, test6, test7, test8, test9)

# trainX, trainY = ReshapeData(train5, train6)
# testX, testY = ReshapeData(test5, test6)

print trainX
print trainX.shape
print trainY
print trainY.shape

knn = KNN()

knn.Use_K_Of(15)
knn.Fit(trainX, trainY)

# count = 0
# for row in range(0, 10000):
#     prediction = int(knn.Predict(testX[row]))
#     if prediction == testY[row]:
#         count = count + 1
#     print(str(count) + " / " + str(row + 1))
# print(count)

pickle.dump(knn, open(path + 'classifier.p', 'wb'))