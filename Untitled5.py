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
def get_page(urlpage,element ,html_class):

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


# In[10]:


#Sort html code by date
contentDate = get_page(urlpage, 'label', 'jCinemaCalendarLabel')
contentDate


# In[12]:


liste_dates = re.findall('data-date="(.*?)"',str(contentDate))
liste_dates


# In[ ]:




