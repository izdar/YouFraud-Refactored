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
import os

data = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\dataset.json')))
# data_test = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\data_test.json')))
dataBenign= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\benignData.json')))

description=[]
tags=[]
channelId=[]
channelTitle=[]
categoryId=[]
title=[]
videoId=[]
viewCount=[]
commentCount=[] 
comments=[]

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
# for i in range(len(data_test['videoId'])):
# 	try:
# 		videos.append(data_test['title'][i].encode('ascii','ignore')+data_test['description'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
# 		index.append(i+len(data['videoId']))
# 		y.append(data_test['classification'][i].lower())	
# 	except:
# 		videos.append(data_test['title'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
# 		index.append(i+len(data['videoId']))
# 		y.append(data_test['classification'][i].lower())

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
	# t += "    " + str(index[i])
	videos[i] = t


y_train=[]
y_train=y


vectorizer = CountVectorizer()
xTrain1 = vectorizer.fit_transform(videos)


#predClass=[]
unique_fraud=[]
unique_benign=[]
xTest1=[]
xTest2=[]
xTest3=[]

# 	totalVideos=0
b=0
f=0

	
for i in range(len(data['videoId'])):
	for c in range(len(data['linkContent'][i])):
		try:
			xTest1.append(data['linkContent'][i][c])
		except:
			xTest1.append('No link content')

# for i in range(len(data_test['videoId'])):
# 	for c in range(len(data_test['linkContent'][i])):
# 		try:
# 			xTest2.append(data_test['linkContent'][i][c])
# 		except:
# 			xTest2.append('No link content')

for i in range(len(dataBenign['videoId'])):
	for c in range(len(dataBenign['linkContent'][i])):
		try:
			xTest3.append(dataBenign['linkContent'][i][c])
		except:
			xTest3.append('No link content')

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
	# t += "    " + str(index[i])
	xTest1[i] = t

for i in range(len(xTest2)):
	raw = re.sub(r'[0-9]+','',xTest2[i].lower())
	tokens = tokenizer.tokenize(raw)
	# remove stop words from tokens
	stopped_tokens = [j for j in tokens if not j in en_stop]
	# stem tokens
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	# add tokens to list
	xTest2[i] = stemmed_tokens
	t = ''
	for k in xTest2[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	# t += "    " + str(index[i])
	xTest2[i] = t

for i in range(len(xTest3)):
	raw = re.sub(r'[0-9]+','',xTest3[i].lower())
	tokens = tokenizer.tokenize(raw)
	# remove stop words from tokens
	stopped_tokens = [j for j in tokens if not j in en_stop]
	# stem tokens
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	# add tokens to list
	xTest3[i] = stemmed_tokens
	t = ''
	for k in xTest3[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	# t += "    " + str(index[i])
	xTest3[i] = t

xTest1 = vectorizer.transform(xTest1)
xTest2 = vectorizer.transform(xTest2)
xTest3 = vectorizer.transform(xTest3)

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
clf_entropy.fit(xTrain1,y_train)
prediction1 = clf_entropy.predict(xTest1)
prediction2 = clf_entropy.predict(xTest2)
prediction3 = clf_entropy.predict(xTest3)

videoLink1=[]
videoLink2=[]
videoLink3=[]

for i in range(len(data['videoId'])):
	for c in range(len(data['linksUp'][i])):
		videoLink1.append(data['linksUp'][i][c])
for i in range(len(prediction1)):
	# predClass.append(predictions[i])
	if prediction1[i]=='f':
		unique_fraud.append(videoLink1[i])
		f+=1
	elif prediction1[i]=='b':
		unique_benign.append(videoLink1[i])
		b+=1

# for i in range(len(data_test['videoId'])):
# 	for c in range(len(data_test['linksUp'][i])):
# 		videoLink2.append(data_test['linksUp'][i][c])

# for i in range(len(prediction2)):
# 	# predClass.append(predictions[i])
# 	if prediction2[i]=='f':
# 		unique_fraud.append(videoLink2[i])
# 		f+=1
# 	elif prediction2[i]=='b':
# 		unique_benign.append(videoLink2[i])
# 		b+=1

for i in range(len(dataBenign['videoId'])):
	for c in range(len(dataBenign['linksUp'][i])):
		videoLink3.append(dataBenign['linksUp'][i][c])
for i in range(len(prediction3)):
	# predClass.append(predictions[i])
	if prediction3[i]=='f':
		unique_fraud.append(videoLink3[i])
		f+=1
	elif prediction3[i]=='b':
		unique_benign.append(videoLink3[i])
		b+=1
# chanVideos[channel]['predClass']=predClass

with open('classifyDomains.json', 'w') as fp:
    json.dump(unique_fraud,fp)
