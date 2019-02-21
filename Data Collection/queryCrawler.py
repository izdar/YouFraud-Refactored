from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2
import sys
import threading
import time

DEVELOPER_KEY = "AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Authorization for using the Youtube API v3
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

sys.setrecursionlimit(20000)

def youtube_search(q, token,numOfResults, res,order="relevance",  location=None, location_radius=None):
    # change res to number of results required
    if (len(res)%500==0 or len(res)%500<5) and len(res)>5:
        time.sleep(30)

    if len(res) >= int(numOfResults):
        return

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    location=location,
    locationRadius=location_radius).execute()

    for search_result in search_response.get("items", []):
    	res.append(search_result)
        
    youtube_search(q, search_response.get("nextPageToken"), numOfResults, res)

def search(query,numOfResults):
    #res is the list of results
    res = []
    
    # Change search query to the required query by changing the first argument of this function
    threadLock.acquire()
    
    youtube_search(query, None,numOfResults,res)
    threadLock.release()
    
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    commentCount = []
    category = []
    videos = []
    comments = []
    tags = []
    description = []

    chan = {}
    count = 0.0
    for search_result in res:
        count += 1.0
        if (count%500==0 or count%500<5) and len(res)>5:
            time.sleep(30)
        print threading.currentThread().getName()+' ' +str(100*(count/float(numOfResults)))[:4]+'%'
        title.append(search_result['snippet']['title']) 

        videoId.append(search_result['id']['videoId'])
        threadLock.acquire()

        response = youtube.videos().list(
        part='statistics, snippet',
        id=search_result['id']['videoId']).execute()
        threadLock.release()

        try:
            channelId.append(response['items'][0]['snippet']['channelId'])
        except:
            channelId.append('No channelId')
        try:
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
        except:
            channelTitle.append('No channelTitle')
        try:
            categoryId.append(response['items'][0]['snippet']['categoryId'])
        except:
            categoryId.append('No categoryId')
        try:
            viewCount.append(response['items'][0]['statistics']['viewCount'])
        except:
            viewCount.append('No viewCount')
        try:
            tags.append(response['items'][0]['snippet']['tags'])
        except:
            tags.append('No tags')
        try:
            description.append(response['items'][0]['snippet']['description'])
        except:
            description.append('No description')
        try:
            commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + search_result['id']['videoId'] + "&maxResults=50",timeout=60).read())
            c = []
            for k in range(len(commentsOnVideo['items'])):
                c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
            comments.append(c)
        except:
            comments.append('No comments')
        try:
            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount.append(response['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append("No commentCount")
        except:
            commentCount.append("No commentCount")
    youtube_dict = {'description': description, 'tags': tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'commentCount':commentCount, 'comments': comments}
    threadLock.acquire()
    # data = json.load(open('dataScaled.json'))
    # for keys in youtube_dict:
    #     data[keys] += youtube_dict[keys]
    with open('affiliateMarketing.json', 'w') as fp:
        json.dump(youtube_dict, fp)
    print threading.currentThread().getName()+' WRITING TO JSON FILE'
    threadLock.release()
threadLock=threading.Lock()

index=1
with open('queries.txt','r') as f:
    for query in f:
        threading.Thread(name=str(index),target=search,args=(query,100)).start()
        index+=1
