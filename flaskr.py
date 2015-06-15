###imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	              abort, render_template, flash
from contextlib import closing

# Los comments con un # son los mios (Fernando), los que tienen 3 # son
# los que vinieron con el codigo.



###configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

###start
app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

init_db()
 
### The closing() function allows us to keep a connection open for the duration 
### of the with block.
### Open_resource: opens a file from the resource location, and allows
### you to read from it. 


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_news():
	cur = g.db.execute('select text, type from news order by id desc')
	news = [dict(text=row[0], type=row[1]) for row in cur.fetchall()]
	return render_template('show_news.html', news=news)


@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into news (text, type) values(?,?)',
				[request.form['text'], request.form['type']])
	g.db.commit()
	flash('New entry was succesfully posted')
	return redirect(url_for('show_news'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_news'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_news'))
			


if __name__ == '__main__':
	app.run()
