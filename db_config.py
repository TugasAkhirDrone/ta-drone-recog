
from flask_mysqldb import MySQL
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dronerecog'
app.config['UPLOAD_FOLDER'] = 'static/files'

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'drone-recog'
mysql.init_app(app)