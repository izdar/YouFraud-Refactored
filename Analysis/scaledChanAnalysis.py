import json
import datetime

gChannels=json.load(open('fraudScaledChannels.json'))
# count=0
# videos=0
# for i in range(0,50):
# 		try:
# 			chanVideos=json.load(open('classifyScaledChan'+str(i)+'.json'))
# 			count+=len(chanVideos)
# 			for channel in chanVideos:
# 				videos+=len(chanVideos[channel]['videoId'])
# 		except:
# 			continue
# print videos
# print count
# Chans={}
# for channel in clasChan:
# 	if clasChan[channel]['totalVideos']>10:
# 		Chans[channel]={}
# 		Chans[channel]=clasChan[channel]

# with open('ChannelAnalysis.json', 'w') as fp:
#     json.dump(Chans, fp)
# gChannels=json.load(open('ChannelAnalysis.json'))
today = datetime.date.today()
for channel in gChannels:
	for i in range(0,50):
		try:
			chanVideos=json.load(open('classifyScaledChan'+str(i)+'.json'))
		except:
			continue
		if channel in chanVideos:
			somedays=[datetime.date(int(x[0:4]), int(x[5:7]), int(x[8:10])) for x in chanVideos[channel]['time']]
			chanVideos[channel]['time']=[int(str((today-someday).days)) for someday in somedays]
			chanVideos[channel]['commentCount']=[0 if x=='No commentCount' else int(x) for x in chanVideos[channel]['commentCount']]
			chanVideos[channel]['viewCount']=[0 if x=='No viewCount' else int(x) for x in chanVideos[channel]['viewCount']]
	
			gChannels[channel]['avgComments']=sum(chanVideos[channel]['commentCount'])/len(chanVideos[channel]['commentCount'])
			gChannels[channel]['avgViews']=sum(chanVideos[channel]['viewCount'])/len(chanVideos[channel]['viewCount'])
			gChannels[channel]['avgtimeDiff']=sum(chanVideos[channel]['time'])/len(chanVideos[channel]['time'])


with open('ChannelAnalysis0.json', 'w') as fp:
    json.dump(gChannels, fp)

for channel in clasChan:
	if clasChan[channel]['avgtimeDiff']<365:
		Chans[channel]={}
		Chans[channel]=clasChan[channel]

with open('ChannelAnalysis2.json', 'w') as fp:
    json.dump(Chans, fp)

print len(clasChan)
print len(gChannels)
print len(Chans)