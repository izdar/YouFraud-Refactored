import json
import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from stop_words import get_stop_words
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
import re

data = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\Data Files\\dataset.json')))
dataBenign= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\Data Files\\benignData.json')))

videos = []
test = []

index=[]
highRisk = {}
mediumRisk = {}


en_stop = get_stop_words('en')

y=[]
for i in range(len(data['videoId'])):
	if data['classification'][i] != 'Not classified':
		try:
			videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i]))

			index.append(i)
			y.append(data['classification'][i].lower())
		except:
			videos.append(data['title'][i].encode('ascii','ignore')+str(data['tags'][i]))
			index.append(i)		
			y.append(data['classification'][i].lower())

for i in range(len(dataBenign['videoId'])):
	try:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(dataBenign['classification'][i].lower())	
	except:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(dataBenign['classification'][i].lower())

tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()
en_stop = get_stop_words('en')

for i in range(len(videos)):				
	raw = re.sub(r'[0-9]+','',videos[i].lower())
	tokens = tokenizer.tokenize(raw)
	# remove stop words from tokens
	stopped_tokens = [j for j in tokens if not j in en_stop]
	# stem tokens
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	# add tokens to list
	videos[i] = stemmed_tokens
	t = ''
	for k in videos[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	t += "    " + str(index[i])
	videos[i] = t 


xTrain1, xTest1, y_train, y_test = train_test_split(videos, y, test_size=0.2, random_state=100)

vectorizer = CountVectorizer()
xTrain2 = []
for i in range(len(xTrain1)):
	xTrain2.append(xTrain1[i])
for i in range(len(xTrain1)):
	xTrain1[i] = xTrain1[i][:-4]
xTrain1 = vectorizer.fit_transform(xTrain1)


xTest2 = []
for i in range(len(xTest1)):
	xTest2.append(xTest1[i])
for i in range(len(xTest1)):
	xTest1[i] = xTest1[i][:-4]
xTest1 = vectorizer.transform(xTest1)
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
clf_entropy.fit(xTrain1,y_train)
# est = clf_entropy.estimators_[99]
predictions = clf_entropy.predict(xTest1)
print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"

wrongPred = []
for i in range(len(predictions)):
	if predictions[i]!=y_test[i]:
		if int(xTest2[i][-4:]) < len(data['videoId']):
			wrongPred.append(['d'+xTest2[i][-4:],data['videoId'][int(xTest2[i][-4:])],predictions[i],y_test[i]])
# 		elif int(xTest2[i][-4:]) < (len(data['videoId'])+len(data_test['videoId'])):
  # 			wrongPred.append(['dt'+xTest2[i][-4:],data_test['videoId'][int(xTest2[i][-4:])-len(data['videoId'])][32:],predictions[i],y_test[i]])			
		else:
			wrongPred.append(['db'+xTest2[i][-4:],dataBenign['videoId'][int(xTest2[i][-4:])-(len(data['videoId'])+len(data_test['videoId']))][32:],predictions[i],y_test[i]])			

fp=[]
fn=[]
dict={}
for pred in wrongPred:
	if pred[-2]=='f':
		fp.append(pred[1])
	if pred[-2]=='b':
		fn.append(pred[1])
dict['falsePositives']=fp
dict['falseNegatives']=fn

print wrongPred

with open((os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Classifier\\Data Files\\falseClassified.json')), 'w') as fp:
    json.dump(dict, fp)
