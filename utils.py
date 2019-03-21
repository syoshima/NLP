import sys, csv
from nltk.tokenize import wordpunct_tokenize
from scipy.special import psi
import numpy as n
import matplotlib.pyplot as plt

LISTOFDOCS = "alldocs.txt"

#scrape 
# To run this, you can install BeautifulSoup
# https://pypi.python.org/pypi/beautifulsoup4

# Or download the file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file
#https://arxiv.org/find/(subject)/1/au:+(lastname)_(initial)/0/1/0/all/0/1

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
"""
#url = input('Enter - ')
url = 'https://arxiv.org'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup('a')
for tag in tags:
    # Look at the parts of a tag
    print('TAG:', tag)
    print('URL:', tag.get('href', None))
    print('Contents:',tag.contents) #[0]
    print('Attrs:', tag.attrs)
"""

filenames = []

def get_filenames(filename):
    print("getting filenames")
    if filename == None:
        filename = LISTOFDOCS
        with open(filename, 'r') as f:
            f = f.replace("\r", "")
            docs = f.readlines()
        for doc in docs:
            print(str(doc).split("\n"))
            filenames.append(str(doc).split("\n")[0])

    return filenames


def getfiles(filename):
	print("getting file " + filename)
	f = open(filename, 'r')
	doc = f.read()
	print(doc)
	return doc


def getalldocs(filename = None):
	files = get_filenames(filename)
	docs = []
	for file in files:
		doc = getfiles(file)
		# print doc
		docs.append(doc)
	# print docs
	return docs



def dirichlet_expectation(alpha):
	'''see onlineldavb.py by Blei et al'''
	if (len(alpha.shape) == 1):
		return (psi(alpha) - psi(n.sum(alpha)))
	return (psi(alpha) - psi(n.sum(alpha, 1))[:, n.newaxis])

def beta_expectation(a, b, k):
	mysum = psi(a + b)
	Elog_a = psi(a) - mysum
	Elog_b = psi(b) - mysum
	Elog_beta = n.zeros(k)
	Elog_beta[0] = Elog_a[0]
	# print Elog_beta
	for i in range(1, k):
		Elog_beta[i] = Elog_a[i] + n.sum(Elog_b[0:i])
		# print Elog_beta
	print(Elog_beta)
	return Elog_beta


def parseDocument(doc, vocab):
	wordslist = list()
	countslist = list()
	doc = doc.lower()
	tokens = wordpunct_tokenize(doc)

	dictionary = dict()
	for word in tokens:
		if word in vocab:
			wordtk = vocab[word]
			if wordtk not in dictionary:
				dictionary[wordtk] = 1
			else:
				dictionary[wordtk] += 1

	wordslist.append(dictionary.keys())
	countslist.append(dictionary.values())
	return (wordslist[0], countslist[0])

def getVocab(file):
	'''getting vocab dictionary from a csv file (nostopwords)'''
	vocab = dict()
	with open(file, 'r') as infile:
		reader = csv.reader(infile)
		for index, row in enumerate(reader):
			vocab[row[0]] = index

	return vocab


def plottrace(x, Y, K, n, perp):
	for i in range(K):
		plt.plot(x, Y[i], label = "Topic %i" %(i+1))

	plt.xlabel("Number of Iterations")
	plt.ylabel("Probability of Each topic")
	plt.legend()
	plt.title("Trace plot for topic probabilities")
	plt.savefig("temp/plot_%i_%i_%f.png" %(K, n, perp))

plt.show()
# 
# def calcPerplexity(test_docs):
	


# getalldocs()
