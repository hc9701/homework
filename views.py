from flask import render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFError

from shuju import app,db
from templates.forms import LoginForm



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not form.errors:
                db.users.find_one()
                flash()
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/user/home')
def home():
    return render_template('home.html')


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'
