__author__ = 'Nikhil'

import cPickle
import get_keywords
from numpy import *

def cluster_score(user_desc, user_skills):
    user_keywords = list(get_keywords.get_keywords(user_desc))
    user_keywords.extend(user_skills)
    cluster_file = 'cluster_dump.txt'
    clusterDump = cPickle.load(open('data/'+cluster_file, 'r'))
    token_lists = clusterDump['tokens']
    token_vector = array([0.0] * len(token_lists))
    n = 0
    '''
    Creating the token vector for the current user
    '''
    for token in token_lists:
        if token in user_keywords:
            token_vector[n] = 1.0
        n += 1
    centroids = clusterDump['centroids']
    titles = clusterDump['job_titles']
    recommendations = clusterDump['recos']
    '''
    Calculating similarity of current user's token vector with each
    of the centroids using Euclidean distance between the vectors.
    '''
    minV = centroids[0] - token_vector
    minMag = sqrt(minV.dot(minV))
    cluster_value = 0
    for i in range(1, len(centroids)):
        diff = centroids[i] - token_vector
        mag = sqrt(diff.dot(diff))
        if mag < minMag:
            minMag = mag
            cluster_value = i
    Result = recommendations[cluster_value], titles[cluster_value]
    return Result

'''
Code for testing above function
================================
'''
'''
user_desc1 = "hello my name is Nikhil, working in Java, python  etc"
user_skillst = ['Java', 'C', 'Python', 'C++']
x, y = cluster_score(user_desc1, user_skillst)
print x
print y
'''