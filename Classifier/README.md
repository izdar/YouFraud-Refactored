Data Collection:
	
	queries.txt -> querycrawler.py -> dataset.json

	queriesScaled.txt ->queryCrawler.py -> uniqueScaled.json  

	channels.txt -> channelCrawler -> domainChannelsVids.json

	dataset.json + data_test.json + benignData.json -> urlText.py -> dataset.json + data_test.json + benignData.json with linkContent (URL textual data)

Classifier:
	
	dataset.json->linksFeature.py-> dataset.json

	dataset.json -> classifier.py -> dataset.json + falseClassified.json	

	uniqueScaled.json -> scaledClassifier.py -> uniqueScaled.json 

	AllClassifiedScaledChan.json -> classifyScaledChan.py -> AllClassifiedScaledChan.json with classifications

	classifyDomains.py -> classifyDomains.json -> webExtract.py -> classifyDomains.json

Analysis:
