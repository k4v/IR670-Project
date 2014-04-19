__author__ = 'karthik'

import cPickle
import os

cwd = os.getcwd()
os.chdir('../scripts')
dump_file = open('data/all_companies.json', 'r')
profile_dump = cPickle.load(dump_file)
os.chdir(cwd)


def get_company_dump(company_name, pos_title=False, location=False):
    profile_list = []
    company_name = unicode(company_name.strip().lower())

    for profile in profile_dump:
        add_profile = False
        for exp_item in profile_dump[profile]['experience']:
            if (exp_item.company.strip().lower().find(company_name) >= 0 or  # Check if company name matches
                company_name.find(exp_item.company.strip().lower()) >= 0) \
            and (exp_item.postitle.strip().lower().find(pos_title) >= 0 or   # Check if job title matches
                pos_title.find(exp_item.pos_title.strip().lower()) >= 0) \
            and (any([x.strip() == y.strip()                                 # Check if location matches
                      for x in exp_item.location.split(',') for y in location.split(',')])):
                add_profile = True
        if add_profile:
            profile_list.append(profile_dump[profile])

    return profile_list
