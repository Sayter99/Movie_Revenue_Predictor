import urllib.request
import json
import time

def getHashtagCounts(tag):
    working_tag = tag.replace(' ', '')
    working_tag = working_tag.replace('.', '')
    print('INFO: Getting tag counts of ' + working_tag)
    url = 'https://www.instagram.com/explore/tags/' + working_tag + '?__a=1'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    tags = 0
    try:
        tags = data['graphql']['hashtag']['edge_hashtag_to_media']['count']
    except:
        pass
    if tags == 0:
        print ('WARNING: Failed to get tag counts of ' + working_tag)
    print ('INFO: Tags of ' + working_tag + ' = ' + str(tags))
    time.sleep(1.5)
    return tags
