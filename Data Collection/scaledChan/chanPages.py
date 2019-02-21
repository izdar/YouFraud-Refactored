from apiclient.discovery import build
import urllib
import json

def get_all_video_in_channel(channel_id):
    api_key = 'AIzaSyClserQ1cuNOX9SssQT6-BvBf65JZZ1Lk4'

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        try:
            inp = urllib.urlopen(url)
        except:
            inp = []
            return inp
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(i['id']['videoId'])
                i['snippet']['title']

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links
# videos=get_all_video_in_channel('UCmMM03CkbXnu6TuDeTIvc0w')
# print len(videos)
# print videos