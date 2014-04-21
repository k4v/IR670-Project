__author__ = 'Nikhil'

import scrapy_reader
import get_keywords
import Pycluster
import types
from scipy.cluster.vq import vq, kmeans2, whiten
from numpy import *

k = 10  # k-means no: of clusters
tokenList = []
vectorList = []
profileVector = []
profileList = scrapy_reader.profile_dump

i=0
for profile in profileList.itervalues():
    i += 1
    tokenList.extend([x.lower() for x in profile['skills']])
    if len(profile['experience']) != 0:
        exp = profile['experience'][0]
        if type(exp.desc) is not types.NoneType:
            descTokens = get_keywords.get_keywords(exp.desc)
            tokenList.extend(descTokens)
    if i == 3:
        break
tokenS = set(tokenList)
tokenList = list(tokenS)

'''
Forming token vectors and profiling of users
'''
i = 0
for profile in profileList.itervalues():
    i += 1
    tokens = []
    tokens.extend([x.lower() for x in profile['skills']])
    if len(profile['experience']) != 0:
        exp = profile['experience'][0]
        if type(exp.desc) is not types.NoneType:
            descTokens = get_keywords.get_keywords(exp.desc)
            tokens.extend(descTokens)
    tempTokens = set(tokens)
    tokens = list(tempTokens)
    #print tokens
    profileVector.append([exp.company.lower(), exp.postitle.lower()])
    tokenV = [0.0] * len(tokenList)
    j = 0
    for t in tokenList:
        if t in tokens:
            tokenV[j] = 1.0
        j += 1
    vectorList.append(tokenV)
    #print tokenV
    if i == 3:
        break

print vectorList
print profileVector
print len(tokenList)
print len(vectorList)

features = array(vectorList)
#whitened = whiten(features)

labels, error, nfound = Pycluster.kcluster(features, 2)
centroids = vstack([features[labels == i].mean(0) for i in range(labels.max() + 1)])


print labels
print centroids


