import numpy as np

from sklearn import linear_model
from sklearn import cross_validation
from sklearn import ensemble
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import MinMaxScaler

from machine_learning.utils import *

from scipy.sparse import csr_matrix
import random


fname = '..\data.tab'
attributes, target, row_i, col_i = file_to_dataset(fname, 1,-1,-1, sparse=False)
#attributes = csr_matrix((attributes, (row_i, col_i)))
n = len(attributes)
attributes = np.array(attributes)
minmax_scaler = MinMaxScaler(feature_range=(-1,1))
attributes = minmax_scaler.fit_transform(attributes)
target_binary  = np.array([1 if t=='red' else 0 for t in target])
target = np.array(target)
target_binary = np.array(target_binary)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(attributes, target_binary, test_size=0.25, random_state=58)#58
#X_train, y_train = attributes,target_binary
#LOGISTIC
#logistic = linear_model.LogisticRegression(C=1, penalty='l1')
#dummy = DummyClassifier(strategy='most_frequent')
#plot_learning_curve(logistic, X_train, y_train, X_test, y_test, step=50)
#plot_learning_curve(logistic, X_train, y_train, None, None, step=49, use_loo=True)
#scores = cross_validation.cross_val_score(logistic, X_train, y_train, cv=10)
#print("Accuracy: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))

#logistic.fit(X_train, y_train)
#dummy.fit(X_train,  y_train)
#y_score =  logistic.decision_function(X_test)#logistic.decision_function(X_test)
#y_pred = logistic.predict(X_test)

#print("CA: " + str(CA(y_test, y_pred)))
#print("AUC: " + str(roc_auc_score(y_test,y_score)))

#y_score =  dummy.predict_proba(X_test)[:,1]#logistic.decision_function(X_test)
#y_pred = dummy.predict(X_test)

#print("CA: " + str(CA(y_test, y_pred)))
#print("AUC: " + str(roc_auc_score(y_test,y_pred)))
#print("AUC2: " + str(roc_auc_score(y_test,y_score)))
#attributes = np.array(attributes)



#LOGISTIC
#profesionalne
#tuned_parameters = [
#  {'C': [0.15], 'penalty':['l1'] },
# ]

#SVM
# Set the parameters by cross-validation

#tuned_parameters = [
#  {'C': [40], 'gamma': [0.0025], 'kernel': ['sigmoid'],'coef0':[0.5], },
# ]

#LINEAR SVM FITTED PARAMETERS
#neprofesionalne
#tuned_parameters = [
#    {'C': [0.1], 'penalty': ['l1'],'dual':[False]}
#]
#profesionalne
#tuned_parameters = [
#    {'C': [0.15], 'penalty': ['l1'],'dual':[False]}
#]

#RANDOM FORREST
#neprofesionalne
#tuned_parameters = [
#   {'n_estimators':[200], 'max_features':[40], 'min_samples_leaf':[100] }
#]
#profesionalne
#tuned_parameters = [
#   {'n_estimators':[200], 'max_features':[20], 'min_samples_leaf':[10] , 'max_depth':[5]}
#]

#clf = GridSearchCV(LinearSVC(), tuned_parameters, cv=50) #SVC(cache_size=1000)
#clf1 = linear_model.LogisticRegression(C=1, penalty='l1')
#clf2 = LinearSVC(C=0.1,penalty='l1',dual=False)
#clf3 = RandomForestClassifier(n_estimators=200, max_features=40,min_samples_leaf=100)

#clf = VotingClassifier(estimators=[('lr', clf1), ('svm', clf2), ('rf', clf3)], voting='hard')

#clf.fit(X_train, y_train)
"""print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
for params, mean_score, scores in clf.grid_scores_:
    print("%0.3f (+/-%0.03f) for %r"
          % (mean_score, scores.std() * 2, params))"""

#print("Detailed classification report:")
#print()
#print("The model is trained on the full development set.")
#print("The scores are computed on the full evaluation set.")
#print()
#plot_learning_curve(clf, X_train, y_train, X_test, y_test, step=100,add_initial=False)
#y_true, y_pred = y_test, clf.predict(X_test)
#y_score = clf.predict_proba(X_test)[:,1]
#y_score = clf.decision_function(X_test)
#print(classification_report(y_true, y_pred))
#print()
#print('CA: ')
#print(CA(y_true, y_pred))
#print("AUC: " + str(roc_auc_score(y_true,y_score)))
"""t_auc = list()
p_auc = list()
ca = list()
loo = cross_validation.LeaveOneOut(n=n)
for train_index, test_index in loo:
    X_tr, X_ts = X_train[train_index], X_train[test_index]
    y_tr, y_ts = y_train[train_index], y_train[test_index]
    clf1 = linear_model.LogisticRegression(C=0.15, penalty='l1',random_state=1)
    #clf = DummyClassifier(strategy='most_frequent')
    clf2 = SVC(cache_size=1000, C=40, gamma=0.0025,kernel='sigmoid',coef0=0.5,probability=True,random_state=1)
    #clf = LinearSVC(C=0.15,penalty='l1',dual=False)
    clf3 = RandomForestClassifier(n_estimators=200, max_features=20,min_samples_leaf=10,max_depth=5,random_state=1)
    clf = VotingClassifier(estimators=[('lr', clf1), ('svm', clf2), ('rf', clf3)], voting='hard')
    clf.fit(X_tr, y_tr)
    y_pred = clf.predict(X_ts)
    #y_score = clf.predict_proba(X_ts)[:,1]
    #y_score = clf.decision_function(X_ts)

    ca.append(CA(y_ts, y_pred))
    #t_auc.append(y_ts[0])
    #p_auc.append(y_score[0])
ca = sum(ca)/len(ca)
#auc = roc_auc_score(np.array(t_auc), np.array(p_auc))
print("CA: " + str(ca))
#print("AUC: " + str(auc))"""