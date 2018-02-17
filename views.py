from flask import render_template
from flask_wtf.csrf import CSRFError

from shuju import app
from templates.forms import LoginForm


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.html', form=form)


@app.errorhandler(CSRFError)
def csrf_error(reason):
    return 'emmm'
