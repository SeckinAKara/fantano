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

table.write(total.encode('utf+8'))
