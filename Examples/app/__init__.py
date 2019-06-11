from flask import Flask

# config
# server will reload on source changes, and provide a debugger for errors
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above
# crf token for login and register (set an environment variable using secrets.token_hex(16))
# create a database first with db.create_all() before you start messing with a db
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

""" 
(__name__) is a reserve variable in python which the python interpreter sets to be 
the name of the file or module in which it is reading). If we put our configuration in 
another file, we would tell Flask to look in that file instead.
"""


# decorator which tells flask what url triggers this fn
@app.route('/')
def index():
  return '<p>Hello world</p>'


"""
The line @app.route('/') means that when a request for "/" is made, 
Flask will run the [native] function index(); This will return the HTML 
for the page we want to show for that request.

This is an example route that we will erase when we create route.py
"""

# import at the bottom to avoid circular imports which will mess up your application
from app import routes