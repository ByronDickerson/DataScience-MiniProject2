#!/usr/bin/env python
# coding: utf-8

# In[5]:


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


# In[132]:



foo = datetime.datetime(2019,2,27,6,30,15)
print(foo)


# In[19]:


#bar charts!
# x axis: time from 00:00 to 05:59, in intervals of 00:15 minutes. so 24 ticks.
#y axis is the number of tweets in that 15-minute time frame. so if there weere 3 yolo tweets between 00:00 and 00:15, then the point would be (00:15,3)
#Only 1 data point per xtick. 

#test = pd.Interval(pd.Timestamp('2019-02-27 18:00:00'), pd.Timestamp('2019-02-27 23:59:59'), closed = 'left')
#stem.Date[0] in test
#d2 = d1 + delta
#test = stem[stem.Date.between(d1, d2, inclusive=True)]
#t2 = test[test.Date.between(d1,d1+datetime.datetime(2019))]
#len(test.index) #this is the number of rows

# so for the first bullet we want len(test.index) to be the value.

#we want 24 values
#scatter1.append([d2,len(test.index)])

from matplotlib.dates import DateFormatter 
import matplotlib.dates as mdates
import matplotlib
import time

#constant
delta = datetime.timedelta(minutes=15) #add this each time youdhssdnfgbbkgnh
bigdelta = datetime.timedelta(hours=6)

time1 = datetime.datetime(2019, 2, 27, 0,0, 0)
#time2 = time1 + delta


#this is the first chunk. we need 8 of these.


def create_axes(d1):
    global delta
    merged_data = []
    d2 = d1+delta
    for i in range(24):
        temp = stem[stem.Date.between(d1,d2,inclusive=True)] #should we make inclusive false?

        #increment the time range by 15 minutes
        d1 = d2
        d2 += delta

        #print(f'At time {d1} we have {len(temp.index)}')

        # add the Date(biggest end) and the Number Of Occurences 
        merged_data.append([d1,len(temp.index)])
    return merged_data

axes1 = create_axes(time1)
time1 += bigdelta

axes2 = create_axes(time1)
time1 += bigdelta

axes3 = create_axes(time1)
time1 += bigdelta

axes4 = create_axes(time1)
time1 += bigdelta

axes5 = create_axes(time1)
time1 += bigdelta

axes6 = create_axes(time1)
time1 += bigdelta

axes7 = create_axes(time1)
time1 += bigdelta

axes8 = create_axes(time1)
time1 += bigdelta


#for i in scatter1:
    #print(f'{i[0]}\t{i[1]}')

s1 = pd.DataFrame(axes1,columns=['Date','Frequency'])    
s2 = pd.DataFrame(axes2,columns=['Date','Frequency'])
s3 = pd.DataFrame(axes3,columns=['Date','Frequency'])
s4 = pd.DataFrame(axes4,columns=['Date','Frequency'])
s5 = pd.DataFrame(axes5,columns=['Date','Frequency'])
s6 = pd.DataFrame(axes6,columns=['Date','Frequency'])
s7 = pd.DataFrame(axes7,columns=['Date','Frequency'])
s8 = pd.DataFrame(axes8,columns=['Date','Frequency'])

print(s1, s2, s3, s4, s5, s6, s7, s8)

#s1.plot.scatter('Date','Frequency')
#plt.scatter(s1.Date, s1.Frequency)
#plt.xlim(s1.Date[0],s1.Date[len(s1.Date.index)-1])
#plt.scatter(list(s1.Date.values),list(s1.Frequency.values),color='r')
#plt.show()
#fig, ax = plt.subplots()

#plt.plot_date(s1.Date, s1.Frequency, c = 'red')

#formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: time.strftime('%H:%M:%S', time.gmtime(ms // 1000)))
#plt.show()
#ax = s1.plot.bar(x='Date', y='Frequency')

#fig, ax = plt.subplots()


#plt.style.use('seaborn-pastel')


# In[46]:



fig, axes = plt.subplots(nrows=4, ncols=2)

#df1.plot(ax=axes[0,0])
#df2.plot(ax=axes[0,1])

import random

s1.plot.bar('Date','Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[0,0])
s2.plot.bar("Date",'Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[0,1])

s3.plot.bar('Date','Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[1,0])
s4.plot.bar("Date",'Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[1,1])

s5.plot.bar('Date','Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[2,0])
s6.plot.bar("Date",'Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[2,1])

s7.plot.bar('Date','Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[3,0])
s8.plot.bar("Date",'Frequency',color=(random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0,0.9), random.uniform(0.4,0.9)),ax=axes[3,1])
#f, ax = plt.subplots(2,4)

#for i in ([s1, s2, s3, s4, s5, s6, s7, s8]):
#s1.plot.bar(i['Date'],i['Frequency'],color='blue')
#fig = plt.figure()




#ax.xaxis.set_major_formatter(fmt)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%M'))
#fig.autofmt_xdate()

#plt.xticks(rotation=45,horizontalalignment='right')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.08)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(top=1,hspace=0.7)
#matplotlib.rcParams['figure.figsize'] = [30,20]
plt.show()



    

