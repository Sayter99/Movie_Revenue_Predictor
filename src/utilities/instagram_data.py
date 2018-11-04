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

    def str2InstagramStyledTag(self, tag):
        tag = str(tag)
        working_tag = tag.replace(' ', '')
        working_tag = working_tag.replace('.', '')
        working_tag = working_tag.replace('-', '')
        working_tag = working_tag.replace('\'', '')
        working_tag = working_tag.replace(':', '')
        working_tag = working_tag.replace(',', '')
        working_tag = working_tag.replace('·', '')
        working_tag = working_tag.replace('&', '')
        working_tag = working_tag.replace('/', '')
        working_tag = working_tag.replace('!', '')
        working_tag = working_tag.replace('?', '')
        working_tag = working_tag.replace('(', '')
        working_tag = working_tag.replace(')', '')
        working_tag = working_tag.replace('_', '')
        working_tag = working_tag.replace('@', '')
        working_tag = working_tag.replace('{', '')
        working_tag = working_tag.replace('}', '')
        working_tag = working_tag.replace('#', '')
        working_tag = working_tag.replace('$', '')
        working_tag = working_tag.replace('%', '')
        working_tag = working_tag.replace('^', '')
        working_tag = working_tag.replace('+', '')
        working_tag = working_tag.replace('\\', '')
        working_tag = working_tag.replace('\"', '')
        working_tag = working_tag.replace('[', '')
        working_tag = working_tag.replace(']', '')
        working_tag = working_tag.replace('~', '')
        working_tag = working_tag.replace('’', '')
        working_tag = working_tag.replace('°', '')
        return working_tag

    def getHashtagCounts(self, tag):
        if str(tag) == 'N/A':
            return 0
        if str(tag) == '' or str(tag) == ' ':
            return 0
        retry = 5
        working_tag = self.str2InstagramStyledTag(tag)
        tags = self.acquired.get(working_tag, 0)
        if tags != 0:
            print ('INFO: Tags of ' + working_tag + ' = ' + str(tags))
            return tags
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
    
    def refillMissingTags(self, data):
        if (data['actor1_hashtags'] == 0):
            if (data.cast.split(',')[0].replace(' ', '') != 'N/A'):
                data.actor1_hashtags = self.getHashtagCounts(data.cast.split(',')[0].replace(' ', ''))
        if (data['actor2_hashtags'] == 0):
            if (data.cast.split(',')[1].replace(' ', '') != 'N/A'):
                data.actor2_hashtags = self.getHashtagCounts(data.cast.split(',')[1].replace(' ', ''))
        if (data['actor3_hashtags'] == 0):
            if (data.cast.split(',')[2].replace(' ', '') != 'N/A'):
                data.actor3_hashtags = self.getHashtagCounts(data.cast.split(',')[2].replace(' ', ''))
        if (data['director_hashtags'] == 0):
            if (data.crew.replace(' ', '') != 'N/A'):
                data.director_hashtags = self.getHashtagCounts(data.crew.replace(' ', ''))
        if (data['movie_hashtags'] == 0):
            if (data.title_x.replace(' ', '') != 'N/A'):
                data.movie_hashtags = self.getHashtagCounts(data.title_x.replace(' ', ''))
        pass

    def clearCache(self):
        self.acquired.clear()
