
##Stochastic Variational Inference for Latent Dirichlet Allocation

>>> LDA Example SVILDA in themes from research papers abstracts from authors of inputed department

Code structure from the OnlineVB code provided by Matthew D. Hoffman (mdhoffma@cs.princeton.edu) and the algorithm is as described in Hoffman's paper below

Based on the following papers:
- [Latent Dirichlet Allocation](https://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf) by David M. Blei, Andrew Y. Ng and Michael I. Jordan
- [Stochastic Variational Inference](http://www.columbia.edu/~jwp2128/Papers/HoffmanBleiWangPaisley2013.pdf) by Matthew D. Hoffman, David M. Blei, Chong Wang and John Paisley

scrapingBS.py (short list): select department, get name of Professors, get papers in arcvix. (abstract_list.csv)
or
facultymen.py (long list): select department, get name of Professors, get papers in arcvix. (abstract_list.csv)
Themes_LDA.py: from papers, pre-proccess database and run LDA.
- A file [dictionary.csv] containing vocabular (1 word per line only once)
- A file [doclist.txt] containing the list of documents in the directory that you want to sample from (file paths)
- RUN LDA=SVILDA(...)

###How to Use
See 'Help' using
```python stochastic_lda.py -h```


