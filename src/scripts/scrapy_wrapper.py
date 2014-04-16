import cPickle
import re
import time
from experience_item import ExperienceItem
from scrapy.item import Item, Field
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from bs4 import BeautifulSoup


class LinkedInItem(Item):
    url = Field()
    skills = Field()
    experience = Field()


class AuthLinkedInSpider(InitSpider):
    name = 'AuthLinkedIn'
    allowed_domains = ['linkedin.com']

    start_urls = []

    login_page = 'https://www.linkedin.com/uas/login'

    write_json = open('all_companies.json', 'w')
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
            # Something went wrong, we couldn't log in, so nothing happens.
            self.log("Login failed")

    def cleanup(self):
        cPickle.dump(self.profile_map, self.write_json)
        print self.profile_map
        self.write_json.close()

    def set_start_urls(self, start_url_list):
        self.start_urls = start_url_list

    def parse(self, response):
        sel = Selector(response)
        profile = {'url': response.url, 'skills': [], 'experience': []}

        # Parse current page URL (public profile URL)

        # Read Skills section
        skills_list = sel.xpath('//a[@class="endorse-item-name-text"]').extract()

        for skill in skills_list:
            skill = self.remove_tag('a', skill)
            profile['skills'].append(skill)

        # List of experience items
        exp_items = []

        # Read Companies and Titles
        exp_entries = sel.xpath('//div[contains(@id, "experience-") and contains(@id, "-view")]').extract()
        for exp_entry in exp_entries:
            b_soup = BeautifulSoup(exp_entry)

            #Get company name
            exp_company_matches = b_soup.findChildren('a', href=re.compile(r'prof-exp-company-name'))
            exp_company = exp_company_matches[len(exp_company_matches) - 1].get_text()\
                if len(exp_company_matches) > 0 else None

            # Get title within company
            exp_title = b_soup.findChild('a', {'name': 'title'}).get_text()

            # Get work description
            exp_desc_match = b_soup.findChild('p', {'class': 'description'})
            exp_desc = exp_desc_match.get_text() if exp_desc_match is not None else None

            # Get work date-locale
            exp_date_loc = b_soup.findChild('span', {'class': 'experience-date-locale'})

            exp_duration_items = exp_date_loc.findChildren('time')
            exp_is_current = 'Present' in exp_duration_items[1].get_text()
            exp_duration = re.sub(r'[^a-zA-Z0-9 ]', '', exp_duration_items[2].get_text()).strip()

            exp_location_item = exp_date_loc.findChild('span', {'class': 'locality'})
            exp_location = None
            if exp_location_item is not None:
                exp_location = re.sub(r'^[^"]*"', '', exp_location_item.get_text())
                exp_location = exp_location.replace("\"", "").strip()

            exp_items.append(ExperienceItem(exp_is_current, exp_title, exp_company,
                                            exp_location, exp_duration, exp_desc))

        profile['experience'] = exp_items

        # Sleep to appease LinkedIn rate limiting
        time.sleep(5)

        self.profile_map[response.url] = profile
        return LinkedInItem(profile)

    @staticmethod
    def remove_tag(tag_name, string):
        string = re.sub(r'\n\s*', "", string)
        string = re.sub(r'<' + tag_name + '[^>]*>', "", string)
        return string.replace("</" + tag_name + ">", "")
