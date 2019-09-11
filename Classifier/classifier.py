import json
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
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
from sklearn.metrics import average_precision_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer

data = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/dataset.json')))
dataBenign= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/benignData.json')))
dataT= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/trainData.json')))

print len(data['domains'])
print len(dataBenign['domains'])
print len(dataT['domains'])

videos = []
test = []

index=[]
highRisk = {}
mediumRisk = {}
uniqueVid=[]

en_stop = get_stop_words('en')
y=[]
wcount=0
videoLinksLength=[]
for i in range(len(data['videoId'])):
	if data['videoId'][i] not in uniqueVid:

		if data['classification'][i] != 'Not classified':
			linkLength=[]
			whatsappFeature=[]
			playstoreFeature=[]
			
			count=0	
			if 'whatsapp' in data['description'][i].encode('ascii','ignore').lower():
				# print data['description'][i].encode('ascii','ignore').lower()
				for d in range(10000):
					whatsappFeature.append('whatsapp')
			for c in data['domains'][i]:
				if 'whatsapp' in c or 'whatsaap' in c or 'whatsap' in c:
					for d in range(10000):
						whatsappFeature.append('whatsapp')
				if 'play.google' in c:
					for d in range(10000):
						playstoreFeature.append('playgoogle')
				count+=1
			for c in data['linkContent'][i]:
				if len(c)<6000:
					for d in range(1000):
						linkLength.append('linkLength')
					
			videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([data['domains'][i] for x in range(100)]))
				
			index.append(i)
			y.append(data['classification'][i].lower())
			uniqueVid.append(data['videoId'][i])

for i in range(len(dataBenign['videoId'])):
	if dataBenign['videoId'][i] not in uniqueVid:
		uniqueVid.append(dataBenign['videoId'][i])

		whatsappFeature=[]
		playstoreFeature=[]
		linkLength=[]

		count=0
		if 'whatsapp' in dataBenign['description'][i].encode('ascii','ignore').lower():
				# print data['description'][i].encode('ascii','ignore').lower()
			for d in range(10000):
				whatsappFeature.append('whatsapp')
		for c in dataBenign['domains'][i]:
			if 'whatsapp' in c or 'whatsaap' in c or 'whatsap' in c:
				for d in range(10000):
					whatsappFeature.append('whatsapp')
			if 'play.google' in c:

				for d in range(10000):
					playstoreFeature.append('playgoogle')
			count+=1
		for c in dataBenign['linkContent'][i]:
			if len(c)<6000:
				for d in range(1000):
					linkLength.append('linkLength')


		videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([dataBenign['domains'][i] for x in range(100)]))		
		index.append(i+len(data['videoId']))
		y.append(dataBenign['classification'][i].lower())	

for i in range(len(dataT['videoId'])):
	if dataT['videoId'][i] not in uniqueVid:

		whatsappFeature=[]
		playstoreFeature=[]
		linkLength=[]
		count=0
		if 'whatsapp' in dataT['description'][i].encode('ascii','ignore').lower():
				# print data['description'][i].encode('ascii','ignore').lower()
			for d in range(10000):
				whatsappFeature.append('whatsapp')
		for c in dataT['domains'][i]:
			if 'whatsapp' in c or 'whatsaap' in c or 'whatsap' in c:
				for d in range(10000):
					whatsappFeature.append('whatsapp')
			if 'play.google' in c:
				for d in range(10000):
					playstoreFeature.append('playgoogle')
			count+=1

		for c in dataT['linkContent'][i]:
			if len(c)<6000:
				for d in range(1000):
					linkLength.append('linkLength')


		videos.append(dataT['title'][i].encode('ascii','ignore')+dataT['description'][i].encode('ascii','ignore')+str(dataT['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([dataT['domains'][i] for x in range(100)]))

		index.append(i+len(data['videoId']))
		y.append(dataT['classification'][i].lower())	
		uniqueVid.append(dataT['videoId'][i])

print 'wCount',wcount
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


xTrain1, xTest1, y_train, y_test = train_test_split(videos, y, test_size=0.2, random_state=2)

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

# print vectorizer
print 'BOW',len(vectorizer.get_feature_names())
# data preprocessing
with open((os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/BOW.json')), 'w') as fp:
    json.dump(vectorizer.get_feature_names(), fp)
# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
# clf_entropy = Pipeline([
#     ('features', FeatureUnion([
#         ('text', Pipeline([
#             ('vectorizer', vectorizer),
#         ])),
#         ('length', Pipeline([
#             ('count', FunctionTransformer(np.array(videoLinksLength).reshape(-1, 1), validate=False)),
#         ]))
#     ])),
#     ('clf_entropy', RandomForestClassifier(n_estimators=10000,criterion='gini',random_state=2))])

clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini',random_state=2)
clf_entropy.fit(xTrain1,y_train)
importantFeatures=[]

for feature in sorted(zip(map(lambda x: round(x, 10), clf_entropy.feature_importances_), vectorizer.get_feature_names()), reverse=True):
    importantFeatures.append(feature)

with open((os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/importantFeatures.json')), 'w') as fp:
    json.dump(importantFeatures, fp)


predictions = clf_entropy.predict(xTest1)
print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"
print classification_report(y_test,predictions)

print(confusion_matrix(y_test,predictions))

trueNegative=0
truePositive=0
wrongPred = []
for i in range(len(predictions)):
	if predictions[i]=='b' and y_test[i]=='b':
		trueNegative+=1
	if predictions[i]=='f' and y_test[i]=='f':
		truePositive+=1

	# if int(xTest2[i][-4:]) < len(data['videoId']):
	# 	print len(data['linkContent'][int(xTest2[i][-4:])])
	# elif int(xTest2[i][-4:]) < (len(data['linkContent'])+len(dataBenign['linkContent'])):
	# 	print len(dataBenign['linkContent'][int(xTest2[i][-4:])-len(data['linkContent'])])
	# else:
	# 	print len(dataT['linkContent'][int(xTest2[i][-4:])-(len(data['linkContent'])+len(dataBenign['linkContent']))])

	if predictions[i]!=y_test[i]:
		if int(xTest2[i][-4:]) < len(data['videoId']):
			wrongPred.append(['d'+xTest2[i][-4:],data['videoId'][int(xTest2[i][-4:])],predictions[i],y_test[i]])
			print len(data['linkContent'][int(xTest2[i][-4:])])
			
		elif int(xTest2[i][-4:]) < (len(data['videoId'])+len(dataBenign['videoId'])):
  			wrongPred.append(['db'+xTest2[i][-4:],dataBenign['videoId'][int(xTest2[i][-4:])-len(data['videoId'])],predictions[i],y_test[i]])			
			print len(dataBenign['linkContent'][int(xTest2[i][-4:])-len(data['linkContent'])])
			
		else:
			print 'HEREEEEE'
			print len(dataT['linkContent'][int(xTest2[i][-4:])-(len(data['linkContent'])+len(dataBenign['linkContent']))])
			
			wrongPred.append(['dt'+xTest2[i][-4:],dataT['videoId'][int(xTest2[i][-4:])-(len(data['videoId'])+len(dataBenign['videoId']))][32:],predictions[i],y_test[i]])

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



# print wrongPred

# with open((os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/falseClassified.json')), 'w') as fp:
#     json.dump(dict, fp)

