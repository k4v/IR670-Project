__author__ = 'Nikhil'

import scrapy_reader
import get_keywords
import types
from scipy.cluster.vq import vq, kmeans2, whiten
from numpy import *

tokenList = []
vectorList = []
profileVector = []
profileList = scrapy_reader.profile_dump

for profile in profileList.itervalues():
    tokenList.extend([x.lower() for x in profile['skills']])
    if len(profile['experience']) != 0:
        exp = profile['experience'][0]
    if type(exp.desc) is not types.NoneType:
        descTokens = get_keywords.get_keywords(exp.desc)
        tokenList.extend(descTokens)
tokenS = set(tokenList)
tokenList = list(tokenS)

'''
Forming token vectors and profiling of users
'''

for profile in profileList.itervalues():
    tokens = []
    tokens.extend([x.lower() for x in profile['skills']])
    if len(profile['experience']) != 0:
        exp = profile['experience'][0]
    if type(exp.desc) is not types.NoneType:
        descTokens = get_keywords.get_keywords(exp.desc)
        tokens.extend(descTokens)
    profileVector.append([exp.company.lower(), exp.postitle.lower()])
    tokenV = [0] * len(tokenList)
    j = 0
    for t in tokenList:
        if t in tokens:
            tokenV[j] = 1
    vectorList.append(tokenV)

print vectorList
print profileVector
print len(tokenList)
print len(vectorList)

features = array(vectorList)
#whitened = whiten(features)
#centroids, index = kmeans2(data=whitened, k=10)
#print centroids


