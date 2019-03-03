import pandas as pd
import numpy as np
import matplotlib.pylab as plt


def mergeDFs(file1,file2):
    temp1 = pd.read_csv(f'{file1}.csv',header=None,names=['ID','Date','User','Followers','RTs','Favorites'])
    temp2 = pd.read_csv(f'{file2}.csv',header=None,names=['ID','Date','User','Followers','RTs','Favorites'])
    return pd.concat([temp1,temp2])

def followers(df):
    df = df.reset_index()
    temp = df.loc[df['Followers'].idxmax()]
    print(f'{temp["Followers"]}\t\t@{temp["User"]}')
    
def retweets(df):
    df = df.reset_index()
    temp = df.loc[df['RTs'].idxmax()]
    printTweet(temp["ID"])
    #print(f'{temp["RTs"]} \t\t {temp["ID"]}')

def favorites(df):
    df = df.reset_index()
    temp = df.loc[df['Favorites'].idxmax()]
    printTweet(temp["ID"])
    
def printTweet(id):
    #ID
    #@user:
    #text
    #RTs
    #Favs
    
    tweet = api.get_status(id)._json#['text']
    print(f'Tweet ID: {id}')
    print(f"{tweet['user']['name']}\t@{tweet['user']['screen_name']}")
    print(tweet['text'])
    print(f'RTs: {tweet["retweet_count"]}\t\tFavorites: {tweet["favorite_count"]}')
          
          

stem = mergeDFs('stem_27','stem_28')
csforall = mergeDFs('csforall_27','csforall_28')
equality = mergeDFs('equality_27','equality_28')
yolo = mergeDFs('yolo_27','yolo_28')

print('Most frequent user per hashtag:')
print(f'#stem\t\t{stem["User"].mode()[0]}')
print(f'#csforall\t{csforall["User"].mode()[0]}')
print(f'#equality\t{equality["User"].mode()[0]}')
print(f'#yolo\t\t{yolo["User"].mode()[0]}')
      

print('\nUser with the most followers, per hashtag:')
print('#stem\t\t',end='')
followers(stem)
print('#csforall\t',end='')
followers(csforall)
print('#equality\t',end='')
followers(equality)
print('#yolo\t\t',end='')
followers(yolo)

print('\nTweet with most retweets per hashtag:')
print('#stem')
retweets(stem)
print('\n#csforall')
retweets(csforall)
print('\n#equality')
retweets(equality)
print('\n#yolo')
retweets(yolo)

      
print('\nTweet with most favorites per hashtag:')
print('#stem')
favorites(stem)
print('\n#csforall')
favorites(csforall)
print('\n#equality')
favorites(equality)
print('\n#yolo')
favorites(yolo)