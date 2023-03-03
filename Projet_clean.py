#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Import packages
from bs4 import BeautifulSoup
import urllib3
import re
import time
from collections import defaultdict
import numpy as np
import tqdm


# In[2]:


##Define URL
urlpage = 'https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/'
urlpage


# In[3]:


##Define Function to get the html code
def get_page(urlpage, element ,html_class):

    # Get page in html
    req = urllib3.PoolManager()
    res = req.request('GET', urlpage)
    soup = BeautifulSoup(res.data, 'html.parser')
    
    # Return elements that matched the html class in a list
    content = soup.find_all(element ,class_= html_class)
    
    return content 


# In[9]:


#Sort html code by theater
contentCine = get_page(urlpage, 'a', 'jCinemaLink')
contentCine


# In[11]:


liste_cinemas = re.findall('">(.*?)</a>', str(contentCine))
liste_cinemas


# In[36]:


contentCine_sub = re.sub('href="', 'https://www.linternaute.com', str(contentCine))
contentCine_sub


# In[38]:


liste_Links = re.findall('jCinemaLink" (.*?)/">',str(contentCine_sub))
liste_Links


# In[10]:


#Sort html code by date
contentDate = get_page(urlpage, 'label', 'jCinemaCalendarLabel')
contentDate


# In[12]:


liste_dates = re.findall('data-date="(.*?)"',str(contentDate))
liste_dates


# In[39]:


#Re-arrange the date format
liste_dates_clean = []

for date in liste_dates :
    tmp = date.split('-')
    tmp_clean = '-'.join([tmp[2], tmp[1], tmp[0]])
    liste_dates_clean.append(tmp_clean)
    


# In[40]:


liste_dates_clean


# In[45]:


url_UGC= 'https://www.linternaute.com/cinema/seances/cinema/608/ugc-cin-cit-strasbourg'
url_Vox= 'https://www.linternaute.com/cinema/seances/cinema/425/cin-vox'


# In[46]:


#Define function to get the movies for a specific Theater
def get_movies (url) :
    contentFilm = get_page (url, 'a', 'movie_title')
    
    liste_films = re.findall('">(.*?)</a',str(contentFilm))
    
    return liste_films
    


# In[47]:


get_movies (url_UGC)


# In[ ]:




