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


data = json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/datasetLinks0.json')))
dataBenign= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/benignDataLinks0.json')))
dataT= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/trainDataf2Links0.json')))

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
for i in range(len(data['videoId'])):
	if data['videoId'][i] not in uniqueVid:

		if data['classification'][i] != 'Not classified':
			# try:
			whatsappFeature=[]
			playstoreFeature=[]
			if 'whatsapp' in data['description'][i].encode('ascii','ignore').lower():
				# print data['description'][i].encode('ascii','ignore').lower()
				for d in range(10000):
					whatsappFeature.append('whatsapp')
				wcount+=1

			for c in data['domains'][i]:
				if 'whatsapp' in c:
					for d in range(10000):
						whatsappFeature.append('whatsapp')
				if 'play.google' in c:
					print 'play.google'
					for d in range(10000):
						playstoreFeature.append('play.google')

			if len(whatsappFeature)!=0 and len(playstoreFeature)!=0:
				# print len(whatsappFeature)
				videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([data['domains'][i] for x in range(100)])+str(data['linkContent'][i]))
				# linkLength=
			elif len(whatsappFeature)==0 and len(playstoreFeature)!=0:
				videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i])+str(playstoreFeature)+str([data['domains'][i] for x in range(100)])+str(data['linkContent'][i]))
			 # +str(data['domains'][i]))
			elif len(whatsappFeature)!=0 and len(playstoreFeature)==0:
				videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i])+str(whatsappFeature)+str([data['domains'][i] for x in range(100)])+str(data['linkContent'][i]))
			else:
				videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i])+str([data['domains'][i] for x in range(100)])+str(data['linkContent'][i]))

			index.append(i)
			y.append(data['classification'][i].lower())
			uniqueVid.append(data['videoId'][i])

for i in range(len(dataBenign['videoId'])):
	if dataBenign['videoId'][i] not in uniqueVid:
		uniqueVid.append(data['videoId'][i])

		whatsappFeature=[]
		playstoreFeature=[]
		if 'whatsapp' in dataBenign['description'][i].encode('ascii','ignore').lower():
			for d in range(10000):
				whatsappFeature.append('whatsapp')
			wcount+=1
		for c in dataBenign['domains'][i]:
			if 'whatsapp' in c:
				for d in range(10000):
					whatsappFeature.append('whatsapp')
			if 'play.google' in c:
				print 'play.google'
				for d in range(10000):
					playstoreFeature.append('play.google')

		if len(whatsappFeature)!=0 and len(playstoreFeature)!=0:
			videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([dataBenign['domains'][i] for x in range(100)])+str(dataBenign['linkContent'][i]))		
		elif len(whatsappFeature)==0 and len(playstoreFeature)!=0:
			videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i])+str([dataBenign['domains'][i] for x in range(100)])+str(playstoreFeature)+str(dataBenign['linkContent'][i]))		
			
		elif len(whatsappFeature)!=0 and len(playstoreFeature)==0:
			videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i])+str(whatsappFeature)+str([dataBenign['domains'][i] for x in range(100)])+str(dataBenign['linkContent'][i]))		
			
		else:
			videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i])+str([dataBenign['domains'][i] for x in range(100)])+str(dataBenign['linkContent'][i]))
		index.append(i+len(data['videoId']))
		y.append(dataBenign['classification'][i].lower())	

for i in range(len(dataT['videoId'])):
	if dataT['videoId'][i] not in uniqueVid:

		whatsappFeature=[]
		playstoreFeature=[]
		if 'whatsapp' in dataT['description'][i].encode('ascii','ignore').lower():
			for d in range(10000):

				whatsappFeature.append('whatsapp')
			wcount+=1
		for c in dataT['domains'][i]:
			if 'whatsapp' in c:
				for d in range(10000):
					whatsappFeature.append('whatsapp')
			if 'play.google' in c:
				print 'play.google'
				for d in range(10000):
					playstoreFeature.append('play.google')

		if len(whatsappFeature)!=0 and len(playstoreFeature)!=0:

			videos.append(dataT['title'][i].encode('ascii','ignore')+dataT['description'][i].encode('ascii','ignore')+str(dataT['tags'][i])+str(whatsappFeature)+str(playstoreFeature)+str([dataT['domains'][i] for x in range(100)])+str(dataT['linkContent'][i]))
		elif len(whatsappFeature)==0 and len(playstoreFeature)!=0:
			videos.append(dataT['title'][i].encode('ascii','ignore')+dataT['description'][i].encode('ascii','ignore')+str(dataT['tags'][i])+str(playstoreFeature)+str([dataT['domains'][i] for x in range(100)])+str(dataT['linkContent'][i]))
			
		elif len(whatsappFeature)!=0 and len(playstoreFeature)==0:
			videos.append(dataT['title'][i].encode('ascii','ignore')+dataT['description'][i].encode('ascii','ignore')+str(dataT['tags'][i])+str(whatsappFeature)+str([dataT['domains'][i] for x in range(100)])+str(dataT['linkContent'][i]))
			
		else:
			videos.append(dataT['title'][i].encode('ascii','ignore')+dataT['description'][i].encode('ascii','ignore')+str(dataT['tags'][i])+str([dataT['domains'][i] for x in range(100)])+str(dataT['linkContent'][i]))

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


# clf_entropy = Pipeline([
#     ('features', FeatureUnion([
#         ('text', Pipeline([
#             ('vectorizer', vectorizer),
#         ])),
#         ('length', Pipeline([
#             ('count', FunctionTransformer(get_text_length, validate=False)),
#         ]))
#     ])),
#     ('clf_entropy', RandomForestClassifier(n_estimators=10000,criterion='gini',random_state=2))])
xTrain1 = vectorizer.fit_transform(xTrain1)


xTest2 = []
for i in range(len(xTest1)):
	xTest2.append(xTest1[i])
for i in range(len(xTest1)):
	xTest1[i] = xTest1[i][:-4]
xTest1 = vectorizer.transform(xTest1)

print 'BOW',len(vectorizer.get_feature_names())
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini',random_state=2)
clf_entropy.fit(xTrain1,y_train)
# est = clf_entropy.estimators_[99]
predictions = clf_entropy.predict(xTest1)
# y_score = clf_entropy.decision_function(xTest1)
print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"
# average_precision = average_precision_score(y_test, y_score)
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
		
	if predictions[i]!=y_test[i]:
		if int(xTest2[i][-4:]) < len(data['videoId']):
			wrongPred.append(['d'+xTest2[i][-4:],data['videoId'][int(xTest2[i][-4:])],predictions[i],y_test[i]])
		elif int(xTest2[i][-4:]) < (len(data['videoId'])+len(dataBenign['videoId'])):
  			wrongPred.append(['db'+xTest2[i][-4:],dataBenign['videoId'][int(xTest2[i][-4:])-len(data['videoId'])],predictions[i],y_test[i]])			
		else:
			print 'HEREEEEE'
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

print wrongPred

# with open((os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/falseClassified.json')), 'w') as fp:
#     json.dump(dict, fp)

