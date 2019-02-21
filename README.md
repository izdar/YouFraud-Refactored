Data Collection:
	
	channels.txt -> channelCrawler -> domainChannelsVids.json

	dataset.json + data_test.json + benignData.json -> urlText.py -> dataset.json + data_test.json + benignData.json with linkContent (URL textual data)

Classifier:

	AllClassifiedScaledChan.json -> classifyScaledChan.py -> AllClassifiedScaledChan.json with classifications

	classifyDomains.py -> classifyDomains.json -> webExtract.py -> classifyDomains.json

Analysis:
