__author__ = 'Nikhil'

import scrapy_reader
from collections import defaultdict
import numpy as nm

def skill_score(skill_list, user_skill_list):
    skill_v = nm.array(skill_list.values())
    skill_v_mag = nm.sqrt(skill_v.dot(skill_v))
    user_skill_mag = nm.sqrt(len([x for x in skill_list if x in user_skill_list]))

    score = 0
    for attr in user_skill_list:
        if attr in skill_list:
            score += skill_list[attr]
    skill_cos_sim = float(score)/(skill_v_mag * user_skill_mag)
    return skill_cos_sim

profileList = scrapy_reader.get_company_dump('facebook')

avg_sim = 0
sim_count = 0
IndexA = defaultdict(list)
IndexB = defaultdict(list)
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
    sortedSkillsVector = sorted(skillsVector, key=lambda key: skillsVector[key], reverse=True)
    flag = 0
    for skill in sortedSkillsVector[0:len(skillsUser)]:
        IndexA[skill] = skillsVector[skill]
        if skillsVector[skill] >= len(profileList)/2:
            IndexB[skill] = skillsVector[skill]
        else:
            flag = 1
    if flag == 0:
        for skill in sortedSkillsVector[len(skillsUser)+1:len(sortedSkillsVector)]:
            if skillsVector[skill] >= len(profileList)/2:
                IndexB[skill] = skillsVector[skill]
            else:
                break

    '''
    skillsVector - Dictionary of all skills in the company
    IndexA - Dictionary of top x skills, where x is no: of skills of current user
    IndexB - Dictionary of skills which at least half of the employees in the company possess
    '''
    #skillScore = skill_score(skillsVector, skillsUser)
    #skillScore = skill_score(IndexA, skillsUser)
    skillScore = skill_score(IndexB, skillsUser)
    print skillScore

    avg_sim += skillScore
    sim_count += 1

print "Average: "+str(avg_sim/sim_count)

