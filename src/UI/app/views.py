from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, CompanySelectForm
from models import User, ROLE_USER, ROLE_ADMIN
from linkedin import linkedin

authentication = None
application = None

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    global authentication
    global application
    user = g.user

    if authentication is None:
        return redirect(url_for('authenticate_user'))

    if application is None:
        authentication.authorization_code = request.args['code']
        authentication.get_access_token()
        application = linkedin.LinkedInApplication(authentication)


    form = CompanySelectForm()
    if form.validate_on_submit():
        return redirect(url_for('test'))
    return render_template("index.html",
        title = 'Home',
        user = user,
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

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    # Call appropriate scripts here
    print request.form['company_list']
    return "TEST!"

@app.route('/')
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
    authentication = None
    application = None
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        posts = posts)