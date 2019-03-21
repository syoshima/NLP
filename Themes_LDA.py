# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 14:03:55 2019
@author: Samy Abud Yoshima
"""
import sys, re, time, string, random, argparse
import pandas as pd
import csv
import os
import io
#io to acces database folder um contant path  
import nltk
from nltk.tokenize import RegexpTokenizer, wordpunct_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer 
from collections import Counter
from utils import *
from stochastic_lda import *
import matplotlib.pyplot as plt
nltk.download('stopwords')
nltk.download('wordnet')

# GOAL: Discover ‘topics’ in a large set of documents
ab_list = pd.read_csv("abstract_list.csv", encoding='utf-8')
fieldnames = ['author', 'shortname', 'id', 'url', 'abstract']
ab_list = ab_list['abstract'].tolist()      
ab_list = [s.replace('\\n',' ') for s in ab_list]
ab_list = pd.DataFrame({'abstract':ab_list})

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
createFolder('./texts/') # check if folder exits, if so rewrite 
#C:\Users\Samy Abud Yoshima\Anaconda3\Library\courses\MIT XPRO\DataScience+BigData\Module 1 - Clustering\CaseSt 1.1.2\texts

# Database pre-procesing
# REGEX
tokenizer = RegexpTokenizer(r'\w+d+')
# Define stop words from augumented NLTK stopwords list
stop_words = set(stopwords.words('english'))
new_stopwords = ['11ad','1d','2d','3d','5d','We',':','und','based','build','built','method','cond','nd','need','prod','used','present','abstract','A','nin','""','b','nthat','nto','use']
stopset = (stop_words.union(new_stopwords))
with open('dictionary1.csv', mode='w') as csvFile:
    fdnames = ['words']
    writer = csv.DictWriter(csvFile, fieldnames=fdnames)
    writer.writeheader()
    with open('alldocs.txt', mode='w') as docs:
        for i in range(1,len(ab_list)):
            words = ab_list.iat[int(i),0].lower()        
            # count words in words,copiar count to new line in txt file
            suma = len(words.split())
            # open txt file, copy words to this txt file,
            with io.open("C:\\Users\\Samy Abud Yoshima\\Anaconda3\\Library\\courses\\MIT XPRO\\DataScience+BigData\\Module 1 - Clustering\\CaseSt 1.1.2\\texts\\file_" + str(i) + ".txt", 'w', encoding='utf-8') as f:
                f.write(words)
                f.write('\n')
                f.write(str(suma))
            # copy file path to alldocs.txt
            docs.write("C:\\Users\\Samy Abud Yoshima\\Anaconda3\\Library\\courses\\MIT XPRO\\DataScience+BigData\\Module 1 - Clustering\\CaseSt 1.1.2\\texts\\file_" + str(i) + ".txt")
            docs.write("\n")
            word = tokenizer.tokenize(words)
            # Lexicon normalization and stemmization
            lem = WordNetLemmatizer()
            stem = PorterStemmer()
            #word = lem.lemmatize(word, "v")
            #word = stem.stem(word)
            tokens = [w for w in word if not w in stopset]
            for line in tokens:
                line = '\n'.join(str(line) for line in tokens)
                writer.writerow({'words': line})          
        csvFile.close()
# Funções de counter
dic = pd.read_csv("dictionary1.csv", sep='\rn',encoding='utf-8',engine='python')    
dic = dic['words'].tolist()      
dic = [s.replace('"','') for s in dic]
cnt = Counter(dic)
fd = nltk.FreqDist(dic)
fdk = fd.keys() # show the keys in the data object
fdv = fd.values() # show the values in the data object
fdi = fd.items() # show everything
#Frequency plots
fd.plot(40,cumulative=False) # generate a chart of the x most frequent words
fd.hapaxes()
#Get word lengths And do FreqDist
lengths = [len(w) for w in dic]
fd = nltk.FreqDist(lengths)

# Create final dictionary.csv file
# Remove frewunent words that appear less than 10 times
df = pd.DataFrame.from_dict(cnt, orient='index').reset_index()
df = df.rename(columns={'index':'word', 0:'cnt'})
#df1 = df.sort_values(by=['cnt'],axis=0)
df['cnt'] = df['cnt'].astype(int)
df2 = df[(df.cnt > 10)&(df.cnt <5000)]
df3 = df2[['word']]
df3.to_csv("dictionary.csv", sep='\n', index=False)

#Frequency plots
df4 = df2.sort_values(by=['cnt'],axis=0,ascending=False)
df4 = df4.iloc[1:40]
fig,ax = plt.subplots()
plt.plot(df4['word'],df4['cnt'])
for tick in ax.get_xticklabels():
    tick.set_rotation(90)
ax.grid()
plt.show()

# Run LDA
v ='dictionary.csv'
K=10
D = len(ab_list)
A = 0.2
E = 0.2
T = 0.7
ka = 1024
docs = 'alldocs.txt'
i = 1000
LDA = SVILDA(vocab=v, K=K,D=D, alpha=A, eta=E, tau=T, kappa=ka, docs=docs, iterations=i, parsed=False)
print(LDA)
"""
λ: what we want in the end (the posterior distribution for the topics for each word
vocab: this is the overall vocabulary we will have in the docs
K: this is the number of topics we want to get in the end
D: this is the total number of documents
α: parameter for per-document topic distribution
η: parameter for per-topic vocab distribution
τ: delay that down weights early iterations
κ: forgetting rate, controls how quickly old information is forgotten; the larger the value, the slower it is.
max:iterations: the number of maximum iterations
"""
# Plot graphs of results
# 1) Most popular words in each topic k = 5 (PIE GRAPH topic 0-5)
# Take out each topic entry, rank the words from highest probability to lower probabilities.
# Obtain list of words for any topic in Figure 1.
 
# 2) bar graph with Department (lab groups) research interests for different number of K   