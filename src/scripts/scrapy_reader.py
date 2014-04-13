__author__ = 'karthik'

import cPickle

dump_file = open('scraped.json', 'r')
item = cPickle.load(dump_file)
print item
