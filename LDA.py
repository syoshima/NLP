# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:04:16 2019

@author: Samy Abud Yoshima
"""

class SVILDA():
def init(self, vocab, K, D, alpha, eta, tau, kappa, docs, iterations):
self ._vocab = vocab
self ._V = len(vocab)
self ._K= K
self ._D = D
self ._alpha = alpha
self ._eta = eta
self ._tau = tau
self ._kappa = kappa
self ._lambda = 1* n.random.gamma(100., 1./100., (self._K, self._V))
self ._Elogbeta = dirichlet_expectation(self._lambda)
self ._expElogbeta = n.exp(self._Elogbeta)
self ._docs = docs
self.ct = 0
self._iterations = iterations

def dirichlet_expectation(alpha):
'''see onlineldavb.py by Matthew Hoffman'''
    if (len(alpha.shape) == 1):
        return (psi(alpha) - psi(n.sum(alpha)))
        return (psi(alpha) - psi(n.sum(alpha, 1))[:, n.newaxis])

def UpdateLocal(self, doc):
    (words, counts) = doc
    newdoc = []
    N_d = sum(counts)
    phi_d = n.zeros((self._K, N_d))
    gamma_d = n.random.gamma(100., 1./100., (self._K))
    Elogtheta_d = dirichlet_expectation(gamma_d)
    expElogtheta_d = n.exp(Elogtheta_d)
    for i, item in enumerate(counts):
        for j in range(item):
            newdoc.append(words[i])
            assert len(newdoc) == N_d, "error"
            for i in range(self._iterations):
                for m, word in enumerate(newdoc):
                    phi_d[:, m] = n.multiply(expElogtheta_d, self._expElogbeta[:, word]) + 1e-100
                    phi_d[:, m] = phi_d[:, m]/n.sum(phi_d[:, m])
                    gamma_new = self._alpha + n.sum(phi_d, axis = 1)
                    meanchange = n.mean(abs(gamma_d - gamma_new))
                    if (meanchange < meanchangethresh):
                        break
                    gamma_d = gamma_new
                    Elogtheta_d = dirichlet_expectation(gamma_d)
                    expElogtheta_d = n.exp(Elogtheta_d)
            newdoc = n.asarray(newdoc)
    return phi_d, newdoc, gamma_d

def UpdateGlobal(self, local_param, doc):
    lambda_d = n.zeros((self._K, self._V))
    for k in range(self._K):
        phi_dk = n.zeros(self._V)
        for m, word in enumerate(doc):
            phi_dk[word] += phi_d[k][m]
            lambda_d[k] = self._eta + self._D * phi_dk
            rho = (self.ct + self._tau) **(-self._kappa)
            self._lambda = (1-rho) * self._lambda + rho * lambda_d
            self._Elogbeta = dirichlet_expectation(self._lambda)
            self._expElogbeta = n.exp(self._Elogbeta)

def runSVI(self):
    for i in range(self._iterations):
    randint = random.randint(0, self._D-1)
    print "ITERATION", i, " running document number ", randint doc =
    parseDocument(self._docs[randint],self._vocab) phi_doc, newdoc, gamma_d =
    self.updateLocal(doc) self.updateGlobal(phi_doc, newdoc)
    self.ct += 1

#The integrated parseDocument function here is as
def parseDocument(doc, vocab): wordslist = list() countslist = list()
    doc = doc.lower()
    tokens = wordpunct_tokenize(doc)
    for word in tokens:
        if word in vocab:
            wordtk = vocab[word]
        if wordtk not in dictionary:
            dictionary[wordtk] = 1
        else: dictionary[wordtk] += 1
    wordslist.append(dictionary.keys())
    countslist.append(dictionary.values())
    return (wordslist[0], countslist[0])