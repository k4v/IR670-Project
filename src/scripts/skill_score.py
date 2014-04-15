__author__ = 'Nikhil'

import scrapy_reader
from collections import defaultdict
import numpy as nm

profileList = scrapy_reader.item
skillsVector = {}
skillsVector = defaultdict(lambda: 0, skillsVector)
'''
skillsUser need to read from the UI
hardcoding for the moment
'''
skillsUser = ['Java', 'Python', 'C', 'C++', 'OAuth']  # <-----------------------------------------
for value in profileList.itervalues():
    skillsCurrentUser = value['skills']
    for skill in skillsCurrentUser:
        skillsVector[skill] += 1

'''
Skill Score evaluation
'''
skillV = nm.array(skillsVector.values())
skillVMag = nm.sqrt(skillV.dot(skillV))
userSkillMag = nm.sqrt(len(skillsUser))

skillScore = 0
for skill in skillsUser:
    skillScore += skillsVector[skill]

skillCosSim = float(skillScore)/(skillVMag * userSkillMag)

print "Cosine similarity of skills is: %f" % skillCosSim



