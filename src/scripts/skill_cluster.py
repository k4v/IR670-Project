__author__ = 'Nikhil'

import scrapy_reader
import get_keywords
import Pycluster
import types
from numpy import *
from collections import defaultdict, Counter
import operator as op
import cPickle

kc = 8  # k-means no: of clusters
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
    tempTokens = set(tokens)
    tokens = list(tempTokens)
    tokenV = [0.0] * len(tokenList)
    j = 0
    for t in tokenList:
        if t in tokens:
            tokenV[j] = 1.0
        j += 1
    vectorList.append(tokenV)

'''
Logging intermediate results
'''
print vectorList
print profileVector
print len(tokenList)
print len(vectorList)

features = array(vectorList)

labels, error, nfound = Pycluster.kcluster(features, kc)
centroids = vstack([features[labels == i].mean(0) for i in range(labels.max() + 1)])
s1Vector = defaultdict(list)
s2Vector = defaultdict(list)
Result1 = []
Result2 = []
for l in range(0, len(labels)):
    s2Vector[labels[l]].append(profileVector[l][1])
    company = profileVector[l][0]
    for z in range(0, len(labels)):
        if profileVector[z][0] in profileVector[l][0]:
            if len(profileVector[z][0]) < len(company):
                company = profileVector[z][0]
    s1Vector[labels[l]].append(company)

for l in range(0, kc):
    temp = dict(Counter(s2Vector[l]))
    result = sorted(temp.iteritems(), key=op.itemgetter(1), reverse=True)
    x, y = result[0]
    Result2.append(x)
    temp2 = dict(Counter(s1Vector[l]))
    result2 = sorted(temp2.iteritems(), key=op.itemgetter(1), reverse=True)
    compL = []
    for i in range(5):
        if i == len(result2):
            break
        x, y = result2[i]
        compL.append(x)
    Result1.append(compL)

'''
Logging clustering results
'''
print labels
print centroids #(Type - ndarray)
print Result2 # (Type - list) List of position(job title) for each cluster
print Result1 # (Type- list of list) List of recommended companies for each cluster

cluster_dump = {'tokens': tokenList, 'centroids': centroids, 'recos': Result1, 'job_titles': Result2}
cPickle.dump(cluster_dump, open('data/cluster_dump.txt', 'w'))
