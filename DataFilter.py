#!/usr/bin/env python
# coding: utf-8

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
csforall["day"] = pd.to_numeric(new[2])
csforall["time"] = new[3]

new = equality["time created"].str.split(" ", expand = True) 
equality["day"] = pd.to_numeric(new[2])
equality["time"] = new[3]

new = stem["time created"].str.split(" ", expand = True) 
stem["day"] = pd.to_numeric(new[2])
stem["time"] = new[3]

new = yolo["time created"].str.split(" ", expand = True) 
yolo["day"] = pd.to_numeric(new[2])
yolo["time"] = new[3]


# In[4]:


# split tweet time into a more useable format, (separate time column into hours, min, sec; save hours)

new = csforall["time"].str.split(":", expand = True) 
csforall["hour"] = pd.to_numeric(new[0])

new = equality["time"].str.split(":", expand = True) 
equality["hour"] = pd.to_numeric(new[0])

new = stem["time"].str.split(":", expand = True) 
stem["hour"] = pd.to_numeric(new[0])

new = yolo["time"].str.split(":", expand = True) 
yolo["hour"] = pd.to_numeric(new[0])


# In[5]:


# drop unneccesary info (only day and hour of publishing remain)

csforall.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time'],inplace=True,axis=1) 
equality.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time'],inplace=True,axis=1) 
stem.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time'],inplace=True,axis=1) 
yolo.drop(['tweet ID','username','user followers', 'retweets', 'favorites', "time created", 'time'],inplace=True,axis=1) 


# In[10]:


# pull all yolo tweets from the first six hours of Feb 27th

test = yolo.loc[(yolo['day'] == 27) & (yolo['hour'] <= 6)]
test.shape


# In[ ]:




