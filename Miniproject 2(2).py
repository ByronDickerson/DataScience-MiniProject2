#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import copy
import datetime


import tweepy
f = open('twitter_tokens.txt','r')
consumer_key = f.readline().rstrip('\n')
consumer_secret = f.readline().rstrip('\n')
app_key = f.readline().rstrip('\n')
app_secret = f.readline().rstrip('\n')

#uses OAuth which is pretty standard

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)# handshake

auth.set_access_token(app_key,app_secret) #access to timeline of the account

api = tweepy.API(auth, wait_on_rate_limit=True) #send it all in to get the API object

#reads in csv files and merges the two days for each hashtag
def mergeDFs(file1,file2):
    temp1 = pd.read_csv(f'{file1}.csv',header=None,names=['ID','Date','User','Followers','RTs','Favorites'])
    temp2 = pd.read_csv(f'{file2}.csv',header=None,names=['ID','Date','User','Followers','RTs','Favorites'])
    return pd.concat([temp1,temp2])

#reference for df.loc[...]
#https://stackoverflow.com/questions/15741759/find-maximum-value-of-a-column-and-return-the-corresponding-row-values-using-pan
def followers(df):
    df = df.reset_index()
    temp = df.loc[df['Followers'].idxmax()]
    print(f'{temp["Followers"]}\t\t@{temp["User"]}')
    
def retweets(df):
    df = df.reset_index()
    temp = df.loc[df['RTs'].idxmax()]
    printTweet(temp["ID"])

def favorites(df):
    df = df.reset_index()
    temp = df.loc[df['Favorites'].idxmax()]
    printTweet(temp["ID"])
    
#grabs tweet by ID and prints out information about it
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


def makeDatetime(date):
    if type(date) == str:
        date = date.split()
        year = int(date[5])
        month = 2 #it's always february dont worry about it
        day = int(date[2])
        time = date[3].split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        return datetime.datetime(year, month, day, hour, minute, second)
          
          
# dataframe formatting. each hashtag is its own dataframe.
stem = mergeDFs('stem_27','stem_28').reset_index()
csforall = mergeDFs('csforall_27','csforall_28').reset_index()
equality = mergeDFs('equality_27','equality_28').reset_index()
yolo = mergeDFs('yolo_27','yolo_28').reset_index()
          
# Convert date strings into datetime objects.
# Reference for apply(lambda x...)
#https://stackoverflow.com/questions/34962104/pandas-how-can-i-use-the-apply-function-for-a-single-column
stem.Date = stem.Date.apply(lambda x: makeDatetime(x))
csforall.Date = csforall.Date.apply(lambda x: makeDatetime(x))
equality.Date = equality.Date.apply(lambda x: makeDatetime(x))
yolo.Date = yolo.Date.apply(lambda x: makeDatetime(x))

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


# In[30]:


#bar charts!
# x axis: time from 00:00 to 05:59, in intervals of 00:15 minutes. so 24 ticks.
#y axis is the number of tweets in that 15-minute time frame. so if there weere 3 yolo tweets between 00:00 and 00:15, then the point would be (00:15,3)
#Only 1 data point per xtick. 

# so for the first bullet we want len(test.index) to be the value.

from matplotlib.dates import DateFormatter 
import matplotlib.dates as mdates
import matplotlib
import time

#matplotlib.rcParams['figure.figsize'] = [15, 10]

#constant
delta = datetime.timedelta(minutes=15) #add this each time youdhssdnfgbbkgnh
bigdelta = datetime.timedelta(hours=6)

time1 = datetime.datetime(2019, 2, 27, 0,0, 0)


#this is the first chunk. we need 8 of these.


def create_axes(d1,data,bd=True):
    global bigdelta
    merged_data = []
    if bd:
        d2 = d1 + bigdelta
        r = 8
    else:
        d2 = d1 + delta
        r = 28
    
    for i in range(r):
        temp = data[data.Date.between(d1,d2,inclusive=True)] #should we make inclusive false?

        #increment the time range by 15 minutes
        d1 = d2
        if bd:
            d2 += bigdelta
        else:
            d2 += delta

        #print(f'At time {d1} we have {len(temp.index)}')

        # add the Date(biggest end) and the Number Of Occurences 
        if bd:
            timestr = str(d1.month)+ '/' +str(d1.day) + ' ' + str(d1.hour) + ':' + str(d1.minute)
        else:
            timestr = str(d1.hour) + ':' + str(d1.minute)
        merged_data.append([timestr,len(temp.index)])
        #print(timestr)
    return merged_data

#these are dataframes
axes_stem     = create_axes(time1, stem)
axes_csforall = create_axes(time1, csforall)
axes_equality = create_axes(time1, equality)
axes_yolo     = create_axes(time1, yolo)

df_bar_stem     = pd.DataFrame(axes_stem,     columns= ['Date','Frequency'])    
df_bar_csforall = pd.DataFrame(axes_csforall, columns = ['Date','Frequency'])
df_bar_equality = pd.DataFrame(axes_equality, columns = ['Date','Frequency'])
df_bar_yolo     = pd.DataFrame(axes_yolo,     columns = ['Date','Frequency'])


import random

c = (0.4, 0.4, 0.8,0.5)
c2 = (0.8, 0.4, 0.4,0.5)
c3 = (0.4, 0.8, 0.4,0.5)
c4 = (0.4, 0.4, 0.4,0.5)

ax  = df_bar_stem.plot.bar(    'Date', 'Frequency', color = c,  rot=0)
ax2 = df_bar_csforall.plot.bar('Date', 'Frequency', color = c2, rot=0)
ax3 = df_bar_equality.plot.bar('Date', 'Frequency', color = c3, rot=0)
ax4 = df_bar_yolo.plot.bar(    'Date', 'Frequency', color = c4, rot=0)


ax.set_ylabel('Frequency')
ax.set_title("#stem")

ax2.set_ylabel('Frequency')
ax2.set_title("#csforall")

ax3.set_ylabel('Frequency')
ax3.set_title("#equality")

ax4.set_ylabel('Frequency')
ax4.set_title("#yolo")




plt.show()


# In[31]:


#cs vs stem:......scatter boys....

stem_15m = create_axes(time1,stem,bd=False)
cs_15m = create_axes(time1,csforall,bd=False)

df_stem_15m = pd.DataFrame(stem_15m,     columns= ['Date','Frequency'])    
df_cs_15m = pd.DataFrame(cs_15m,     columns= ['Date','Frequency'])    

ax = plt.scatter(x=df_stem_15m['Date'],y=df_stem_15m['Frequency'])

