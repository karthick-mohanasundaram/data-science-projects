# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Data Science in python assignment 2
# Part 1. Text Data Scraping (40% of marks)
# Submitted by Karthick Mohanasundaram
# student id: 15200702

import urllib
from bs4 import BeautifulSoup
import requests


response_object = urllib.request.urlopen('http://mlg.ucd.ie/modules/COMP41680/news/index.html')
html_tags = response_object.read()
soup = BeautifulSoup(html_tags)
#finding all href attribute specifies the URL of the page the link goes to
#e.g. from <a href="month-jan.html">January</a>
html_links = soup.find_all('a')


#  retrieving the each month url of article
# e.g http://mlg.ucd.ie/modules/COMP41680/news/month-jan.html
articles_urls_list = []
dns = 'http://mlg.ucd.ie/modules/COMP41680/news/'
for links in html_links:
    
    # get rid of the below links that don't have a hyperlink
    # <a href="">Terms &amp; Conditions</a>
    # <a href="">Privacy Policy</a>
    # <a href="">Cookie Information</a>

    if(links.get('href') != ''):
        articles_urls_list.append(dns+links.get('href'))



# retrieving all the article paths of contained in each months
# e.g article-jan-4425.html
# total 1131 article
article_month_list = []

for temp in articles_urls_list:
    
    response_object = urllib.request.urlopen(temp)
    html_tags = response_object.read()
    soup = BeautifulSoup(html_tags)
    html_links = soup.find_all('a')

    for links in html_links:
        #filtering the hyperlinks whose href is empty and index.html
        if(links.get('href') != '' and links.get('href') != 'index.html'):
            article_months = links.get('href')
            # list of all article paths
            article_month_list.append(article_months)





# building the entire url of each article
# e.g http://mlg.ucd.ie/modules/COMP41680/news/article-jan-3329.html
all_articles_urls_list = []
for suffix in article_month_list:
    all_articles_urls_list.append(dns+suffix) 



# retrieving the content of paragraph tags
article_body = []

for l in all_articles_urls_list:
    article_content = []
    article = requests.get(l)
    soup = BeautifulSoup(article.content, 'html.parser')
    #finds all the paragraph
    paragraph = soup.find_all("p")
    
    for p in paragraph:
        # removing pargaraph tags that has empty content
        if(p.get_text() != ''):
            article_content.append(p.get_text())    
    
    # appending the content of each paragraph tag in all article
    # a list items indicate the paragraph content of one article
    article_body.append(article_content)
        
               
               
# extracting the article's name by removing .html, which is used for identifing flies
article_names = []
for i in article_month_list:
    article_names.append(i[0:len(i)-5])

# writing the  body of article into seperate text file
for name,body in zip(article_names,article_body):
    f = open(str(name)+'.txt','w',encoding = 'utf-8')
    f.write(str(body))
    f.close()