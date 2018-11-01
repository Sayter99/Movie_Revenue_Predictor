import urllib.request
import urllib.parse
import json
import time

class AcquireJson():
    def __init__(self):
        self.acquired = {}

    def tryGetInstagramJson(self, url):
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            time.sleep(2)
        except Exception as e:
            print('Failed to get hashtag info of ' + url)
            print(str(e))
            time.sleep(5)
            return None
        return data

    def getHashtagCounts(self, tag):
        retry = 5
        working_tag = tag.replace(' ', '')
        working_tag = working_tag.replace('.', '')
        working_tag = working_tag.replace('-', '')
        working_tag = working_tag.replace('\'', '')
        working_tag = working_tag.replace(':', '')
        tags = self.acquired.get(working_tag, 0)
        if tags != 0:
            print ('INFO: Tags of ' + working_tag + ' = ' + str(tags))
            return tags
        if working_tag == 'N/A':
            return 0
        print('INFO: Getting tag counts of ' + working_tag)
        url = 'https://www.instagram.com/explore/tags/' + urllib.parse.quote_plus(working_tag) + '?__a=1'
        for i in range(retry):
            if i > 0:
                print('retry... [' + url + ']')
            data = self.tryGetInstagramJson(url)
            if data != None:
                break
        tags = 0
        try:
            tags = data['graphql']['hashtag']['edge_hashtag_to_media']['count']
        except:
            pass
        if tags == 0:
            print ('WARNING: Failed to get tag counts of ' + working_tag)
        print ('INFO: Tags of ' + working_tag + ' = ' + str(tags))
        self.acquired[working_tag] = tags
        return tags

    def clearCache(self):
        self.acquired.clear()
