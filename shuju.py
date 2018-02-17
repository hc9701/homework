from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'h@rd t0 gu3Ss Str1n9'
csrf = CSRFProtect(app)

if __name__ == '__main__':
    from views import *

    app.run(debug=True)
