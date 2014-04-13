__author__ = 'karthik'


from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log, signals
from scrapy_wrapper import LinkedInSpider
from twisted.internet import reactor


def stop_reactor():
    reactor.stop()


people_map = ['http://in.linkedin.com/pub/nitish-kumar/45/58b/29', 'http://www.linkedin.com/in/viditochani',
              'http://www.linkedin.com/pub/denis-bellavance/5/b15/63a', 'http://www.linkedin.com/in/seansharma',
              'http://www.linkedin.com/pub/madhwaraj-g-k/10/98/64', 'http://www.linkedin.com/in/kgillett',
              'http://www.linkedin.com/in/semihenergin', 'http://www.linkedin.com/in/sharathchandrapilli',
              'http://www.linkedin.com/pub/nitish-kackar/a/b07/635', 'http://www.linkedin.com/in/rkots',
              'http://www.linkedin.com/pub/amit-nain/19/519/47a', 'http://www.linkedin.com/in/rachitdhall']

dispatcher.connect(stop_reactor, signal=signals.spider_closed)

linkedin_spider = LinkedInSpider()

crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(linkedin_spider)
crawler.start()

# log.start(loglevel=log.DEBUG, crawler=crawler, logstdout=True)

reactor.run()

linkedin_spider.cleanup()
