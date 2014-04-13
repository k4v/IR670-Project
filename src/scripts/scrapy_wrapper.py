import cPickle
import re
from scrapy.contrib.spiders import CrawlSpider
from scrapy.item import Item, Field
from scrapy.selector import Selector


class LinkedInItem(Item):
    url = Field()
    skills = Field()
    experience = Field()


class ExperienceItem:
    def __init__(self, is_current, postitle, company, desc):
        self.is_current = is_current
        self.postitle = postitle
        self.company = company
        self.desc = desc


class LinkedInSpider(CrawlSpider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']
    start_urls = ['http://in.linkedin.com/pub/nitish-kumar/45/58b/29', 'http://www.linkedin.com/in/viditochani',
                  'http://www.linkedin.com/pub/denis-bellavance/5/b15/63a', 'http://www.linkedin.com/in/seansharma',
                  'http://www.linkedin.com/pub/madhwaraj-g-k/10/98/64', 'http://www.linkedin.com/in/kgillett',
                  'http://www.linkedin.com/in/semihenergin', 'http://www.linkedin.com/in/sharathchandrapilli',
                  'http://www.linkedin.com/pub/nitish-kackar/a/b07/635', 'http://www.linkedin.com/in/rkots',
                  'http://www.linkedin.com/pub/amit-nain/19/519/47a', 'http://www.linkedin.com/in/rachitdhall']

    write_json = open('scraped.json', 'w')
    profile_map = {}

    def cleanup(self):
        cPickle.dump(self.profile_map, self.write_json)
        print self.profile_map
        self.write_json.close()

    def set_url(self, crawl_url):
        self.start_urls = [crawl_url]

    def parse(self, response):
        sel = Selector(response)
        profile = {'url': response.url, 'skills': []}

        # Parse current page URL (public profile URL)

        # Read Skills section
        skills_list = sel.xpath('string(//span[@class="jellybean"])').extract()
        print [self.remove_spans(x) for x in skills_list]

        for skill in skills_list:
            skill = self.remove_spans(skill)
            profile['skills'].append(skill)

        # Read Experience section
        experience_list = []

        current_exp_titles = sel.xpath(
            '//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
            'first experience vevent vcard summary-current"]/div/h3/span').extract()

        current_exp_companies = sel.xpath('//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
                                          'first experience vevent vcard summary-current"]/*span[@class=org summary]').extract()

        for current_exp in [(current_exp_titles[i], current_exp_companies[i]) for i in range(len(current_exp_titles))]:
            print (self.remove_spans(current_exp[0]), self.remove_spans(current_exp[1]))

        self.profile_map[response.url] = profile
        return LinkedInItem(profile)

    @staticmethod
    def remove_spans(string):
        print 'With '+string+"!!!!!!!!!!!"
        string = re.sub(r'\n\s*', "", string)
        string = re.sub(r'<span[^>]*>', "", string)
        return string.replace("</span>", "")