from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, CompanySelectForm
from models import User, ROLE_USER, ROLE_ADMIN
from linkedin import linkedin
import sys
import os
import math
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

lib_path = os.path.abspath('../scripts')
sys.path.append(lib_path)
import skill_score
import get_keywords
import cluster_recommender

authentication = None
application = None
linkedin_user_name = ''
user_cluster = None
recommended_companies = None
recommended_profile = None
company_recommendations_based_on_score = {}

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    global authentication
    global application
    global company_recommendations_based_on_score
    global linkedin_user_name
    global user_cluster
    global recommended_companies
    global recommended_profile

    #if(os.path.isfile('./app/static/img/graph*.png')):
    #    os.remove('./app/static/img/graph.png')

    my_dir = './app/static/img/'
    for fname in os.listdir(my_dir):
        if fname.startswith("graph"):
            os.remove(os.path.join(my_dir, fname))

    user = g.user

    if authentication is None:
        return redirect(url_for('authenticate_user'))

    if application is None:
        authentication.authorization_code = request.args['code']
        authentication.get_access_token()
        application = linkedin.LinkedInApplication(authentication)

        # Get user skill list
        user_skill_list = []
        location = application.get_profile(selectors=['location'])
        linkedin_user_name = application.get_profile(selectors=['first-name'])['firstName']

        user_experience = ''
        for item in application.get_profile(selectors=['positions'])['positions']['values']:
            if 'summary' in item:
                user_experience += item['summary']

        #print get_keywords.get_keywords(user_experience)
        user_cluster = cluster_recommender.cluster_score(user_experience, user_skill_list)

        recommended_companies = [x.encode('ascii', 'ignore') for x in user_cluster[0]]
        recommended_profile   = user_cluster[1]

        for item in application.get_profile(selectors=['skills'])['skills']['values']:
            user_skill_list.append(str(item['skill']['name']))

        for company in app.config['COMPANY_LIST']:
            for title in app.config['PROFILE_LIST']:
                profile_score, top_skill_vector = skill_score.score_evaluation(user_skill_list, company, title, None)
                if (company, title) not in company_recommendations_based_on_score:
                    if math.isnan(profile_score):
                        profile_score = 0
                    company_recommendations_based_on_score[(company, title)] = math.ceil(profile_score*100)

    #print application.search_job(selectors=[{'jobs': ['id', 'customer-job-code', 'posting-date', 'position', 'location']}], params={'company-name' : 'Google', 'job-title' : 'Software Engineer', 'count': 10})
    form = CompanySelectForm()
    if form.validate_on_submit():
        return redirect(url_for('profile_score'))
    return render_template("index.html",
        title = 'Home',
        user = linkedin_user_name,
        form = form)


@app.route('/authenticate_user', methods=['GET', 'POST'])
@login_required
def authenticate_user():
    global authentication
    API_KEY = '75dkp5mywna5gh'
    API_SECRET = '3KKU269ElBobsGzA'
    RETURN_URL = 'http://localhost:5000/index'

    authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())

    return redirect(authentication.authorization_url)

@app.route('/profile_score', methods=['GET', 'POST'])
@login_required
def profile_score():
    # Call appropriate scripts here

    # Get user skill list
    user_skill_list = []
    location = application.get_profile(selectors=['location'])
    #print (location['location']['name']) + ", " + str(location['location']['country']['code'])
    for item in application.get_profile(selectors=['skills'])['skills']['values']:
        user_skill_list.append(str(item['skill']['name']))

    company = request.form['company_list']
    title   = request.form['profile_list']

    profile_score, top_skill_vector = skill_score.score_evaluation(user_skill_list, company, title, location)
    if math.isnan(profile_score):
        profile_score = 0
    profile_score = math.ceil(profile_score*100)

    employee_scores = skill_score.evaluate_employee_scores(company, title, location)
    employee_scores = [math.ceil(x*100) for x in employee_scores]
    employee_scores = [value for value in employee_scores if not math.isnan(value)]


    employee_scores.append(profile_score)
    sorted_scores = sorted(employee_scores)

    user_score_index = sorted_scores.index(profile_score) + 1

    ax = plt.subplot('111', axisbg='#EBEBEB')
    spines_to_remove = ['top', 'right']
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    plt.scatter(range(1,len(employee_scores)+1), sorted_scores, linestyle='--', marker='o', color='b')
    plt.xlabel('Employee Number')
    plt.ylabel('Profile Score')
    plt.annotate('You', xy=(user_score_index, profile_score), xytext=(user_score_index - 0.3, profile_score + 5), textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5), arrowprops=dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    file_name = './app/static/img/graph_'+str(company)+'.png'
    plt.savefig(file_name, bbox_inches='tight', transparent = True)
    plt.clf()

    return render_template("profile_score.html", company = company, score = profile_score, profile = title,
                           top_skills = top_skill_vector, user_skills = user_skill_list, curr_time = datetime.datetime.now().time())


@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('authenticate_user'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('authenticate_user'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    global authentication
    global application
    global company_recommendations_based_on_score
    global user_cluster
    authentication = None
    application = None
    user_cluster = None
    linkedin_user_name = ''
    company_recommendations_based_on_score = {}
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    global user_cluster
    global recommended_companies
    global recommended_profile

    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        #flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))

    top_company_list = []
    top_matched_companies = (sorted(company_recommendations_based_on_score, key = company_recommendations_based_on_score.get))[-7:]
    for company_profile in top_matched_companies:
        top_company_list.append((company_profile, company_recommendations_based_on_score[company_profile]))

    top_company_list = sorted(top_company_list, key = lambda x: x[1])

    print 'reco:'
    print recommended_companies
    print recommended_profile
    return render_template('user.html',
        user = linkedin_user_name,
        top_companies = reversed(top_company_list),
        recommended_companies = recommended_companies,
        recommended_profile = recommended_profile)
