__author__ = 'karthik'


from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log, signals
from scrapy_wrapper import *
from twisted.internet import reactor


def stop_reactor():
    reactor.stop()

dispatcher.connect(stop_reactor, signal=signals.spider_closed)

linkedin_spider = AuthLinkedInSpider()

start_urls = []
for line in open('data/intel_dump.txt', 'r'):
    if (not (line.strip() == '')) and (not (line.strip().startswith('#'))):
        start_urls.append(line.strip())

linkedin_spider.set_start_urls(start_urls)

crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(linkedin_spider)
crawler.start()

log.start(loglevel=log.DEBUG, crawler=crawler, logstdout=True)

reactor.run()

linkedin_spider.cleanup()
