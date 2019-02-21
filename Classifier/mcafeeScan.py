import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json 
import requests

def Scan():
	data = json.load(open('dataset.json'))
	uniqueLinks=[] 
	linkDetect={}
	detectFeature=['status','categorization','reputation']
	for i in range(len(data['linksUp'])):
		for link in data['linksUp'][i]:
			if link not in uniqueLinks:
				uniqueLinks.append(link)
	index=1
	for link in uniqueLinks: 
		try:
			print str(index/float(len(uniqueLinks))*100)[:4]+'%'

			index+=1
			browser = webdriver.Chrome()
			browser.get('https://trustedsource.org/en/feedback/url')
			select = Select(browser.find_element_by_name('product'))
			select.select_by_value('01-ts')
			inputElement= browser.find_element_by_class_name('typeTextLarge')
			inputElement.send_keys(link)
			inputElement.submit()
			contents = BeautifulSoup(browser.page_source,'html.parser')
			result=""

			count=0
			linkDetect[link]={}
			for tag in contents.find_all('td'):
				if "Optional categorization" in tag.text:
					break
				if "http" in tag.text:
					print "here"
					count=1
					c=0
					continue
				if count==1:
					linkDetect[link][detectFeature[c]]=tag.text
					c+=1
			print linkDetect[link]
		except Exception,e:
			print "error"
	with open('linkDetect.json', 'w') as fp:
		json.dump(linkDetect,fp)

	linkDetect = json.load(open('linkDetect.json'))

	total = []
	mcafeeHighRisk=[]
	mcafeeMediumRisk=[]
	mcafeeUnverified=[]
	commonMal=[]

	for i in range(len(data['videoId'])):
		scannedLinks={}
		highRisk={}
		mediumRisk={}
		unverified={}
		check=0
		overlap=0
		for link in data['linksUp'][i]:
			mal=0
			if link in linkDetect:
				scannedLinks[link] = linkDetect[link]
				if linkDetect[link]['reputation']=='High Risk':
					highRisk[link]=linkDetect[link]
					for result in data['totalMalLinks'][i]:
						if link in result:
							print link+'here'+str(i)
							mal=1
				elif linkDetect[link]['reputation']=='Medium Risk':
					mediumRisk[link]=linkDetect[link]
					for result in data['totalMalLinks'][i]:
						if link in result:
							# print link+ 'here2'
							mal=1
				elif linkDetect[link]['reputation']=='Unverified':
					unverified[link]=linkDetect[link]
			else:
				scannedLinks[link] = {'result':'unknown'}
			if mal==1:
				overlap+=1

		commonMal.append(overlap)
		total.append(scannedLinks)
		mcafeeHighRisk.append(highRisk)
		mcafeeMediumRisk.append(mediumRisk)
		mcafeeUnverified.append(unverified)
	data['mcafeeScannedLink'] = total
	data['mcafeeHighRisk'] = mcafeeHighRisk
	data['mcafeeMediumRisk'] = mcafeeMediumRisk
	data['mcafeeUnverified'] = mcafeeUnverified
	data['commonMal']=commonMal
	with open('dataset.json', 'w') as fp:
		json.dump(data,fp)
