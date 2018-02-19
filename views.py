from itertools import chain

from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFError

from shuju import app, db
from templates.forms import LoginForm, RegisterForm

POST = 'POST'

GET = 'GET'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=[GET, POST])
def login():
    form = LoginForm()
    if request.method == POST:
        if form.validate_on_submit():
            d = db.users.find_one({
                'username': form.username.data,
                'password': form.password.data,
                'is_admin': form.identity.data,
            })
            if d:
                flash('登录成功')
                del d['_id']
                session['user'] = d
                return redirect(url_for('home') if not d['identity'] else url_for(''))
            else:
                flash('用户名或密码错误')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('login.html', form=form)


@app.route('/user/home')
def home():
    return render_template('home.html')


@app.route('/register',methods=[GET,POST])
def register():
    form = RegisterForm()
    if request.method == POST:
        if form.validate_on_submit():
            user_info = {
                'username': form.username.data,
                'password': form.password.data,
                'is_admin': 0,
            }
            d = db.users.find_one(user_info)
            if not d:
                user_info['email'] = form.email.data
                db.users.insert(user_info)
                flash('注册成功')
                return redirect(url_for('user_center'))
            flash('用户名已存在')
        flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('register.html', form=form)

@app.route('/user/user_center')
def user_center():
    return render_template('usercenter.html')


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'
