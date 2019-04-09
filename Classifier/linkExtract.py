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

def filteredLink(link):
	
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
	print link
	return link





linkDict={}
domains=[]
completeDomains=[]
count=0
data['redirectedDomains']=[]
dataB['redirectedDomains']=[]
dataT['redirectedDomains']=[]

for i in range(len(data['videoId'])):
	count+=1
	print str(100*(count/float(len(data['videoId']))))[:4]+'%'
	linkList=url.check(data['description'][i]+' ')
	if linkList == None:
		continue
	else:
		# print linkList
		completeDomains.append(linkList)
		filteredList=[]
		redirectedDomains=[]
		for c in range(len(linkList)):
			if linkList[c] not in linkDict:
				try:
					if linkList[c].find("http") == -1:
						linkList[c] = "http://"+linkList[c]

					link = requests.get(linkList[c].encode('ascii','ignore')).url
				except Exception,e:
					link=linkList[c]
					print link,str(e)

				filteredUrl=filteredLink(link)
				linkDict[linkList[c]]=(link,filteredUrl)
				print linkDict[linkList[c]][0],linkDict[linkList[c]][1]

			
			redirectedDomains.append(linkDict[linkList[c]][0])
			# else:
			filteredList.append(linkDict[linkList[c]][1])
		data['redirectedDomains'].append(redirectedDomains)
		domains.append(filteredList)
		
data['domains']=domains
data['completeDomains']=completeDomains

with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/datasetLinks0.json'), 'w') as fp:
    json.dump(data, fp)

print 'Data Done'

domains=[]
completeDomains=[]
count=0

for i in range(len(dataB['videoId'])):
	count+=1
	print str(100*(count/float(len(dataB['videoId']))))[:4]+'%'
	
	linkList=url.check(dataB['description'][i]+' ')
	if linkList == None:
		continue
	else:
		completeDomains.append(linkList)
		filteredList=[]
		redirectedDomains=[]

		for c in range(len(linkList)):
			if linkList[c] not in linkDict:
				try:
					if linkList[c].find("http") == -1:
						linkList[c] = "http://"+linkList[c]

					link = requests.get(linkList[c].encode('ascii','ignore')).url
				except Exception,e:
					link=linkList[c]
					print link,str(e)

				filteredUrl=filteredLink(link)
				linkDict[linkList[c]]=(link,filteredUrl)
				print linkDict[linkList[c]][0],linkDict[linkList[c]][1]

			
			redirectedDomains.append(linkDict[linkList[c]][0])
			# else:
			filteredList.append(linkDict[linkList[c]][1])
		dataB['redirectedDomains'].append(redirectedDomains)
				
			# else:
			# filteredList.append(linkDict[linkList[c]])
			# filteredList.append(filteredLink(linkList[c]))
		domains.append(filteredList)
		
			
dataB['domains']=domains
dataB['completeDomains']=completeDomains

with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/benignDataLinks0.json'), 'w') as fp:
    json.dump(dataB, fp)

print 'Data BenignDone'

domains=[]
completeDomains=[]
count=0

for i in range(len(dataT['videoId'])):
	count+=1
	print str(100*(count/float(len(dataT['videoId']))))[:4]+'%'
	
	linkList=url.check(dataT['description'][i]+' ')
	if linkList == None:
		continue
	else:
		completeDomains.append(linkList)
		filteredList=[]
		redirectedDomains=[]

		for c in range(len(linkList)):
			if linkList[c] not in linkDict:
				try:
					if linkList[c].find("http") == -1:
						linkList[c] = "http://"+linkList[c]

					link = requests.get(linkList[c].encode('ascii','ignore')).url
				except Exception,e:
					link=linkList[c]
					print link,str(e)

				filteredUrl=filteredLink(link)
				linkDict[linkList[c]]=(link,filteredUrl)
			print linkDict[linkList[c]][0],linkDict[linkList[c]][1]
			redirectedDomains.append(linkDict[linkList[c]][0])
			# else:
			filteredList.append(linkDict[linkList[c]][1])
		dataT['redirectedDomains'].append(redirectedDomains)
				# filteredUrl=filteredLink(linkList[c])
				# linkDict[linkList[c]]=filteredUrl

			# else:
			# filteredList.append(linkDict[linkList[c]])
			# filteredList.append(filteredLink(linkList[c]))
		domains.append(filteredList)
			

dataT['domains']=domains
dataT['completeDomains']=completeDomains

with open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Classifier/Data Files/trainDataf2Links0.json'), 'w') as fp:
    json.dump(dataT, fp)
print 'DataT Done'

