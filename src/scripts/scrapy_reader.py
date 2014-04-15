__author__ = 'karthik'

import cPickle

dump_file = open('all_companies.json', 'r')
item = cPickle.load(dump_file)
print item
