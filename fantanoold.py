from ast import literal_eval
import codecs
import re

videos = codecs.open('fantanovideos.txt', encoding='utf+8').read()
videos = literal_eval(videos)

old_videos = {}

for video in videos:
    if videos[video][0] < videos['Flying Lotus- Cosmogramma ALBUM REVIEW'][0]:
        old_videos[video] = videos[video]

old_reviews = {}

for video in old_videos:
    if 'Review' in video and 'Track Review' not in video:
        old_reviews[video] = old_videos[video]

del old_reviews['MIA- Born Free Review']

old_albums = {}; old_tracks = {}

for video in old_reviews:
    if 'track' not in old_reviews[video][1]:
        track = 1000000
    else:
        track = old_reviews[video][1].index('track')
    if 'album' not in old_reviews[video][1] and 'compilation' in old_reviews[video][1]:
        album = old_reviews[video][1].index('compilation')
    elif 'album' not in old_reviews[video][1] and 'LP ' in old_reviews[video][1]:
        album = old_reviews[video][1].index('LP ')
    elif 'album' in old_reviews[video][1]:
        album = old_reviews[video][1].index('album')
    else:
        album = 1000000
    if 'single' in old_reviews[video][1]:
        single = old_reviews[video][1].index('single')
        if single < track:
            track = single
    if album < track:
        old_albums[video] = old_reviews[video]
    elif track < album:
        old_tracks[video] = old_reviews[video]
    else:
        print video

rating = re.compile(r'\d+/10')
for video in old_albums:
    if video == 'Black Tambourine Anthology Review':
        artist = 'Black Tambourine'
        title = 'Black Tambourine'
    elif 'Self-Titled' in video:
        artist = video.split('- ')[0]
        title = artist
    else:
        artist = video.split('- ')[0]
        title = video.split('- ')[1]
        title = title.replace('Review', '')
    date = old_albums[video][0][:10]
    score = rating.findall(old_albums[video][1])[0][0]
    print artist + '\t' + title + '\t' + date + '\t' + score + '\t'
