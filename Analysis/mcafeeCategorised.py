import json

dataset = json.load(open('dataset.json'))

dict={}
malDict={}

for i in range(len(dataset['videoId'])):
	for x in dataset['mcafeeScannedLink'][i].keys():
		try:
		# print dataset['mcafeeScannedLink'][i][x]
		 	categorization=dataset['mcafeeScannedLink'][i][x]['categorization']
		 	if categorization not in dict:
		 		dict[categorization]=[]
			if x not in dict[categorization]:
 				dict[categorization].append(x) 
		except Exception,e:
			if 'notCategorized' not in dict:
				dict['notCategorized']=[]
			if x not in dict['notCategorized']:
 				dict['notCategorized'].append(x)

			print str(e)+'1'		
	for x in dataset['mcafeeHighRisk'][i].keys():
		try:
	 		categorization=dataset['mcafeeHighRisk'][i][x]['categorization']
		 	if categorization not in malDict:
		 		malDict[categorization]=[]
			if x not in malDict[categorization]:
		 		malDict[categorization].append(x)
		except Exception,e:
			if 'notCategorized' not in malDict:
				malDict['notCategorized']=[]
			if x not in malDict['notCategorized']:
	 			malDict['notCategorized'].append(x)
			print str(e)+'2'
	for x in dataset['mcafeeMediumRisk'][i].keys():
		try:
	 		categorization=dataset['mcafeeMediumRisk'][i][x]['categorization']
		 	if categorization not in malDict:
		 		malDict[categorization]=[]
			if x not in malDict[categorization]:
				malDict[categorization].append(x)
		except Exception,e:
			if 'notCategorized' not in malDict:
				malDict['notCategorized']=[]
			if x not in malDict['notCategorized']:
	 			malDict['notCategorized'].append(x)
			print str(e)+'3'		

with open('mcafeeMalCategorised.json', 'w') as fp:
	    json.dump(malDict, fp)		
with open('mcafeeCategorised.json', 'w') as fp:
	    json.dump(dict, fp)
