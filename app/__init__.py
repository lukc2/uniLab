from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import sqlite3
import os
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, NoneOf, Email

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
dbPath = os.path.join(ROOT_DIR, './static/database.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__, static_url_path='',
            static_folder='./static',
            template_folder='./templates')
app.config['SECRET_KEY'] = 'Supertajnehaslo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(ROOT_DIR, './static/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(ROOT_DIR, './static/img/cats/')
app.config['USER_UNAUTHORIZED_ENDPOINT'] = 'noaccess'
app.config['USER_ENABLE_EMAIL'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LebyaIZAAAAADh1mxzILmWIHBSNNN6AZ9meGVEL'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LebyaIZAAAAAF3_yzQdE2d9vv_hWg3FUYVww93R'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(257), unique=False, nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


db.create_all()


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    remember = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    emails = [e.email for e in db.session.query(User.email).distinct()]
    usernames = [u.username for u in db.session.query(User.username).distinct()]
    email = StringField('Email', validators=[InputRequired(),
                                             NoneOf(emails, message="Account with that email already exists"),
                                             Email(message='Invalid email'), Length(max=50)])
    username = StringField('Login', validators=[InputRequired(),
                                                NoneOf(usernames, message="Username taken"),
                                                Length(min=4, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])


class UploadForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired('Name can not be empty'), Length(min=3, max=30)])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired('You have to select the date')])
    file = FileField('Picture', validators=[FileRequired(),
                                            FileAllowed(['jpg', 'gif', 'png'], 'Images only!')])
    # recaptcha = RecaptchaField()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


from app import routes


def sql_init():
    con = sqlite3.connect(dbPath)
    con.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT, date TEXT, user TEXT, file TEXT,'
                'UNIQUE(file))')
    cats = [
        ('Cat Adam', '2020-03-29', 'admin', '1.jpg'),
        ('Puszek', '2020-04-02', 'admin', '2.jpg'),
        ('Fluff', '2020-04-03', 'admin', '3.jpg'),
        ('Rock', '2020-04-01', 'admin', '4.jpg'),
        ('Kitty', '2020-03-30', 'admin', '5.jpg'),
        ('Darly', '2020-03-31', 'admin', '6.jpg')
    ]
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.executemany('INSERT OR REPLACE INTO cats (name,date,user,file) '
                        'VALUES (?, ?, ?, ?)', cats)
        con.commit()
    con.close()


sql_init()

if __name__ == "__main__":
    routes.session.pop('logged_in')
    app.run(debug=True)
