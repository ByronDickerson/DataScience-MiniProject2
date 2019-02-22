storage = []
for item in tweepy.Cursor(api.search, q="#yolo",tweet_mode='extended', since='2019-02-17',until='2019-02-18').items(20):
    parsedItem = item._json
    #if 'retweeted_status' in parsedItem:
        #print(parsedItem['retweeted_status']['full_text'])
    print(parsedItem['user']['screen_name'])
    print(parsedItem["full_text"])
    print(parsedItem["retweet_count"])
    print(parsedItem["favorite_count"])
    print(parsedItem['user']['followers_count'])
    print(parsedItem["created_at"])
    storage.append({'screen_name':parsedItem['user']['screen_name'],
                    'text':parsedItem['full_text'],
                    'followers_count':parsedItem['user']["followers_count"], 
                    'retweet_count':parsedItem["retweet_count"], 
                    'favorite_count':parsedItem["favorite_count"],
                   'created_at':parsedItem["created_at"]})
    #print(parsedItem)
    print('===============================')
