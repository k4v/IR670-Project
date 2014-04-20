__author__ = 'karthik'

import cPickle
import os

cwd = os.getcwd()
os.chdir('../scripts')
os.chdir(cwd)

profile_dump = {}


def load_all_companies():
    global profile_dump

    for pickle_file in [pickle_file for pickle_file in os.listdir('data') if pickle_file.endswith('.pickle')]:
        profile_dump.update(cPickle.load(open('data/'+pickle_file, 'r')))


def get_company_dump(company_name, pos_title=False, location=False):
    global profile_dump

    profile_list = []
    company_name = unicode(company_name.strip().lower())

    for profile in profile_dump:
        add_profile = False
        for exp_item in profile_dump[profile]['experience']:
            if (exp_item.company.strip().lower().find(company_name) >= 0 or  # Check if company name matches
                company_name.find(exp_item.company.strip().lower()) >= 0) \
            and (exp_item.postitle.strip().lower().find(pos_title) >= 0 or   # Check if job title matches
                pos_title.find(exp_item.postitle.strip().lower()) >= 0) \
            and (any([x.strip() == y.strip()                                 # Check if location matches
                      for x in exp_item.location.split(',') for y in location.split(',')])):
                add_profile = True
        if add_profile:
            profile_list.append(profile_dump[profile])

    return profile_list


load_all_companies()