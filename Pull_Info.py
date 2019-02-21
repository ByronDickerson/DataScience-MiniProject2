storage = []
for item in tweepy.Cursor(api.search, q="#csforall",tweet_mode='extended').items(20):
    parsedItem = item._json
    #if 'retweeted_status' in parsedItem:
        #print(parsedItem['retweeted_status']['full_text'])
    print(parsedItem['user']['screen_name'])
    print(parsedItem["full_text"])
    print(parsedItem["retweet_count"])
    print(parsedItem["favorite_count"])
    print(parsedItem['user']['followers_count'])
    storage.append({'screen_name':parsedItem['user']['screen_name'], 
                    'followers_count':parsedItem['user']["followers_count"], 
                    'retweet_count':parsedItem["retweet_count"], 
                    'favorite_count':parsedItem["favorite_count"]})
    #print(parsedItem)
    print('===============================')
