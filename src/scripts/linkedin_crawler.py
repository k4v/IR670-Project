__author__ = 'karthik'

import ConfigParser
from linkedin import linkedin


class LinkedInCrawler():
    __return_url = "http://localhost/"

    authentication = None
    application = None

    def __init__(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.readfp(open('data/oauth.keys'))

        self.__consumer_key = config_parser.get('ouath-keys', 'consumer.key')
        self.__consumer_secret = config_parser.get('ouath-keys', 'consumer.secret')
        self.__user_token = config_parser.get('ouath-keys', 'user.token')
        self.__user_secret = config_parser.get('ouath-keys', 'user.secret')

        self.authentication = linkedin.LinkedInDeveloperAuthentication(self.__consumer_key, self.__consumer_secret,
                                                                       self.__user_token, self.__user_secret,
                                                                       self.__return_url,
                                                                       linkedin.PERMISSIONS.enums.values())

    def create_application_object(self):
        if self.application is None:
            self.application = linkedin.LinkedInApplication(self.authentication)

        return self.application


company_names = ['Cisco']
position_list = ['Software Engineer', 'Software Engineer Test',
                 'Recruiter', 'Manager']
lin_crawler = LinkedInCrawler()
app_obj = lin_crawler.create_application_object()

per_page_results = 25

for company_name in company_names:
    company_file = open('data/' + company_name.lower() + '_dump.txt', 'w')
    # Get results for each profile in the company
    for position_name in position_list:
        company_file.write('# ' + position_name + '\n')
        for page_index in range(0, 4):
            search_response = app_obj.search_profile(selectors={'people': 'public-profile-url'},
                                                     params={'company-name': company_name,
                                                             'current-company': 'true',
                                                             'keywords': position_name,
                                                             'start': page_index * per_page_results,
                                                             'count': per_page_results})
            # End search if we've looked at all results
            if (search_response['people']['_total'] == 0) or \
               (search_response['people']['_total'] < page_index * per_page_results):
                break

            for profile in search_response['people']['values']:
                if 'publicProfileUrl' in profile:
                    profile_url = profile['publicProfileUrl']
                    company_file.write(profile_url + '\n')

    company_file.close()
