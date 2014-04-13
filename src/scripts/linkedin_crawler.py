__author__ = 'karthik'

from linkedin import linkedin


class LinkedInCrawler():

    __consumer_key = "75dkp5mywna5gh"
    __consumer_secret = "3KKU269ElBobsGzA"

    __user_token = "500e9b2f-51a9-433a-9042-9b7f4ff45830"
    __user_secret = "daecf06d-cd08-474a-be6d-c40881b557b5"

    __return_url = "http://localhost/"

    authentication = None
    application = None

    def __init__(self):
        self.authentication = linkedin.LinkedInDeveloperAuthentication(self.__consumer_key, self.__consumer_secret,
                                                                       self.__user_token, self.__user_secret,
                                                                       self.__return_url,
                                                                       linkedin.PERMISSIONS.enums.values())

    def create_application_object(self):
        if self.application is None:
            self.application = linkedin.LinkedInApplication(self.authentication)

        return self.application
