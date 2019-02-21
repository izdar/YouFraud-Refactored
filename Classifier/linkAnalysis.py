import json
import csv
import re
import url
import urllib2
import threading
import httplib2

uniqueLinks = []
lock=0
linkResults = {}
threadLock = threading.Lock()

def multiLinkCheck(links,i):
	global uniqueLinks
	global lock
	global linkResults
	global threadLock
	threadLock.acquire()
	print "Thread:",i
	threadLock.release()
	for link in links:
		temp = url.active(link,i)
		threadLock.acquire()
		linkResults[link] = temp
		threadLock.release()
	threadLock.acquire()
	lock+=1
	print "LOCK UPDATED",lock
	threadLock.release()

def linkWork():
	global uniqueLinks
	global lock
	global linkResults
	links=[]
	linksCount=[]
	category=[]
	linksDownCount=[]
	linksDown = []
	linksUp = []
	classification=[]

	notclassified=0
	x = json.load(open('dataset.json'))

	count=0.0
	h = httplib2.Http(timeout=60)
	for i in range(len(x['videoId'])):
		count += 1.0
		print str(100*(count/float(923)))[:4]+'%'
		
		inactive=0
		videoLinksUp = []
		videoLinksDown = []
		linksDownError={}
		# for i in range(len(x['videoId'])):
		linkList=url.check(x['description'][i]+' ')
		if linkList != None:
			# continue
			for link in linkList:
				if linkResults[link][1] != 'active':
					inactive+=1
					# linksDownError[link]=linkResults[link]
					videoLinksDown.append(linkResults[link])
				else:
					videoLinksUp.append(linkResults[link][0])

		linksDownCount.append(inactive)
		linksDown.append(videoLinksDown)
		linksUp.append(videoLinksUp)

		if len(linkList)!=0:
			links.append(linkList)
			linksCount.append(str(len(linkList)))

		else:
			links.append('No links')
			linksCount.append('0')

		# with open ('categorylist.txt','r') as file:
		# 	for line in file:
		# 		if x['categoryId'][i] in str(line[0:4]):
		# 			category.append(line[4:-1])
		# 			break

		
	x['links']=links
	# x['category']=category
	x['linksCount']=linksCount
	x['linksDown'] = linksDown
	x['linksUp'] = linksUp
	x['linksDownCount']=linksDownCount
	# x['classification']=classification

	with open('dataset.json', 'w') as fp:
		json.dump(x,fp)


def main():
	global uniqueLinks
	global linkResults
	global lock
	x = json.load(open('dataset.json'))
	for i in range(len(x['videoId'])):
		linkList=url.check(x['description'][i]+' ')
		if linkList == None:
			continue
		else:
			for link in linkList:
				if link not in uniqueLinks:
					uniqueLinks.append(link)
	parts = len(uniqueLinks)/20
	for i in range(19):
		t = threading.Thread(target=multiLinkCheck,args=(uniqueLinks[i*parts:(i+1)*parts],i))
		t.start()
	t = threading.Thread(target=multiLinkCheck,args=(uniqueLinks[19*parts:],19))
	t.start()
	while(lock<20):
		continue
	linkWork()

if __name__=='__main__':
	main()