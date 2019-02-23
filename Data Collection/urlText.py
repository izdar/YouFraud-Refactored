import re
import urllib2
from bs4 import BeautifulSoup
import json

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def urlText(url):
	try:
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html)
		data = soup.findAll(text=True)
		result = filter(visible, data)
		temp = ""
		for t in list(result):
			if '<' in t and '>' in t:
				continue
			temp += t.encode('ascii','ignore')
		return temp.replace('\n',' ')
	except Exception,e:
		print url
		print str(e)
		return "link not found" 
data = json.load(open('dataset.json'))
# data_test = json.load(open('data_test.json'))
dataBenign= json.load(open('benignData.json'))

# data_test['linkContent'] = []
# for i in range(len(data_test['videoId'])):
# 	linkContent = []
# 	print str(100*(i/float(len(data_test['videoId']))))[:4]+'%'
	
	
# 	for c in data_test['linksUp'][i]:
# 		linkContent.append(urlText(c))
# 	data_test['linkContent'].append(linkContent)

# with open('data_test.json','w') as f:
# 	json.dump(data_test,f)
# # print "t2 DONE"


# print len(data_test['linkContent'])
# print len(data_test['videoId'])


data['linkContent'] = []
for i in range(len(data['videoId'])):
	linkContent = []
	print str(100*(i/float(len(data['videoId']))))[:4]+'%'

	for c in data['linksUp'][i]:
		linkContent.append(urlText(c))
	data['linkContent'].append(linkContent)
with open('dataset.json','w') as f:
	json.dump(data,f)
# print "t1 DONE"
print len(data['linkContent'])
print len(data['videoId'])


dataBenign['linkContent'] = []
for i in range(len(dataBenign['videoId'])):
	print str(100*(i/float(len(dataBenign['videoId']))))[:4]+'%'
	
	linkContent = []
	for c in dataBenign['linksUp'][i]:
		linkContent.append(urlText(c))
	dataBenign['linkContent'].append(linkContent)
print len(dataBenign['linkContent'])
print len(dataBenign['videoId'])

with open('benignData.json','w') as f:
	json.dump(dataBenign,f)
# print "t3 DONE"

