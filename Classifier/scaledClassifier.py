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

unique_fraud=[]
unique_benign=[]
predClass=[]


dataScaled = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\Data Files\\uniqueScaled.json')))


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
	videos[i] = t 


y_train=[]
y_train=y
xTest1=[]
for i in range(len(dataScaled['videoId'])):
	try:
		xTest1.append(dataScaled['title'][i].encode('ascii','ignore')+dataScaled['description'][i].encode('ascii','ignore')+str(dataScaled['tags'][i]))
	except:
		xTest1.append(dataScaled['title'][i].encode('ascii','ignore')+str(dataScaled['tags'][i]))

vectorizer = CountVectorizer()


xTrain1 = vectorizer.fit_transform(videos)

for i in range(len(xTest1)):				
	raw = re.sub(r'[0-9]+','',xTest1[i].lower())
	tokens = tokenizer.tokenize(raw)
	# remove stop words from tokens
	stopped_tokens = [j for j in tokens if not j in en_stop]
	# stem tokens
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	# add tokens to list
	xTest1[i] = stemmed_tokens
	t = ''
	for k in xTest1[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	xTest1[i] = t 

xTest1 = vectorizer.transform(xTest1)
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
clf_entropy.fit(xTrain1,y_train)
predictions = clf_entropy.predict(xTest1)

wrongPred = []

b=0
f=0
t=''

for i in range(len(predictions)):
	predClass.append(predictions[i])

	if predictions[i]=='f':
		unique_fraud.append((dataScaled['videoId'][i],predictions[i]))
		t+=predictions[i]+":   https://www.youtube.com/watch?v="+dataScaled['videoId'][i]+'\n'
	elif predictions[i]=='b':
		unique_benign.append((dataScaled['videoId'][i],predictions[i]))
	if predictions[i]=='f':
		f+=1
	elif predictions[i]=='b':
		b+=1
print 'Total Videos= '+ str(len(dataScaled['videoId']))
print 'Fraud Count= ',f
print 'Benign Count= ',b

dataScaled['predClass']=predClass

with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Classifier\\Data Files\\scaledFraud.txt'),'w') as f:
	f.write(t)
with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\Data Files\\uniqueScaled.json'), 'w') as fp:
    json.dump(dataScaled, fp)
