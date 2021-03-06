__author__ = 'Nikhil'

import scrapy_reader
from collections import defaultdict
import numpy as nm

def skill_score(skill_list, user_skill_list):
    skill_v = nm.array(skill_list.values())
    skill_v_mag = nm.sqrt(skill_v.dot(skill_v))
    #print skill_v_mag
    user_skill_mag = nm.sqrt(len([x for x in skill_list if x in user_skill_list]))

    score = 0
    for attr in user_skill_list:
        if attr in skill_list:
            score += skill_list[attr]
    skill_cos_sim = float(score)/(skill_v_mag * user_skill_mag)
    return skill_cos_sim

def evaluate_employee_scores(company, title, location):
    profile_list = scrapy_reader.get_company_dump(company, title, location)
    employee_scores = [None]*len(profile_list)
    for i in range(0, len(profile_list)):
        current_employee_profile = profile_list[i]
        skills_current_user = current_employee_profile['skills']
        employee_scores[i], vector = score_evaluation(skills_current_user, company, title, location)

    return employee_scores

def score_evaluation(user_skills, user_company, user_title, user_location):
    profile_list = scrapy_reader.get_company_dump(user_company, user_title, user_location)
    if len(profile_list) == 0:
        return (0, {})
    IndexA = defaultdict(list)
    IndexB = defaultdict(list)
    skillsVector = {}
    skillsVector = defaultdict(lambda: 0, skillsVector)
    skillsUser = [x.lower() for x in user_skills]
    for j in range(0, len(profile_list)):
        value = profile_list[j]
        skillsCurrentUser = [x.lower() for x in value['skills']]
        for skill in skillsCurrentUser:
            skillsVector[skill] += 1

    '''
    Skill Score evaluation
    '''
    sortedSkillsVector = sorted(skillsVector, key=lambda key: skillsVector[key], reverse=True)
    '''
    Sorted skills formatted to display on UI
    '''
    display_skills = []
    for skills_vector in sortedSkillsVector:
        display_skills.append(skills_vector.title())

    flag = 0
    for skill in sortedSkillsVector[0:len(skillsUser)]:
        IndexA[skill] = skillsVector[skill]
        if skillsVector[skill] >= len(profile_list)/3:
            IndexB[skill] = skillsVector[skill]
        else:
            flag = 1
    if flag == 0:
        for skill in sortedSkillsVector[len(skillsUser)+1:len(sortedSkillsVector)]:
            if skillsVector[skill] >= len(profile_list)/3:
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
    return skillScore, display_skills[0:10]
