import json

domain = json.load(open('domainList.json'))
mcafee = json.load(open('mcafeeCategorized.json'))
data = json.load(open('dataset.json'))
suspect = {}
countOriginal = 0
countMcafee = 0

for url in domain:
	for category in mcafee:
		for list in mcafee[category]:
			if url in list:
				if category not in suspect:
					suspect[category] = []
				if url not in suspect[category]:
					suspect[category].append(url)
					countOriginal += 1
				break

check = 0
for category in suspect:
	for c in range(len(suspect[category])):
		for i in range(len(data['videoId'])):
			for scanned in data['mcafeeScannedLink'][i]:
				if suspect[category][c] in scanned:
					suspect[category][c] = (suspect[category][c], data['videoId'][i])
					countMcafee += 1
					check = 1
					break
			if check:
				break
		check = 0


print countOriginal
print countMcafee

with open('DomainListCategory.json','w') as f:
	json.dump(suspect,f)
