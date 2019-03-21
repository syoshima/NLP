# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:46:19 2019
@author: Samy Abud Yoshima
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import numpy as np
import re
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = input('Enter - ')
#if len(url) < 1:
#position = input("Enter position: ")
#count = input("Enter count: ")
# Find Faculty List
url     = 'https://www.eecs.mit.edu/people/faculty-advisors'
html    = urlopen(url, context=ctx).read()
soup    = BeautifulSoup(html, 'html.parser')
tags    = soup(class_="field-content card-title")
Authors = ['Victor Chernozhukov','Stefanie Jegelka','Tamara Broderick','David Gamarnik','Johnathan Kelner','Ankur Moitra','Devavrat Shah','Phillipe Rigollet','Caroline Uhler','Guy Bresler','Kalyan Veeramachaneni']
for tag in tags:
    tag = (tag)
    tag2 = tag.find_next('a')
    tag1 = re.findall('>(.*)<br/>',str(tag2))
    tag1 = str(tag1)
    for char in tag1:
        if char in "´[]'":
            tag1 = tag1.replace(char,'')
        if char in "ÒòÓóöÖõÕÔô":
            tag1 = tag1.replace(char,'o')
        if char in "àÀÁáÄäÃãÂâ":
            tag1 = tag1.replace(char,'a')
        if char in "éÉèÈêÊëË":
            tag1 = tag1.replace(char,'e')
        if char in "üÜÚùúÚÛû":
            tag1 = tag1.replace(char,'u')
          if char in "ïÏìÌÍîÎ":
            tag1 = tag1.replace(char,'i')    
    if author is not in Authors:
        Authors.append(tag1)
Authors = [x for x in Authors if x != ""]
print('Number of Authors: ',np.size(Authors))

# Find list of papers
baseUrl = 'https://arxiv.org'
# open csv for saving data
with open('abstract_list.csv', mode='w') as csvFile:
    fieldnames = ['author', 'shortname', 'id', 'url', 'abstract']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()

    # for each author we search his paper abstract list
    for author in Authors:
        print('Processing papers abstracts from author: ' + author)
        split = author.split(" ")
        if len(split) != 2:
            continue
        searchName = split[1] + "_" + split[0]

        page = urlopen(baseUrl + "/find/all/1/au:+" + searchName + "/0/1/0/all/0/1?per_page=100")
        soup = BeautifulSoup(page,features='html.parser')

        # for each abstract link we extract the text
        for paper in soup('a', title='Abstract'):
            id = paper.contents[0]
            abstractUrl = baseUrl + paper['href']
            abstractPage = urlopen(abstractUrl)
            abstract = BeautifulSoup(abstractPage,features='html.parser')
            text = abstract.find('blockquote', {'class': 'abstract'}).text.encode('utf-8').strip()

            # and save the information as a new csv line
            writer.writerow({'author': author, 'shortname': searchName, 'id': id, 'url': abstractUrl, 'abstract': text})

print('-- The end')




