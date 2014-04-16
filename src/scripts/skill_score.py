__author__ = 'Nikhil'

import scrapy_reader
from collections import defaultdict
import numpy as nm

profileList = scrapy_reader.get_company_dump('facebook')

avg_sim = 0
sim_count = 0

'''
skillsUser need to read from the UI
hardcoding for the moment
'''
for i in range(0, len(profileList)):
    skillsVector = {}
    skillsVector = defaultdict(lambda: 0, skillsVector)

    skillsUser = profileList[i]['skills']
    if len(skillsUser) == 0:
        continue
    for j in range(0, len(profileList)):
        if i == j:
            continue

        value = profileList[j]
        skillsCurrentUser = value['skills']
        for skill in skillsCurrentUser:
            skillsVector[skill] += 1

    '''
    Skill Score evaluation
    '''
    skillV = nm.array(skillsVector.values())
    skillVMag = nm.sqrt(skillV.dot(skillV))
    userSkillMag = nm.sqrt(len([x for x in skillsVector if x in skillsUser]))

    skillScore = 0
    for skill in skillsUser:
        skillScore += skillsVector[skill]

    skillCosSim = float(skillScore)/(skillVMag * userSkillMag)

    print "Cosine similarity of skills is: %f" % skillCosSim
    avg_sim += skillCosSim
    sim_count += 1

print "Average: "+str(avg_sim/sim_count)
