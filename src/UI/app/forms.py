from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required
from app import app

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class CompanySelectForm(Form):
    company_list = SelectField(u'Amazon', choices = [(x, x) for x in app.config['COMPANY_LIST']])
    profile_list = SelectField(u'Software Developer', choices = [(x, x) for x in app.config['PROFILE_LIST']])