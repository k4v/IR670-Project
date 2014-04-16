__author__ = 'karthik'

import cPickle

dump_file = open('all_companies.json', 'r')
profile_dump = cPickle.load(dump_file)


def get_company_dump(company_name):
    profile_list = []
    company_name = unicode(company_name.strip().lower())

    for profile in profile_dump:
        add_profile = False
        for exp_item in profile_dump[profile]['experience']:
            if exp_item.company.strip().lower().find(company_name) >= 0 or \
                    company_name.find(exp_item.company.strip().lower()) >= 0:
                add_profile = True
        if add_profile:
            profile_list.append(profile_dump[profile])

    return profile_list
