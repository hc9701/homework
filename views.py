import json
from itertools import chain
import collections

from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf.csrf import CSRFError
from pymongo import ASCENDING, DESCENDING, errors

from shuju import app, db
from forms import *
import numpy

from spider import SpiderFactory

limit = 20

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
                    return redirect(url_for('main'))
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
                'word1': '',
                'word2': '',
                'app1': '',
                'app2': ''
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


@app.route('/user/download/')
def download():
    user = session['user']
    app1 = user['app1']
    app2 = user['app2']
    t = datetime.now()
    apps = [get_download(app1, t), get_download(app2, t)]
    print(apps)
    return render_template('APPdownload.html', apps=apps)


@app.route('/user/details/<path:app_name>/<page>')
def detail(app_name, page, count=10):
    user = session['user']
    word1 = user['word1']
    word2 = user['word2']
    comments = []
    if app_name == 'none':
        app1 = user['app1']
        app2 = user['app2']
        d = db.comments.find({
            '$or': [
                {
                    "app_name": app1
                }, {
                    "app_name": app2
                }],
        }, {
            '_id': 0
        }).limit(count).skip(int(page) * count)
    else:
        d = db.comments.find({
            'app_name': app_name
        }, {
            '_id': 0
        }).limit(count).skip(int(page) * count)

    if d:
        for i in d:
            comments.append(i)
            i['content'] = i['content'].replace(word1, '<mark>%s</mark>' % word1)
            i['content'] = i['content'].replace(word2, '<mark>%s</mark>' % word2)
    return render_template('Details.html', comments=comments)


@app.route('/user/score')
def score():
    user = session['user']
    app1 = user['app1']
    app2 = user['app2']
    apps = [get_score(app1), get_score(app2)]
    return render_template('score.html', apps=apps)


@app.route('/user/score/search/<app_name>')
def search_score(app_name):
    app1 = get_score(app_name)
    return jsonify(app1)


@app.route('/user/download/search/<app_name>')
def search_download(app_name):
    app1 = get_download(app_name, datetime.now())
    return jsonify(app1)


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'


def get_score(app_name):
    d = db.ratings.aggregate(
        [{'$match': {'app_name': app_name, 'type': 5}}]
    )
    xing = numpy.array([x['ratings'] for x in d])
    d = db.ratings.aggregate(
        [{'$match': {'app_name': app_name, 'type': 3}}]
    )
    ping = numpy.array([x['ratings'] for x in d])
    return {
        "app_name": app_name,
        "xing": [str(x) for x in xing.sum(0)] if xing.any() else [],
        "ping": [str(x) for x in ping.sum(0)] if ping.any() else [],
    }


def get_download(app_name, times):
    last = datetime(year=times.year, month=times.month, day=1)
    first = datetime(year=times.year - 1, month=times.month, day=1)
    d1 = db.downloads.aggregate([
        {
            '$match': {
                'app_name': app_name,
                'time': {
                    '$gte': first,
                    '$lt': last,
                },
            }
        }, {
            '$group': {
                '_id': {
                    '$month': '$time',
                }, 'value': {
                    '$sum': '$value'
                }
            }
        }
    ])
    d2 = db.downloads.find(
        {
            "app_name": app_name,
            'time': {'$gte': times - timedelta(days=8)}
        }, {
            "_id": 0,
            "time": 1,
            "value": 1,
        }).sort("time", ASCENDING).limit(7)
    monthly_data = [(x['_id'], abs(x['value'] // 1000)) for x in d1]
    monthly_data.sort(key=lambda l: l[0])
    d = collections.deque(monthly_data)
    d.rotate(13 - times.month)
    daily_data = [('%02d-%02d' % (x['time'].month, x['time'].day), abs(x['value'] // 1000)) for x in d2]
    return {
        "app_name": app_name,
        "monthly_data": [list(x) for x in zip(*d)],
        "daily_data": [list(x) for x in zip(*daily_data)],
    }


@app.route('/manage/show_users/<int:page>')
def show_users(page, limit=limit):
    user_list = []
    d = db.users.find({}).limit(limit).skip((page - 1) * limit)
    session['show_users_page'] = page
    return render_template('show_users.html', user_list=d)


@app.route('/manage/delete_user/<username>')
def delete_user(username):
    n = db.users.delete_one({'username': username, 'is_admin': 0})
    if n:
        flash('删除成功')
    else:
        if db.users.find_one({'username': username, 'is_admin': 1}):
            flash('管理员不能被删除')
        else:
            flash('用户名不存在')
    return redirect(url_for('show_users', page=session['show_user_page']))


@app.route('/manage/modify_user/<username>', methods=[GET, POST])
def modify_user(username):
    form = ModifyUserForm
    if request.method == POST:
        if form.validate_on_submit():
            if request.method == POST:
                if form.validate_on_submit():
                    if form.username.data != username:
                        flash('不能修改用户名')
                    else:
                        password = form.new_password.data
                        user = {
                            'username': username,
                            'password': form.new_password.data,
                            'confirm': form.confirm.data,
                            'email': form.email.data,
                        }
                        db.users.update_one({
                            'username': user['username'],
                            'is_admin': form.is_admin.data,
                        },
                            {'$set': user}
                        )
                        flash('更新成功')
                        return redirect(url_for('show_users', page=session['show_users_page']))
                else:
                    flash('\\n'.join(chain.from_iterable(form.errors.values())))
    else:
        user = db.users.find_one({
            'username': username,
            'is_admin': 0
        })
        form.username.data = user['username']
        form.email.data = user['email']
    return render_template('modify_user.html', form=form)


@app.route('/manage/add_user', methods=[GET, POST])
def add_user():
    form = AddUserForm()
    if request.method == POST:
        if form.validate_on_submit():
            d = db.users.find_one({
                'username': form.username.data,
                'is_admin': form.is_admin.data,
            })
            if d:
                flash('用户名已存在')
            else:
                db.users.insert_one({
                    'username': form.username.data,
                    'password': form.password.data,
                    'is_admin': form.is_admin.data,
                    'email': form.email.data,
                    'word1': '',
                    'word2': '',
                    'app1': '',
                    'app2': ''
                })
                flash('添加用户成功')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('add_user.html', form=form)


@app.route('/manage/show_comments/<int:page>')
def show_comments(page=1, limit=limit):
    d = db.comments.find().limit(limit)
    session['show_comments_page'] = page
    return render_template('show_comments.html', comment_list=d)


@app.route('/manage/delete_comment/<id>')
def delete_comments(id):
    n = db.comments.delete_one({'_id': id})
    flash('删除成功')
    return redirect(url_for('show_comments', page=session['show_comments_page']))


@app.route('/manage/show_downloads/<int:page>')
def show_downloads(page, limit=limit):
    d = db.downloads.find().limit(limit).sort('time', DESCENDING)
    session['show_downloads_page'] = page
    return render_template('show_downloads.html', download_list=d)


@app.route('/manage/show_downloads/<id>')
def delete_downloads(id):
    n = db.downloads.delete_one({'_id': id})
    flash('删除成功')
    return redirect(url_for('show_downloads', page=session['show_downloads_page']))


@app.route('/manage/show_stars/<int:page>')
def show_stars(page, limit=limit):
    d = db.ratings.find({'type': 5}).limit(limit)
    session['show_stars_page'] = page
    return render_template('show_stars.html', star_list=d)


@app.route('/manage/delete_stars/<id>')
def delete_stars(id):
    n = db.ratings.delete_one({'_id': id})
    flash('删除成功')
    return redirect(url_for('show_stars', page=session['show_stars_page']))


@app.route('/manage/show_assessment/<int:page>')
def show_assessments(page, limit=limit):
    d = db.ratings.find({'type': 5}).limit(limit)
    session['show_assessment_page'] = page
    return render_template('show_assessment.html', star_list=d)


@app.route('/manage/delete_assessment/<id>')
def delete_assessment(id):
    n = db.ratings.delete_one({'_id': id})
    flash('删除成功')
    return redirect(url_for('show_assessments', page=session['show_assessment_page']))


@app.route('/manage/load_net_data', methods=[GET, POST])
def load_net_data():
    form = LoadNetDataForm()
    if request.method == POST:
        if form.validate_on_submit():
            try:
                spider = SpiderFactory.create_spider(form.url.data)
                spider.parse()
                spider.store()
                flash('数据导入成功')
            except errors.BulkWriteError:
                flash('数据导入成功')
            except Exception:
                flash('找不到对应的数据')
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('load_net_data.html', form=form)


@app.route('/manage/modify_data', methods=[GET, POST])
def modify_data():
    form = ModifyDataForm()
    if request.method == POST:
        if form.validate_on_submit():
            if request.method == POST:
                user = session['user']
                if form.validate_on_submit():
                    if form.username.data != user['username']:
                        flash('不能修改用户名')
                    else:
                        password = form.new_password.data
                        if user['password'] != password and password != '':
                            user['password'] = password
                        db.users.update_one({
                            'username': user['username'],
                            'is_admin': 1
                        },
                            {'$set': user}
                        )
                        flash('更新成功')
    else:
        user = session.get('user')
        form.username.data = user['username']
        form.email.data = user.get('email')
    return render_template('modify_data.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/manage/main')
def main():
    return render_template('base_template/base_admin.html')


@app.before_request
def verify():
    user = session.get('user')
    if request.url.find('/user/') > -1:
        if not user:
            flash('请先登录')
            return redirect(url_for('login'))
    elif request.url.find('/manage/') > -1:
        if not user or not user['is_admin']:
            flash('请先登录')
            return redirect(url_for('login'))
    print(request.url)


@app.route('/manage/load_excel')
def load_excel():
    form = UploadForm()
    return render_template('load_excel.html', form=form)


@app.route('/manage/save_excel',methods=[POST])
def save_excel():
    f = request.files['file']
    return redirect(url_for('load_excel'))
