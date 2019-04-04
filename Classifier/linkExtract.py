import json
import csv
import re
import url
import urllib2
import threading
import httplib2
import os
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Queue as queue
import cfscrape
import time
from tqdm import tqdm
import datetime
from dateutil import parser



data = json.load(open(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/dataset.json'))
dataT= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/trainDataf2.json')))
dataB= json.load(open(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/Data Collection/Data Files/benignData.json')))

def fetch_proxies():
    scraper = cfscrape.create_scraper()
    print 'hereeee'
    proxies = []
    PROXY_URLS = ["https://hidemy.name/en/proxy-list/"]
    for url in PROXY_URLS:
        success = False
        while not success:
            try:
                random_agent = global_ua.random
                headers = {'User-Agent': random_agent}
                soup = BeautifulSoup(scraper.get(url, headers=headers).text, "html.parser")
                print 'stupd'
                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    columns = row.findAll('td')
                    ip = columns[0].contents[0]
                    port = columns[1].contents[0]
                    ping = int(row.findAll('p')[0].contents[0].split(" ")[0])
                    protocol = columns[4].contents[0].split(',')[0].lower()
                    proxies.append((ip, port, ping, protocol))
                success = True
                if(os.path.exists('../record.csv') == False):
                    with open('../record.csv','w') as csv_file:
                        csv_writer = csv.writer(csv_file,delimiter=',')
                        csv_writer.writerow(["Source","Time"])
                with open('../record.csv','a') as csv_file:
                    csv_writer = csv.writer(csv_file,delimiter=',')
                    csv_writer.writerow(["BR",str(datetime.datetime.now())])

            except Exception as ex:
                print(ex)
                print('Cannot get proxy')
                success = False
                exit()
    filtered_proxies = [p for p in proxies if p[3] in ["http", "https"]]
    return filtered_proxies


def refresh_proxy_queue():
    global proxy_queue
    proxies = fetch_proxies()
    for proxy in proxies:
        proxy_queue.put(proxy)


def filteredLink(url,headers,proxies):
	try:
		link = requests.get(url.encode('ascii','ignore'),headers=headers,proxies=proxies).url
	except requests.exceptions.MissingSchema:
		link = requests.get('http://'+url.encode('ascii','ignore')).url
	except Exception,e:
		link = url
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


global proxy_queue, global_ua
global_ua = UserAgent()
proxy_queue = queue.Queue()

refresh_proxy_queue()



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
		for c in range(len(linkList)):
			random_agent = global_ua.random
			if proxy_queue.empty():
				refresh_proxy_queue()
			proxy = proxy_queue.get()
			headers = {'User-Agent': random_agent}
			proxies = {proxy[3]: "{0}://{1}:{2}".format(proxy[3], proxy[0], proxy[1])}
			filteredList.append(filteredLink(linkList[c],headers,proxies))
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

