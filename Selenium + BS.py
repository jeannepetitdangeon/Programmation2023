#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Installation de Selenium
pip install selenium


# In[55]:


urlpage = 'https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/'


# In[25]:


##Installation des packages et webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib3
import re
import time
from collections import defaultdict
import numpy as np
import tqdm
import itertools

driver = webdriver.Chrome()

#Launch the webdriver
driver.get('https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/')


# In[26]:


##Define Function to get the html code
def get_page(urlpage, element ,html_class):

    # Get page in html
    req = urllib3.PoolManager()
    res = req.request('GET', urlpage)
    soup = BeautifulSoup(res.data, 'html.parser')
    
    # Return elements that matched the html class in a list
    content = soup.find_all(element ,class_= html_class)
    
    return content 


# In[31]:


##Define function to get the available dates
def get_all_dates():
    
    urlpage = 'https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/'
    #Sort html code by date
    contentDate = get_page(urlpage, 'label', 'jCinemaCalendarLabel')
    
    #get a list with the available dates
    liste_dates = re.findall('data-date="(.*?)"',str(contentDate))

    ##Re-arrange the date format
    liste_dates_clean = []

    for date in liste_dates :
        tmp = date.split('-')
        tmp_clean = '-'.join([tmp[2], tmp[1], tmp[0]])
        liste_dates_clean.append(tmp_clean)
    
    return liste_dates_clean


# In[32]:


dates = get_all_dates()


# In[33]:


def get_Showdays_class() :
    liste_Showdays = []
    
    for date in dates:
        tmp = date.split('-')
        jour = tmp[0]
        Showday = 'jShowDay show-day-'+jour
        liste_Showdays.append(Showday)
    return liste_Showdays


# In[34]:


get_Showdays_class()


# In[51]:


def get_showday_class() :
    liste_Showdays = []
    
    for date in dates:
        tmp = date.split('-')
        jour = tmp[0]
        Showday = 'show-day-'+jour
        liste_Showdays.append(Showday)
    return liste_Showdays


# In[52]:


get_showday_class()


# In[59]:


##Define a function to get VF or VO for a movie
def get_versions():
    
    #set url
    urlpage = 'https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/'
    
    #define the classes for every available day
    showday_list = get_showday_class()
    
    liste_versions = []
    for showday in showday_list:
        content_showDay = get_page (urlpage, 'div', 'showday')
        liste_versions = re.findall('data-diffusion="(.*?)" data',str(content_showDay))

    return liste_versions


# In[60]:


get_versions()


# In[65]:


showday_list = get_showday_class()

for showday in showday_list:
    content_showDay = get_page (urlpage, 'div', 'show-day-07')
    liste_versions = re.findall('data-diffusion="(.*?)" data',str(content_showDay))
liste_versions


# In[27]:


##Define function to get all links for all theaters
def get_all_links():

    # Webpage from which we extract all links
    urlpage = 'https://www.linternaute.com/cinema/seances/ville/35074/strasbourg/'
   
    # Use get_page function to extract a list with all theaters
    contentCine = get_page(urlpage, 'a', 'jCinemaLink')
    liste_cinemas = re.findall('">(.*?)</a>', str(contentCine))
    
    #Sub the string to get working links
    contentCine_sub = re.sub('href="', 'https://www.linternaute.com', str(contentCine))
    liste_Links = re.findall('jCinemaLink" (.*?)/">',str(contentCine_sub))
    
    # Create an empty dict
    names_links = {}
    
    # Iterate over each link
    for (name, link) in zip(liste_cinemas, liste_Links):
            names_links.update({name : link})
            
    return names_links


# In[28]:


links = get_all_links()
links


# In[29]:


##Define function to get all movies from all Theaters
def get_all_movies () :
    links
    
    #create empty dict
    movies_in_theaters={}
    
    #Fill it with theater names
    for name in tqdm.tqdm(links):
        contentFilm = get_page (links[name], 
                                'a', 'movie_title')
        for content in contentFilm:
            liste_films = re.findall('">(.*?)</a',str(contentFilm))
            movies_in_theaters.update({name:liste_films})
    
    return movies_in_theaters


# In[30]:


get_all_movies()


# In[18]:


##Define a function for scraping by class name
def get_list_by_class(class_name):
    #scrap content by matching class
    contents = driver.find_elements(By.CLASS_NAME, class_name)
    
    #Create an empty list
    list_content =[]
    
    for i in range(len(contents)):
        content = contents[i].text
        list_content.append(content)

    return list_content


# In[19]:


##Define a function for scraping by class name
def get_list_by_xpath(xpath):
    #scrap content by matching class
    contents = driver.find_elements(By.XPATH, xpath)
    
    #Create an empty list
    list_content =[]
    
    for i in range(len(contents)):
        content = contents[i].text
        list_content.append(content)

    return list_content


# In[66]:


liste_horaires = get_list_by_class('showtimes')


# In[68]:


def get_all_versions_all_horaires():
    #create empty dict
    versions_horaires={}
    
    #Fill it with versions VO/VF
    for version in liste_versions: 
        
        for horaires in liste_horaires:
            versions_horaires.update({version:horaires})
    
    return versions_horaires


# In[70]:


get_all_versions_all_horaires()
    


# In[ ]:




