from itertools import chain

from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFError

from shuju import app, db
from forms import *

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
                'is_admin': form.is_admin.data,
            })
            if d:
                flash('登录成功')
                del d['_id']
                session['user'] = d
                if d['is_admin']:
                    # todo
                    pass
                else:
                    return redirect(url_for('home'))
            else:
                flash('用户名或密码错误')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('login.html', form=form)


@app.route('/register', methods=[GET, POST])
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
            else:
                flash('用户名已存在')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('register.html', form=form)


@app.route('/user/user_center', methods=[GET, POST])
def user_center():
    form = UserCenterForm()
    user = session['user']

    if request.method == POST:
        if form.validate_on_submit():
            if form.username.data != user['username']:
                flash('不能修改用户名')
            else:
                password = form.new_password.data
                if user['password'] != password and password != '':
                    user['password'] = password
                user['app1'] = form.app1.data
                user['app2'] = form.app2.data
                user['word1'] = form.word1.data
                user['word2'] = form.word2.data
                db.users.update_one({
                    'username': user['username'],
                },
                    {'$set': user}
                )
                flash('更新成功')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    else:
        user = session['user']
        form.username.data = user['username']
        form.new_password.data = ''
        form.confirm.data = ''
        form.email.data = user.get('email')
        form.app1.data = user.get('app1')
        form.app2.data = user.get('app2')
        form.word1.data = user.get('word1')
        form.word2.data = user.get('word2')
    return render_template('usercenter.html', form=form)


@app.route('/user/home')
def home():
    return render_template('home.html')


@app.route('/user/download')
def download():
    return render_template('APPdownload.html')


@app.route('/user/details')
def detail():
    return render_template('Details.html')


@app.route('/user/score')
def score():
    return render_template('score.html')


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'
