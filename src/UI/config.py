import os

CSRF_ENABLED = True
SECRET_KEY = 'you-shall-not-pass'

OPENID_PROVIDERS = [
    { 'name': 'Google_1', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo_1', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

COMPANY_LIST = [
    'Amazon', 'Microsoft', 'Yahoo', 'Nvidia', 'Google', 'Facebook', 'Bloomberg', 'Cisco', 'Intel'
]

PROFILE_LIST = ['Software Engineer', 'Recruiter', 'Manager']

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
