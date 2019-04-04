import json
import csv
import re
import url
import urllib2
import threading
import httplib2
import os
import requests

data = json.load(open(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/dataset.json'))
dataT= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/trainDataf2.json')))
dataB= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/benignData.json')))

def filteredLink(url):
	try:
		link = requests.get(url.encode('ascii','ignore')).url
	except Exception,e:
		print str(e)

	c=0
	ind = 0
	for letter in link:
		ind+=1
		if letter == '/':
			c+=1
		if c==3:
			link = link[:ind]
			break
	if 'http' in link:
		link=link[7:]

	if link[0]=='/':
		link=link[1:]

	if 'www.' in link:
		link=link[4:]

	if ('.com') in link:
		link=link.split('.com')[0]

	try:	
		if link[-1]=='/':
			link=link[:-1]
	except:
		print 'here'
		# print link
	return link





domains=[]
completeDomains=[]

for i in range(len(data['videoId'])):
	linkList=url.check(data['description'][i]+' ')
	if linkList == None:
		continue
	else:
		# print linkList
		completeDomains.append(linkList)
		filteredList=[]
		for c in range(len(linkList)) :
			filteredList.append(filteredLink(linkList[c]))
		domains.append(filteredList)
		
data['domains']=domains
data['completeDomains']=completeDomains

# with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/datasetLinks.json'), 'w') as fp:
#     json.dump(data, fp)


domains=[]
completeDomains=[]

for i in range(len(dataB['videoId'])):
	linkList=url.check(dataB['description'][i]+' ')
	if linkList == None:
		continue
	else:
		completeDomains.append(linkList)
		filteredList=[]
		for c in range(len(linkList)) :
			filteredList.append(filteredLink(linkList[c]))
		domains.append(filteredList)
		
			
dataB['domains']=domains
dataB['completeDomains']=completeDomains

# with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/benignDataLinks.json'), 'w') as fp:
#     json.dump(dataB, fp)


domains=[]
completeDomains=[]

for i in range(len(dataT['videoId'])):
	linkList=url.check(dataT['description'][i]+' ')
	if linkList == None:
		continue
	else:
		completeDomains.append(linkList)
		filteredList=[]
		for c in range(len(linkList)) :
			filteredList.append(filteredLink(linkList[c]))
		domains.append(filteredList)
			

dataT['domains']=domains
dataT['completeDomains']=completeDomains

with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/trainDataf2Links.json'), 'w') as fp:
    json.dump(dataT, fp)

