import urllib2
import json
from copy import deepcopy

api = 'AIzaSyBcXY8ifCmFKi1rRociakxrHZcghJRsLuA'
pageToken = ''
url = 'https://www.googleapis.com/youtube/v3/playlistItems?'+pageToken+'&part=snippet&playlistId=UUt7fwAhXDy3oNFTAzF2o8Pw&key='+api+'&maxResults=50'

info = json.load((urllib2.urlopen(url)))
all_videos = {}; reviews = {}

for i in range(2):
    for video in info['items']:
        context = video['snippet']
        all_videos[context['title']] = (context['publishedAt'],context['description'])
    if 'nextPageToken' in info:
        pageToken = '&pageToken='+info['nextPageToken']
        url = 'https://www.googleapis.com/youtube/v3/playlistItems?'+pageToken+'&part=snippet&playlistId=UUt7fwAhXDy3oNFTAzF2o8Pw&key='+api+'&maxResults=50'
        info = json.load((urllib2.urlopen(url)))
        print pageToken
    else:
        break   
    

for video in all_videos:
    if 'REVIEW' in video and 'TRACK' not in video:
        reviews[video] = deepcopy(all_videos[video])

open('fantanoreviews.txt', 'w').write(str(reviews))
