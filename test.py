from linkedin import linkedin
from oauthlib import *

class LinkedInCrawler():
    consumer_key        = "75dkp5mywna5gh"
    consumer_secret     = "3KKU269ElBobsGzA"
    user_token          = "71a19fa3-6951-4ba2-b725-c8cbc15705e6"
    user_secret         = "88e68848-8b45-4034-b7ad-fefb2d6d1cc7"
    return_url          = "http://localhost:8000"
    authentication      = None
    application         = None

    def __init__(self):
        self.authentication = linkedin.LinkedInDeveloperAuthentication(self.consumer_key, self.consumer_secret,
                                                      self.user_token, self.user_secret,
                                                      self.return_url, linkedin.PERMISSIONS.enums.values())

    def create_application_object(self):
        self.application = linkedin.LinkedInApplication(self.authentication)
        return self.application

def main():
    linkedInCrawler = LinkedInCrawler()
    application = linkedInCrawler.create_application_object()
    #g = application.get_profile()
    company_info = application.search_company(selectors=[{'companies': ['name', 'universal-name', 'website-url']}], params={'keywords': 'apple microsoft'})
    #connections = application.get_connections()
    print company_info
    #print g

if __name__ == '__main__':
    main()