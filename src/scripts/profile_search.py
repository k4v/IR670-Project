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

crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(linkedin_spider)
crawler.start()

log.start(loglevel=log.DEBUG, crawler=crawler, logstdout=True)

reactor.run()

linkedin_spider.cleanup()