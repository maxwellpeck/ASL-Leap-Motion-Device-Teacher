import numpy as np

import csv, operator, random

class KNN:

    def __init__(self):

        self.trainingSet=[]
        self.testSet=[]
        self.split = 0.67

        self.data = None
        self.target = None

        self.k = 1

        self.trainX = None

        self.trainy = None

    def Fit(self,trainX,trainy):

        self.trainX = trainX

        self.trainY = trainy

    def Load_Dataset(self,filename):

        self.Determine_Data_Shape(filename)

        self.data   = np.zeros((self.numRowsOfData,self.numColumnsOfData-1),dtype='f')

        self.target = np.zeros((self.numRowsOfData),dtype='f')

        self.Load_Data_And_Target(filename)

    def Predict(self,testFeatures):

        neighbors = self.Get_Neighbors(testFeatures)

        result    = self.Get_Response(neighbors)

        return result

    def Print(self):

        print(self.data)
        print(self.target)

    def Use_K_Of(self,k):

        self.k = k

# ------------------ Private methods -------------------

    def Determine_Data_Shape(self,filename):

        self.numColumnsOfData = 0
        self.numRowsOfData = 0

        with open(filename, 'rb') as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                self.numRowsOfData = self.numRowsOfData + 1
                self.numColumnsOfData = len(line)

    def Get_Neighbors(self,testFeatures):

        distances = []

        for i in range(len(self.trainX)):

            trainingFeatures = self.trainX[i,:]

            trainingClass    = int(self.trainY[i])

            dist = np.linalg.norm( trainingFeatures - testFeatures )

            distances.append( ( trainingFeatures , trainingClass, dist ) )

        distances.sort(key=operator.itemgetter(2))

        neighbors = []
        for i in range(self.k):
            neighbors.append((distances[i][0],distances[i][1]))

        return neighbors

    def Get_Response(self,neighbors):

        classVotes = {}

        for x in range(len(neighbors)):

            response = neighbors[x][1]

            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1

        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)

        return sortedVotes[0][0]

    def Load_Data_And_Target(self,filename):

        with open(filename, 'rb') as csvfile:
            lines = csv.reader(csvfile)
            i = 0
            for line in lines:
                j = 0
                for j in range(0,self.numColumnsOfData-1):
                    self.data[i,j] = float(line[j])
                self.target[i] = float(line[self.numColumnsOfData-1])
                i = i + 1
