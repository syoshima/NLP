# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:26:47 2019

@author: Samy Abud Yoshima
From Julio Villane
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# https://stat.mit.edu/people_categories/core/
# $.map($("div.copy > h3 > a"), $.text);

baseUrl = 'https://arxiv.org'
# author's list extracted from 'https://www.eecs.mit.edu/people/faculty-advisors'
#authors = ['Hal Abelson', 'Elfar Adalsteinsson', 'Anant Agarwal', 'Akintunde Akinwande', 'Mohammad Alizadeh', 'Saman Amarasinghe', 'Dimitri Antoniadis', ' Arvind', 'Arthur Baggeroer', 'Hari Balakrishnan', 'Marc A. Baldo', 'Regina Barzilay', 'Adam Belay', 'Bonnie A. Berger', 'Karl Berggren', 'Tim Berners-Lee', 'Dimitri Bertsekas', 'Robert Berwick', 'Sangeeta Bhatia', 'Duane Boning', 'Louis Braida', 'Guy Bresler', 'Tamara Broderick', 'Rodney Brooks', 'Vladimir Bulovic', 'Michael Carbin', 'Vincent Chan', 'Anantha Chandrakasan', 'Adam Chlipala', 'Isaac Chuang', 'David Clark', 'Fernando Corbato', 'Munther Dahleh', 'Luca Daniel', 'Constantinos Daskalakis', 'Randall Davis', 'Jesus del Alamo', 'Erik Demaine', 'Jack Dennis', 'Srini Devadas', 'Fredo Durand', 'Joel Emer', 'Dirk R. Englund', 'Clifton Fonstad', 'David Forney', 'Dennis Freeman', 'William Freeman', 'James Fujimoto', 'Robert Gallager', 'Manya Ghobadi', 'David Gifford', 'Shafi Goldwasser', 'Polina Golland', 'Martha Gray', 'W. Eric L. Grimson', 'Alan Grodzinsky', 'John Guttag', 'Peter Hagelstein', 'Song Han', 'Jongyoon Han', 'Ruonan Han', 'Thomas Heldt', 'Berthold Horn', 'Qing Hu', 'Piotr Indyk', 'Erich Ippen', 'Phillip Isola', 'Tommi Jaakkola', 'Daniel Jackson', 'Patrick Jaillet', 'Stefanie Jegelka', 'M. Frans Kaashoek', 'Leslie Kaelbling', 'David Karger', 'John Kassakian', 'Dina Katabi', 'Manolis Kellis', 'James Kirtley, Jr.', 'Leslie Kolodziejski', 'Jing Kong', 'Tim Kraska ', 'Butler Lampson', 'Jeffrey Lang', 'Hae-Seung Lee', 'Steven Leeb', 'Charles Leiserson', 'Jae Lim', 'Barbara Liskov', 'Luqiao Liu', 'Andrew W. Lo', 'Tomas Lozano-Perez', 'Timothy Lu', 'Nancy Lynch', 'Samuel Madden', 'Aleksander Madry', 'Thomas Magnanti', 'Roger Mark', 'Wojciech Matusik', 'Muriel Medard', 'Alexandre Megretski', 'Albert Meyer', 'Silvio Micali', 'Rob Miller', 'Sanjoy Mitter', 'Robert Morris', 'Joel Moses', 'Stefanie Mueller', 'Farnaz Niroui', 'Alan Oppenheim', 'Terry Orlando', 'Asuman Ozdaglar', 'Tomas Palacios', 'Pablo Parrilo', 'Li-Shiuan Peh', 'Paul Penfield, Jr.', 'David Perreault', 'Yury Polyanskiy', 'Rajeev Ram', 'L. Rafael Reif', 'Martin Rinard', 'Ronald Rivest', 'Ronitt Rubinfeld', 'Jennifer L.M. Rupp', 'Daniela Rus', 'Daniel Sanchez', 'Arvind Satyanarayan ', 'Joel Schindall', 'Martin A. Schmidt', 'Devavrat Shah', 'Jeffrey Shapiro', 'Nir Shavit', 'Max Shulaker', 'Julian Shun', 'Henry Smith', 'Charles Sodini', 'Armando Solar-Lezama', 'Justin Solomon', 'David Sontag', 'Suvrit Sra', 'Michael Stonebraker', 'Collin Stultz', 'Gerald Sussman', 'Vivienne Sze', 'Peter Szolovits', 'Russell Tedrake', 'Christopher Terman', 'Bruce Tidor', 'Antonio Torralba', 'John Tsitsiklis', 'Caroline Uhler', 'Vinod Vaikuntanathan', 'George Verghese', 'Joel Voldman', 'Stephen Ward', 'Cardinal Warde', 'Michael Watts', 'Ron Weiss', 'Jacob White', 'Virginia Williams', 'Ryan Williams', 'Alan Willsky', 'Patrick Winston', 'Gregory Wornell', 'Markus Zahn', 'Nickolai Zeldovich', 'Lizhong Zheng', 'Victor Zue']
Authors = ['Victor Chernozhukov','Stefanie Jegelka','Tamara Broderick','David Gamarnik','Johnathan Kelner','Ankur Moitra','Devavrat Shah','Phillipe Rigollet','Caroline Uhler','Guy Bresler','Kalyan Veeramachaneni']
# caputre from faculty memebers

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