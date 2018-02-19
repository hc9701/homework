from flask import Flask
from flask_wtf import CSRFProtect
import pymongo

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'db_name': 'shuju',
    'username': None,
    'password': None
}

class MongoConn(object):

    def __init__(self):
        # connect db
        self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
        self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
        self.username = MONGODB_CONFIG['username']
        self.password = MONGODB_CONFIG['password']
        if self.username and self.password:
            self.connected = self.db.authenticate(self.username, self.password)
        else:
            self.connected = True


app = Flask(__name__)
app.config['SECRET_KEY'] = 'h@rd t0 gu3Ss Str1n9'
csrf = CSRFProtect(app)
db = MongoConn().db



if __name__ == '__main__':
    from views import *
    app.run(debug=True)
    map()