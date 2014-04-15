import cPickle
import re
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

    # Amazon
    start_urls = ['http://www.linkedin.com/pub/nitish-kumar/45/58b/29', 'http://www.linkedin.com/in/viditochani',
                  'http://www.linkedin.com/pub/denis-bellavance/5/b15/63a', 'http://www.linkedin.com/in/seansharma',
                  'http://www.linkedin.com/pub/madhwaraj-g-k/10/98/64', 'http://www.linkedin.com/in/kgillett',
                  'http://www.linkedin.com/in/semihenergin', 'http://www.linkedin.com/in/sharathchandrapilli',
                  'http://www.linkedin.com/pub/nitish-kackar/a/b07/635', 'http://www.linkedin.com/in/rkots',
                  'http://www.linkedin.com/pub/amit-nain/19/519/47a', 'http://www.linkedin.com/in/rachitdhall']

    # Google
    start_urls.extend(['http://www.linkedin.com/pub/vinu-rajashekhar/41/773/613',
                       'http://www.linkedin.com/pub/tushar-udeshi/0/186/434',
                       'http://www.linkedin.com/in/ravikumarmandala', 'http://www.linkedin.com/in/srikanthsastry',
                       'http://www.linkedin.com/in/vandanabachani', 'http://www.linkedin.com/in/ruchilohani',
                       'http://www.linkedin.com/in/sauravtiwari',
                       'http://www.linkedin.com/pub/jasmeet-singh/48/313/225',
                       'http://www.linkedin.com/in/kusumkumar', 'http://www.linkedin.com/pub/ritesh-gupta/8/47b/490',
                       'http://www.linkedin.com/in/sushrutkaranjkar',
                       'http://www.linkedin.com/pub/prakash-mallick/61/ab5/219',
                       'http://www.linkedin.com/pub/madhusudhan-reddy-adupala/28/7b8/485',
                       'http://www.linkedin.com/pub/panchapagesan-krishnamurthy/1/7b0/962',
                       'http://www.linkedin.com/in/bineshandrews',
                       'http://www.linkedin.com/pub/karanjit-cheema/14/887/8',
                       'http://www.linkedin.com/pub/roman-kalukiewicz/1/838/997', 'http://www.linkedin.com/in/galiu',
                       'http://www.linkedin.com/in/tanmaykhirwadkar',
                       'http://www.linkedin.com/pub/aneesh-mulye/18/331/85',
                       'http://www.linkedin.com/in/zhouxing', 'http://www.linkedin.com/in/kashyappuranik',
                       'http://www.linkedin.com/pub/prakash-mallick/61/ab5/219',
                       'http://www.linkedin.com/pub/garima-agarwal/12/4a3/312',
                       'http://www.linkedin.com/in/divyasudhakar'])

    # Facebook
    start_urls.extend(['http://www.linkedin.com/in/tejaspatil1', 'http://www.linkedin.com/in/kapilgoenka',
                       'http://www.linkedin.com/in/paritoshaggarwal',
                       'http://www.linkedin.com/pub/adithya-surampudi/1a/b64/797',
                       'http://www.linkedin.com/in/shuxiu', 'http://www.linkedin.com/in/gauravmenghani',
                       'http://www.linkedin.com/in/abhishekkona', 'http://www.linkedin.com/in/akhilravidas',
                       'http://www.linkedin.com/pub/nishanth-ps/15/748/333',
                       'http://www.linkedin.com/pub/keith-adams/5/518/1b4',
                       'http://www.linkedin.com/in/skoppala', 'http://www.linkedin.com/pub/dipanshu-agrawal/56/4b6/871',
                       'http://www.linkedin.com/in/nitinisthename',
                       'http://www.linkedin.com/pub/saurabh-chakradeo/30/b01/7b8',
                       'http://www.linkedin.com/pub/yueh-hsuan-chiang/81/b25/85a',
                       'http://www.linkedin.com/in/agrwlgaurav',
                       'http://www.linkedin.com/in/kurchi', 'http://www.linkedin.com/pub/aravind-anbudurai/46/8a5/916',
                       'http://www.linkedin.com/pub/avani-nandini/18/137/763',
                       'http://www.linkedin.com/pub/rishit-shroff/11/609/6b6',
                       'http://www.linkedin.com/pub/siva-keshava-sastry-popuri/11/5/479',
                       'http://www.linkedin.com/pub/ben-bharat-b/60/455/4b4'])

    # Nvidia
    start_urls.extend(
        ['http://www.linkedin.com/pub/nadir-cazi/14/52b/32', 'http://www.linkedin.com/pub/bharath-h-s/13/43/987',
         'http://www.linkedin.com/pub/jay-agarwal/a/83/511', 'http://www.linkedin.com/in/spyne',
         'http://www.linkedin.com/in/contactshashanksharma', 'http://www.linkedin.com/pub/ajay-agarwal/9/853/438',
         'http://www.linkedin.com/pub/koushik-bhattacharya/17/8a6/947', 'http://www.linkedin.com/in/gpradypkumar',
         'http://www.linkedin.com/in/sumantadatta', 'http://www.linkedin.com/pub/krishna-vadali/18/6ab/72'])

    # Adobe
    start_urls.extend(['http://www.linkedin.com/in/shankarv25', 'http://www.linkedin.com/in/vakul',
                       'http://www.linkedin.com/in/gauravright85', 'http://www.linkedin.com/pub/anirudh-singh/8/2b/867',
                       'http://www.linkedin.com/in/guptasushant16', 'http://www.linkedin.com/pub/vinod-thak/16/170/748',
                       'http://www.linkedin.com/pub/ashish-agarwal/1b/939/2b4',
                       'http://www.linkedin.com/pub/ravi-chaudhary/1b/824/b1',
                       'http://www.linkedin.com/pub/mosum-gaba/6/345/74',
                       'http://www.linkedin.com/pub/shruti-gupta/10/71/1a0'])

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

        self.profile_map[response.url] = profile
        return LinkedInItem(profile)

    @staticmethod
    def remove_tag(tag_name, string):
        string = re.sub(r'\n\s*', "", string)
        string = re.sub(r'<' + tag_name + '[^>]*>', "", string)
        return string.replace("</" + tag_name + ">", "")
