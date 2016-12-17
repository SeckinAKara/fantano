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
        #print pageToken
    else:
        break   
    

for video in all_videos:
    if 'REVIEW' in video and 'TRACK' not in video:
        reviews[video] = deepcopy(all_videos[video])

open('fantanoreviews.txt', 'w').write(str(reviews))







import codecs
import re
from ast import literal_eval

fantano = codecs.open('fantanoreviews.txt', encoding='utf+8')
reviews = fantano.read()
fantano.close()
reviews = literal_eval(reviews)

albums = {}
non_albums = {}

for title in reviews:
    for word in ['ALBUM', 'MIXTAPE', ' EP', 'COMPILATION', 'MIX']:
        if word in title:
            albums[title] = reviews[title]
            break
    else:
        non_albums[title] = reviews[title]

rating = re.compile(r'\n\d{1,2}/10')

table = open('fantanotable.txt', 'w')
total = ''

for video in albums:
    dash = video.count('- ')
    if dash == 1:
        artist = video.split('- ')[0]
        title = video.split('- ')[1]
        for word in ['ALBUM', 'MIXTAPE', ' EP', 'COMPILATION', 'MIX']:
            if word in title:
                title = title.split(word)[0]
    if 'self-titled' in video.lower():
        artist = video.split('- ')[0]
        title = artist
        for word in ['ALBUM', 'MIXTAPE', ' EP', 'COMPILATION', 'MIX']:
            if word in title:
                title = title.split(word)[0]
    title = title.strip()
    artist = artist.strip()
    score = rating.findall(albums[video][1])
    date = albums[video][0]
    date = date[:10]
    if len(score) == 1:
        score = score[0].replace('\n', '')
        score = score.replace('/10', '')
        if dash == 1:
            line = artist + '\t' + title + '\t' + date + '\t' + score + '\n'
        else:
            line = video + '\t'*2 + date + '\t' + score + '\n'
    else:
        if dash == 1:
            line = artist + '\t' + title + '\t' + date + '\t' + '\n'
        else:
            line = video + '\t'*2 + date + '\t' + '\n'
    total += line

#print total

table.write(total.encode('utf+8'))
table.close()







import gspread
from oauth2client.service_account import ServiceAccountCredentials

json_key = 'Drive Python-18694af03e99.json'
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key, scope)


new_reviews = open("fantanotable.txt", 'r').readlines()

gc = gspread.authorize(credentials)
wks = gc.open("Anthony Fantano Reviews").sheet1


album_names = wks.col_values(2)
last_row = str(album_names.index("Plastic Beach") + 1)
valued_cells = wks.range("A1:D" + last_row)

for row, review in enumerate(new_reviews):
    new_reviews[row] = review.split('\t')

new_reviews = sorted(new_reviews, key = lambda x: x[2])[::-1]
for review in new_reviews:
    if valued_cells[1].value in review[1]:
        reviews_to_add = new_reviews.index(review)

for review in new_reviews[reviews_to_add+1:]:
    if review[2] == new_reviews[reviews_to_add][2] and review[1] not in [(lambda x: x.value)(x) for x in valued_cells[:20]]:
        new_reviews.insert(reviews_to_add, review)
        reviews_to_add += 1
    else:
        break



if reviews_to_add == 0:
    exit(0)

cells_to_update = wks.range("A" + str(1 + reviews_to_add) + ":D" + str(int(last_row) + reviews_to_add))

for row in range(0, len(cells_to_update))[::-1]:
    cells_to_update[row].value = valued_cells[row].value

wks.update_cells(cells_to_update)

all_new_reviews = []
for review in new_reviews[:reviews_to_add]:
    all_new_reviews.append(review[0])
    all_new_reviews.append(review[1])
    all_new_reviews.append(review[2])
    all_new_reviews.append(review[3])


cells_to_update = wks.range("A1:D" + str(len(all_new_reviews)/4))
for row in range(0, len(cells_to_update)):
    cells_to_update[row].value = all_new_reviews[row].decode('utf-8')

wks.update_cells(cells_to_update)

