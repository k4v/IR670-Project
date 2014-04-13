import cPickle
import re
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
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
    name = 'LinkedIn'
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
        skills_list = sel.xpath('//div[@id="profile-skills"]/ul[1]/li[1]/span/span/a').extract()

        for skill in skills_list:
            skill = self.remove_spans(skill)
            profile['skills'].append(skill)

        # Read Experience section
        experience_list = []

        current_exp_titles = sel.xpath(
            '//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
            'first experience vevent vcard summary-current"]/div/h3/span').extract()

        current_exp_companies = sel.xpath('//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
                                          'first experience vevent vcard summary-current"]/div/h4/strong/a/'
                                          'span[@class="org summary"]').extract()

        for current_exp in [(current_exp_titles[i], current_exp_companies[i]) for i in range(len(current_exp_titles))]:
            print (self.remove_spans(current_exp[0]), self.remove_spans(current_exp[1]))

        self.profile_map[response.url] = profile
        return LinkedInItem(profile)

    @staticmethod
    def remove_spans(string):
        string = re.sub(r'\n\s*', "", string)
        string = re.sub(r'<span[^>]*>', "", string)
        return string.replace("</span>", "")


class AuthLinkedInSpider(InitSpider):
    name = 'AuthLinkedIn'
    allowed_domains = ['linkedin.com']
    start_urls = ['http://www.linkedin.com/pub/nitish-kumar/45/58b/29', 'http://www.linkedin.com/in/viditochani',
                  'http://www.linkedin.com/pub/denis-bellavance/5/b15/63a', 'http://www.linkedin.com/in/seansharma',
                  'http://www.linkedin.com/pub/madhwaraj-g-k/10/98/64', 'http://www.linkedin.com/in/kgillett',
                  'http://www.linkedin.com/in/semihenergin', 'http://www.linkedin.com/in/sharathchandrapilli',
                  'http://www.linkedin.com/pub/nitish-kackar/a/b07/635', 'http://www.linkedin.com/in/rkots',
                  'http://www.linkedin.com/pub/amit-nain/19/519/47a', 'http://www.linkedin.com/in/rachitdhall']

    login_page = 'https://www.linkedin.com/uas/login'

    write_json = open('scraped.json', 'w')
    profile_map = {}

    def init_request(self):
        # This function is called before crawling starts
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        # Generate a login request
        return FormRequest.from_response(response,
                                         formdata={'session_key': '',
                                                   'session_password': ''},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        # Check the response returned by a login request to see if we are successfully logged in.
        if "Sign Out" in response.body:
            self.log("Login successful")
            # Now the crawling can begin
            return self.initialized()
        else:
            # Something went wrong, we couldn't log in, so nothing happens.1
            self.log("Login failed")

    def cleanup(self):
        cPickle.dump(self.profile_map, self.write_json)
        print self.profile_map
        self.write_json.close()

    def parse(self, response):
        sel = Selector(response)
        profile = {'url': response.url, 'skills': []}

        print response.url

        # Parse current page URL (public profile URL)

        # Read Skills section
        skills_list = sel.xpath('//a[@class="endorse-item-name-text"]').extract()

        for skill in skills_list:
            skill = self.remove_tag('a', skill)
            profile['skills'].append(skill)

        print profile['skills']

        # Read Experience section
        experience_list = []

        current_exp_titles = sel.xpath(
            '//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
            'first experience vevent vcard summary-current"]/div/h3/span').extract()

        current_exp_companies = sel.xpath('//div[@id="profile-experience"]/div[2]/div/div[1]/div[@class="position  '
                                          'first experience vevent vcard summary-current"]/div/h4/strong/a/'
                                          'span[@class="org summary"]').extract()

        for current_exp in [(current_exp_titles[i], current_exp_companies[i]) for i in range(len(current_exp_titles))]:
            print (self.remove_tag('span', current_exp[0]), self.remove_tag('span', current_exp[1]))

        self.profile_map[response.url] = profile
        return LinkedInItem(profile)

    @staticmethod
    def remove_tag(tag_name, string):
        string = re.sub(r'\n\s*', "", string)
        string = re.sub(r'<'+tag_name+'[^>]*>', "", string)
        return string.replace("</"+tag_name+">", "")
