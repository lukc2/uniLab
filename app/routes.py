import hashlib
import os
import sqlite3

from flask import render_template, redirect, url_for, session, json
from flask_login import login_user, login_required, logout_user

from app import app, dbPath, db, User, LoginForm, RegistrationForm, allowed_file, dict_factory, UploadForm

galleries_file = os.path.join(app.static_folder, 'json', 'galleries.json')

headers_file = os.path.join(app.static_folder, 'json', 'headers.json')
with open(headers_file, encoding="utf8") as head:
    headers = json.load(head)


@app.route("/")
def main():
    return render_template('index.html', title=list(headers.keys())[0],
                           header=headers[list(headers.keys())[0]][0]['name'],
                           header_i=headers[list(headers.keys())[0]][0]['icon'],
                           section=headers[list(headers.keys())[0]][1]['name'],
                           section_i=headers[list(headers.keys())[0]][1]['icon'])


@app.route("/noaccess")
def no_access():
    data = {'title': 'NO ACCESS!',
            'content': 'Website u tried to open needs higher privileges!'}
    return render_template('result.html', title=data['title'], content=data['content'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    data = {'title': 'Log in',
            'content': 'You have to be logged in to access that content'}
    form = LoginForm()
    if form.validate_on_submit():
        users = User.query.filter_by(username=form.username.data).first()
        if users:
            if users.password == hashlib.sha3_256(form.password.data.encode()).hexdigest():
                session['logged_in'] = form.username.data
                login_user(users, remember=form.remember.data)
                msg = "Login Successful!"
                return render_template('result.html', msg=msg)
        msg = "Login Failed!"
    return render_template('login.html', title=data['title'], content=data['content'], form=form, msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = {'title': 'Sign in',
            'content': 'To register fill out this form:'}
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashlib.sha3_256(form.password.data.encode()).hexdigest())
        db.session.add(new_user)
        db.session.commit()
        msg = "Registration successful! You can log in now"
        return render_template('result.html', msg=msg)
    return render_template('register.html', title=data['title'], content=data['content'], form=form)


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    session.pop('logged_in')
    return redirect(url_for('main'))


@app.route("/about")
def about_me():
    data = {'title': 'About me',
            'content': 'I am me, Łukasz Ćwiek. Nothing really to see here...'}
    return render_template('about.html', title=data['title'], content=data['content'])


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    data = {'title': 'Add cat photos!',
            'content': 'Choose data from your drive and fill out the form'}
    msg = ''
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file.filename == '':
            msg = "You have to select the file"
            return render_template('result.html', msg=msg)
        if file and allowed_file(file.filename):
            try:
                with sqlite3.connect(dbPath) as con:
                    cur = con.cursor()
                    cur.execute("SELECT MAX(rowid) AS amount from cats")
                    filename = [int(i[0]) for i in cur.fetchall()]
                    filename[0] = filename[0] + 1
                    extension = file.filename.split(".")[-1]
                    filetosave = str(filename[0]) + "." + extension
                    name = form.name.data
                    date = form.date.data.strftime('%Y-%m-%d')
                    user = session['logged_in']
                    cur.execute('INSERT INTO cats (name,date,user,file) VALUES (?, ?, ?, ?)',
                                (name, date, user, filetosave))
                    con.row_factory = dict_factory
                    cursor = con.cursor()
                    cursor.execute("select * from cats order by rowid")
                    results = cursor.fetchall()
                    with open(galleries_file, 'w', encoding='utf-8') as galry:
                        json.dump(results, galry, ensure_ascii=False, indent=4)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filetosave))
                    con.commit()
                msg = "Upload succesfull"
            except:
                con.rollback()
                msg = "Upload failed"
            con.close()
        else:
            msg = "Wrong file extension!"
        return render_template('result.html', msg=msg)

    return render_template('add.html', title=data['title'], content=data['content'], msg=msg, form=form)


@app.route("/account")
@login_required
def account():
    data = {'title': 'Welcome on your account panel',
            'content': 'Here you can see your uploaded pictures.'}
    con = sqlite3.connect(dbPath)
    con.row_factory = dict_factory
    cur = con.cursor()
    user = session['logged_in']
    cur.execute("select * from cats order by rowid")
    if user == 'admin':
        output_dict = cur.fetchall()
    else:
        list = cur.fetchall()
        output_dict = [x for x in list if (x["user"] == str(user))]
    return render_template('account.html', title=data['title'], content=data['content'], list=output_dict)


@app.errorhandler(Exception)
def error_default(e):
    return render_template('result.html', head=e.code, msg=e.name, title=e.code)
