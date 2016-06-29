from pybrain.datasets import SupervisedDataSet
from machine_learning.utils import file_to_dataset
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from sklearn.metrics import classification_report
from machine_learning.utils import CA
import numpy as np

CLASS = ['blue','red']
CLASS_OUTPUT = {'blue':0,'red':1}


def predict(net, X):
    y = np.empty(len(X),dtype='S5')
    for i, x in enumerate(X):
        y[i] = CLASS[int(round(net.activate(x)[0]))]
    return y



#DATASET SETUP
fname = '..\data_composition.tab'

attributes, target = file_to_dataset(fname,2,-1,-1)
num_attr = len(attributes[0])
ds = SupervisedDataSet(num_attr , 1)
for i in range(50000):
    ds.addSample(attributes.pop(), [CLASS_OUTPUT[target.pop()]])

#NETWORK SETUP
net = buildNetwork(num_attr, 3, 1, bias = True)
trainer = BackpropTrainer(net, ds,weightdecay=0.00001,learningrate=0.05)
trainer.trainUntilConvergence(maxEpochs=100)

y_test = np.array(target[50000:],dtype='S5')
y_pred = predict(net, attributes[50000:])
print(CA(y_test, y_pred))