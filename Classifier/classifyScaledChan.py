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

# 4,6,7,13,14,15,22,23,24,27,30,31,35,38,39,43,44,45,49


data = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\dataset.json')))
data_test = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\data_test.json')))
dataBenign= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\benignData.json')))

# for i in range(50):

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
# highRisk = {}
# mediumRisk = {}

# for i in range(len(data_test['videoId'])):
# 	if data_test['videoId'][i][32:]=='https://www.youtube.com/watch?v=F1-poGrDhCI':
# 		# print 'h'
# 		print data_test['classification'][i]
# for i in range(len(data_test['videoId'])):
# 	for j in range(len(data['videoId'])):
# 		if data_test['videoId'][i][64:] == data['videoId'][j]:
# 			highRisk[i] = data['mcafeeHighRisk'][j]
# 			mediumRisk[i] = data['mcafeeMediumRisk'][j]
# 			break

# data_test['mcafeeHighRisk'] = highRisk
# data_test['mcafeeMediumRisk'] = mediumRisk

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
for i in range(len(data_test['videoId'])):
	try:
		videos.append(data_test['title'][i].encode('ascii','ignore')+data_test['description'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())	
	except:
		videos.append(data_test['title'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())

for i in range(len(dataBenign['videoId'])):
	try:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
		y.append(dataBenign['classification'][i].lower())	
	except:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
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
count=0
# for f_index in range(29,50):
# 	try:
chanVideos=json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '\\Data Collection\\AllClassifiedScaledChan.json')))
# 	except:
# 		print 'File not Found'
# 		continue
# def classify(chanVideos,xTrain1,y_train):
for channel in chanVideos:
	print str(100*(count/float(len(chanVideos))))[:4]+'%'
	count+=1
	predClass=[]
	unique_fraud=[]
	unique_benign=[]
	xTest1=[]
	totalVideos=0
	b=0
	f=0

	if len(chanVideos[channel]['videoId'])==0:
		chanVideos[channel]['predClass']=predClass
		chanVideos[channel]['totalVideos']=totalVideos
		chanVideos[channel]['Fraud']=unique_fraud
		chanVideos[channel]['Benign']=unique_benign
		chanVideos[channel]['fcount']=f
		chanVideos[channel]['bcount']=b
		continue
	
	for i in range(len(chanVideos[channel]['videoId'])):
		try:
			xTest1.append(chanVideos[channel]['title'][i].encode('ascii','ignore')+chanVideos[channel]['description'][i].encode('ascii','ignore')+str(chanVideos[channel]['tags'][i]))
		except:
			xTest1.append(chanVideos[channel]['title'][i].encode('ascii','ignore')+str(chanVideos[channel]['tags'][i]))

	xTest1 = vectorizer.transform(xTest1)

	# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
	clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
	clf_entropy.fit(xTrain1,y_train)
	predictions = clf_entropy.predict(xTest1)

	wrongPred = []

	for i in range(len(predictions)):
		predClass.append(predictions[i])

		if predictions[i]=='f':
			unique_fraud.append((chanVideos[channel]['videoId'][i],predictions[i]))
			t+=predictions[i]+":   https://www.youtube.com/watch?v="+chanVideos[channel]['videoId'][i]+'\n'
		elif predictions[i]=='b':
			unique_benign.append((chanVideos[channel]['videoId'][i],predictions[i]))
		if predictions[i]=='f':
			f+=1
		elif predictions[i]=='b':
			b+=1
	totalVideos=len(chanVideos[channel]['videoId'])

	print 'Total Videos= '+ str(len(chanVideos[channel]['videoId']))
	print 'Fraud Count= ',f,len(unique_fraud)
	print 'Benign Count= ',b,len(unique_benign)
	print 'predClass= ',len(predClass)

	chanVideos[channel]['predClass']=predClass
	chanVideos[channel]['totalVideos']=totalVideos
	chanVideos[channel]['Fraud']=unique_fraud
	chanVideos[channel]['Benign']=unique_benign
	chanVideos[channel]['fcount']=f
	chanVideos[channel]['bcount']=b


with open('AllClassifiedScaledChan.json', 'w') as fp:
    json.dump(chanVideos, fp)

fraudDict=json.load(open('fraudScaledChannels.json'))

t=''
# fraudDict={}
uniqueFraudChan=[]

for channel in clasChan:
	totalVideos=clasChan[channel]['totalVideos']
	fraudCount=clasChan[channel]['fcount']
	percentFraud=0
	if fraudCount>0:
		print 'F',fraudCount
		percentFraud=(fraudCount/float(totalVideos))*100
		print 'per',percentFraud
	if percentFraud>=50:
		t+= channel+': '+str(percentFraud)+' percent fraudulent'+'\n'
		fraudDict[channel]={}
		fraudDict[channel]['totalVideos']=totalVideos
		fraudDict[channel]['fraudCount']=fraudCount
		fraudDict[channel]['percentFraud']=percentFraud
		if channel not in uniqueFraudChan:
			uniqueFraudChan.append(channel)
print len(clasChan)
print len(uniqueFraudChan)
print len(fraudDict)
# with open('fraudChannels.txt','w') as f:
# 	f.write(t)
with open('fraudScaledChannels.json', 'w') as fp:
    json.dump(fraudDict, fp)

