import numpy as np
import pandas as pd
import random

data = pd.read_csv('data.csv')
random.seed( 10 )
data=data.sample(n=150)
#M-1 guz zlosliwy B-0 guz niezlosliwy
y = data[['diagnosis']].replace(['M','B'],[1,0])
y=y.values
#dane po normalizacji 
X = data[['radius_mean','texture_mean','perimeter_mean','area_mean','smoothness_mean','compactness_mean','concavity_mean','concave points_mean','symmetry_mean','fractal_dimension_mean']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
X = X.values

xPredicted = np.array(([11.41,10.82,73.34,403.3,0.094,0.066,0.035,0.026,0.16,0.061]),dtype=float)
#Normalizacja xPredicted
xPredicted = xPredicted/np.amax(xPredicted, axis=0) 

class Neural_Network(object):
  def __init__(self):
  #parametry - ilosc neuronow na wejsciu/wyjsciu/w warstwie ukrytej
    self.inputSize = 10
    self.outputSize = 1
    self.hiddenSize = 7

  #wagi - tutaj dla jednej warstwy ukrytej
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize) #  macierz wag z warstwy wejsciowej do ukrytej
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # macierz wag z warstwy ukrytej do wyjsciowej 

  def forward(self, X):
    #forward propagation through our network
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
    o = self.sigmoid(self.z3) # final activation function
    return o

  def sigmoid(self, s):
    # funkcja aktywacji
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #pochodna sigmoidy
    return s * (1 - s)

  def backward(self, X, y, o):
    # backward propagate through the network
    self.o_error = y - o # error in output
    self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error

    self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
    self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error

    self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
    self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights

  def train(self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)

  def saveWeights(self):
    np.savetxt("w1.txt", self.W1, fmt="%s")
    np.savetxt("w2.txt", self.W2, fmt="%s")

  def predict(self):
    print ("Predicted data based on trained weights: ");
    print ("Input (scaled): \n" + str(xPredicted));
    print ("Output: \n" + str(self.forward(xPredicted)));

NN = Neural_Network()
for i in range(5000): # trening sieci x50000
  print ("# " + str(i) + "\n")
  print ("Input (scaled): \n" + str(X))
  print ("Actual Output: \n" + str(y))
  print ("Predicted Output: \n" + str(NN.forward(X)))
  print ("Loss: \n" + str(np.mean(np.square(y - NN.forward(X))))) # kwadrat bledu
  print ("\n")
  NN.train(X, y)

#NN.saveWeights()
NN.predict()