#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from html.parser import HTMLParser
from urllib import parse
import scrapy
import json
import numpy as np
import pandas as pd
import codecs
import datetime
from lxml import html
from bs4 import BeautifulSoup
import requests

class My_Parkinson_WebCrawler:
    
    def __init__(self):
        self.data_all_forums = pd.DataFrame()
        self.topics= []
        self.links=[]
        self.discussions =[]
        self.voices = []
        self.reply= []
    
    def __init__(self,starting_url,depth):
        self.starting_url = starting_url
        self.depth = depth
        self.data_all_forums = pd.DataFrame()
        
    def __init__(self,starting_url,depth,file_path):
        self.starting_url = starting_url
        self.depth = depth
        self.file_path = file_path
        self.data_all_forums = pd.DataFrame()
        
        
    def extractor_by_forum(self):
        
        titles= []
        links=[]
        descriptions=[]
        topics_count= []
        reply= []
        response = requests.get(self.starting_url)
        soup = BeautifulSoup(response.text)
        metas = soup.findAll('ul',id = lambda value: value and value.startswith("bbp-forum"))
        try:
            titles=map( lambda meta:meta.findAll("a",{"class":"bbp-forum-title"})[0].contents,metas)
            links=map( lambda meta:meta.findAll("a",{"class":"bbp-forum-title"})[0]['href'],metas)
            descriptions =map( lambda meta: meta.findAll("div",{"class":"bbp-forum-content"})[0].contents[1],metas)
            topics_count = map( lambda meta:meta.findAll('li',{"class":"bbp-forum-topic-count"})[0].contents,metas)
            reply= map( lambda meta:meta.findAll('li',{"class":"bbp-forum-reply-count"})[0].contents,metas)


        except:
            print(' A troublee is gonna up ')

        data =  {"titles":titles,"links":links, "descriptions":descriptions,"topics_count":topics_count,"replies":reply}
        forums = pd.DataFrame(data)
        return forums

    # to determine how many pages in the pagination of each forum === Depth of each forum
    def page_count(self,soup_page_url):
        response = requests.get(soup_page_url)
        soup = BeautifulSoup(response.text)
        metas = soup.findAll('a',{"class":"page-numbers"})
        res=[]
        #self.res= res
        if len(metas)!=0:
            res = [str(meta.contents[0])for meta in metas]
            res = [int(i) for i in res if i.isdigit()]
            res = res if len(res)!=0 else 1
            return max(res)
        else:
            return 1

    def extractor_comments(self,link):
        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        metas = soup.find_all('meta')
        bbp_reply = soup.findAll("div",{"class":"bbp-reply-content"})
        comments =[]

        for meta in bbp_reply:
            result= ''.join(meta.findAll(text=True))
            result = str(result).replace('\\n',"").replace('\\t',"")
            comments.append([result])
      
        return comments
    
    def meta_comments(self,link):
        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        metas = soup.find_all('meta')
        bbp_reply = soup.findAll("div",{"class":"bbp-reply-content"})
        comments =[]

        for meta in bbp_reply:
            result= ''.join(meta.findAll(text=True))
            comments.append(result)
        
        #attrss
        #if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        res =[meta.attrs for meta in metas]
        properties = ['og:title','og:locale','og:description','twitter:discription']
        tag = ['property','name']
        extracted_data = []
        data={}

        for i in range(len(res)):
            for item in tag:
                if np.any(item in res[i] and res[i][item] in properties):
                    data[res[i][item]] = res[i]['content']
        extracted_data.append(data)
        data['comments_reply'] = comments
        return pd.DataFrame(extracted_data)
    
    def show(self):
        print(self.data_all_forums)

    def extractor_by_topic(self,soup_page_url):

        
        response = requests.get(soup_page_url)
        soup = BeautifulSoup(response.text)
        metas = soup.findAll('ul',id = lambda value: value and value.startswith("bbp-topic"))
        try:
            topics=map( lambda meta:meta.find('a',{"class":"bbp-topic-permalink"}).contents[0],metas)
            links=map( lambda meta:meta.a['href'],metas)
            voices = map( lambda meta:meta.findAll('li',{"class":"bbp-topic-voice-count"})[0].contents,metas)
            reply= map( lambda meta:meta.findAll('li',{"class":"bbp-topic-reply-count"})[0].contents,metas)
            comments = map (lambda link : self.extractor_comments(link), map( lambda meta:meta.a['href'],metas))
        except:
            print(' A troublee is gonna up ')
            
        data =  {"topics":topics,"links":links,"voices":voices,"replies":reply,"comments":comments}
        topics = pd.DataFrame(data)
        #comments = {"comments":comments}
        return topics
    
    def extractor_by_tag(soup_page_url):

        topics= []
        links=[]
        discussions =[]
        voices = []
        reply= []
        response = requests.get(soup_page_url)
        soup = BeautifulSoup(response.text)
        metas = soup.findAll('ul',id = lambda value: value and value.startswith("bbp-topic"))
        try:
            topics=map( lambda meta:meta.find('a',{"class":"bbp-topic-permalink"}).contents[0],metas)
            links=map( lambda meta:meta.a['href'],metas)
            discussions =map( lambda meta:meta.find('span',{"class":"bbp-topic-started-in"}).a['href'],metas)
            voices = map( lambda meta:meta.findAll('li',{"class":"bbp-topic-voice-count"})[0].contents,metas)
            reply= map( lambda meta:meta.findAll('li',{"class":"bbp-topic-reply-count"})[0].contents,metas)



        except:
            print(' A trouble is gonna up ')
        comments = map (lambda link : str(extractor_comments(link)).split(','), links)
        data =  {"topics":topics,"links":links, "discussions":discussions,"voices":voices,"replies":reply}
        topics = pd.DataFrame(data)
        return topics
    def collect_from_forums(self,links):
        for link in links:
            self.data_all_forums = self.data_all_forums.append(self.extractor_by_topic(link),ignore_index=True)
            if self.page_count(link)!=1:
                self.data_all_forums = self.data_all_forums.append(self.pagination_scraping(link,self.page_count(link)))
        return self.data_all_forums

    #paginate all pages in forums link
    def pagination_scraping(self,link_basic,page_numbers):
        data = self.extractor_by_topic(link_basic)
        for i in range(1,page_numbers):
            link = link_basic+"page/"+str(i)+"/"
            try:
                data = data.append(self.extractor_by_topic(link),ignore_index=True)

            except:
                print('doesnt append')
            #print(len(data))
        return data

    def to_write_csv(self,file_path):
        self.data_all_forums.to_csv(file_path)



class Main:
    print("Welcome.\n\n")
    forum_link = "https://parkinsonsnewstoday.com/forums/forums/"
    file_path ="Parkinson_data.csv"
    my_crawler = My_Parkinson_WebCrawler(forum_link,1,file_path)
    my_crawler.show()
    forums = my_crawler.extractor_by_forum()
    my_crawler.collect_from_forums(forums.links)
    my_crawler.page_count(forum_link)
#     my_crawler.show()
    my_crawler.to_write_csv(file_path)
