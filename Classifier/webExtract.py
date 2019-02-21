import json

# words = ['click',' ad','register',' sign ','money','paid']

# data1 = json.load(open('t1.json'))
# data2 = json.load(open('t2.json'))
# data3 = json.load(open('t3.json'))

# suspects = []
# for i in range(len(data1['videoId'])):
# 	for c in range(len(data1['linkContent'][i])):
# 		score = 0
# 		for word in words:
# 			if word in data1['linkContent'][i][c]:
# 				score += 1
# 		if score > 1:
# 			if data1['linksUp'][i][c] not in suspects:
# 				suspects.append(data1['linksUp'][i][c])
# for i in range(len(data2['videoId'])):
# 	for c in range(len(data2['linkContent'][i])):
# 		score = 0
# 		for word in words:
# 			if word in data2['linkContent'][i][c]:
# 				score += 1
# 		if score > 1:
# 			if data2['linksUp'][i][c] not in suspects:
# 				suspects.append(data2['linksUp'][i][c])
# for i in range(len(data3['videoId'])):
# 	for c in range(len(data3['linkContent'][i])):
# 		score = 0
# 		for word in words:
# 			if word in data3['linkContent'][i][c]:
# 				score += 1
# 		if score > 1:
# 			if data3['linksUp'][i][c] not in suspects:
# 				suspects.append(data3['linksUp'][i][c])
# print len(suspects)
suspects = json.load(open('classifyDomains.json'))

safe = ['youtube','twitter','insta','imgur','facebook','google','amazon','itunes','goo.gl','amzn','yout','blogspot']
filtered = []
for video in suspects:
	c = 0
	for word in safe:
		if word in video:
			c+=1
	if c == 0:
		filtered.append(video)

with open('filteredList.json','w') as f:
	json.dump(filtered,f)

final = []
for site in filtered:
	c=0
	ind = 0
	for letter in site:
		ind+=1
		if letter == '/':
			c+=1
		if c==3:
			final.append(site[:ind])
			break

with open('domainList.json','w') as f:
	json.dump(final,f)
