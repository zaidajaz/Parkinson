import numpy as np
from sklearn import preprocessing, neighbors, model_selection, metrics, svm
from sklearn.metrics import accuracy_score
import pandas as pd


def calc_accuracy(filefullname, insig_field, class_field):
	accuracy = 0
	# for i in range (0, 5):
	df = pd.read_csv(str(filefullname))

	insig_field = str(insig_field)
	insig_field_list = insig_field.split(',')
	for insig in insig_field_list:
		df.drop([insig],1,inplace=True)

	X = np.array(df.drop([class_field], 1))
	y=np.array(df[class_field])

	X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.1)

	clf = svm.LinearSVC()
	clf.fit(X_train, y_train)
	y_pred_class = clf.predict(X_test)
	c_error = (1-(accuracy_score(y_test, y_pred_class)))*100
	c_accuracy = clf.score(X_test, y_test)*100
	conf_matrix = metrics.confusion_matrix(y_test, y_pred_class)
	measures = {"classification_error":c_error, "classification_accuracy":c_accuracy, "confusion_matrix":conf_matrix}
	return measures
	#return 0

def predict(string_values):

	# df = pd.read_csv('/home/zaid/parkinson/datasets/hello_GQbFp9y.txt')
	# df.drop(['name'],1,inplace=True)

	# X = np.array(df.drop(['status'], 1))
	# y=np.array(df['status'])

	# X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.1)

	# clf = neighbors.KNeighborsClassifier()
	# clf.fit(X_train, y_train)

	# clf = neighbors.KNeighborsClassifier()
	# string_values = string_values.split(',')
	# new_data = np.array([string_values])
	# new_data = new_data.reshape(1,-1)
	# prediction = clf.predict(new_data)
	
	# return prediction

	# for i in range (0, 5):
	df = pd.read_csv('/home/zaid/parkinson/datasets/hello_GQbFp9y.txt')

	
	df.drop(['name'],1,inplace=True)

	X = np.array(df.drop(['status'], 1))
	y=np.array(df['status'])

	X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.1)

	clf = neighbors.KNeighborsClassifier()
	clf.fit(X_train, y_train)

	string_values = string_values.split(',')

	new_data = np.array([string_values])
	new_data = new_data.reshape(1,-1)
	prediction = clf.predict(new_data)

	return prediction