#!/usr/bin/env python
# coding: utf-8

# Answer this: what shape do you need your data?

# In[1]:


import  numpy as np
import pandas as pd
import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import confusion_matrix
from patsy import dmatrices, dmatrix
import matplotlib.pyplot as plt
from sklearn import datasets


# In[2]:


# import tweet data

csforall_27 = pd.read_csv("csforall_27.csv")
csforall_28 = pd.read_csv("csforall_28.csv")

equality_27 = pd.read_csv("equality_27.csv")
equality_28 = pd.read_csv("equality_28.csv")

stem_27 = pd.read_csv("stem_27.csv")
stem_28 = pd.read_csv("stem_28.csv")

yolo_27 = pd.read_csv("yolo_27.csv")
yolo_28 = pd.read_csv("yolo_28.csv")

csforall = pd.concat([csforall_27, csforall_28])
equality = pd.concat([equality_27, equality_28])
stem = pd.concat([stem_27, stem_28])
yolo = pd.concat([yolo_27, yolo_28])


# In[3]:


# split tweet time into a more useable format (separate timestamp into component elements, save day and time)

new = csforall["time created"].str.split(" ", expand = True) 
csforall["day"] = new[2]
csforall["time"] = new[3]

new = equality["time created"].str.split(" ", expand = True) 
equality["day"] = new[2]
equality["time"] = new[3]

new = stem["time created"].str.split(" ", expand = True) 
stem["day"] = new[2]
stem["time"] = new[3]

new = yolo["time created"].str.split(" ", expand = True) 
yolo["day"] = new[2]
yolo["time"] = new[3]


# In[13]:


# split tweet time into a more useable format, (separate time column into hours, min, sec; save hours, tens place of min)

new = csforall["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
csforall["hour"] = new[0]
csforall["min"] = new[4]

new = equality["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
equality["hour"] = new[0]
equality["min"] = new[4]

new = stem["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
stem["hour"] = new[0]
stem["min"] = new[4]

new = yolo["time"].str.split(":", expand = True) 
new[4] = [time[0] for time in new[1]]
yolo["hour"] = new[0]
yolo["min"] = new[4]


# In[14]:


# period = day/hour, format: ddhhm

csforall['period'] = pd.to_numeric(csforall[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
equality['period'] = pd.to_numeric(equality[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
stem['period'] = pd.to_numeric(stem[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))
yolo['period'] = pd.to_numeric(yolo[['day', 'hour','min']].apply(lambda x: ''.join(x), axis=1))


# In[15]:


# compile freqencies over 6 hour chunks

# pull all yolo tweets from the first six hours of Feb 27th
#test = yolo.loc[(yolo['day'] == 27) & (yolo['hour'] >= 0) & (yolo['hour'] < 6)]
# the number of tweets in that time period
#len(test)

# compile ALL the frequencies
d = {'csforall': csforall['period'].value_counts(), 
     'equality': equality['period'].value_counts(), 
     'stem': stem['period'].value_counts(),
     'yolo': yolo['period'].value_counts()}

# put the frequencies into a dataframe, fill all nulls with 0
frequencies = pd.DataFrame(data=d).fillna(0)


# In[16]:


#frequencies


# In[17]:


chunk1 = frequencies.loc[range(27000,27060)].dropna()
chunk2 = frequencies.loc[range(27060,27120)].dropna()
chunk3 = frequencies.loc[range(27120,27180)].dropna()
chunk4 = frequencies.loc[range(27180,27240)].dropna()
chunk5 = frequencies.loc[range(28000,28060)].dropna()
chunk6 = frequencies.loc[range(28060,28120)].dropna()
chunk7 = frequencies.loc[range(28120,28180)].dropna()
chunk8 = frequencies.loc[range(28180,28240)].dropna()

chunks = [chunk1, chunk2, chunk3, chunk4, chunk5, chunk6, chunk7, chunk8]


# In[21]:


for chunk in chunks:
    number = 1
    checklist = []
    fig = plt.figure(figsize=(12,10))
    fig.subplots_adjust(wspace=0.25, hspace=0.7, left=0.125, right=0.9, top=0.9, bottom=0.1)
    #title = ('Frequencies in time chunk number ', number)
    #fig.suptitle(title, fontsize=16)
    for hashtag in chunk:
        checklist.append(hashtag)
        for othertag in chunk:
            if othertag not in checklist:
                ax1 = fig.add_subplot(3,2,number)
                ax1.scatter(chunk.index, chunk[hashtag], color="blue", marker="o", label = hashtag, alpha = .4)
                ax1.scatter(chunk.index, chunk[othertag], c='r', marker="s", label= othertag, alpha = .4)
                plt.legend(loc='upper left');
                ax1.set_xlabel('time')
                ax1.set_ylabel('frequency')
                number += 1
    print('')
    plt.show()


# In[ ]:




