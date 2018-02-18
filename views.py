from itertools import chain

from flask import render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFError

from shuju import app,db
from templates.forms import LoginForm

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
            d=db.users.find_one({
                'username':form.username.data,
                'password':form.password.data,
                'identity':form.identity.data,
            })
            if d:
                flash('登录成功')
                return redirect(url_for('home'))
        else:
            flash('\\n'.join(chain.from_iterable(form.errors.values())))
    return render_template('login.html', form=form)


@app.route('/user/home')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    form = Reg
    if request.method==GET:
        return render_template('register.html',form=form)


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'
