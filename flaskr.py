###imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	              abort, render_template, flash
from contextlib import closing
from datetime import date

# Los comments con un # son los mios (Fernando), los que tienen 3 # son
# los que vinieron con el codigo.

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

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

def get_today():
	'''Regresa la fecha de hoy en formato dd-mm-yyyy'''
	today = date.today().isoformat().split("-") # regresa la fecha de hoy en formato [YYYY, MM, DD]
	today.reverse()
	return "-".join(today)


@app.before_request
def before_request():
    '''Ni idea de que hace'''
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    '''Ni idea de que hace asumo que "cierra" el db cuando la aplicacion se cierra'''
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def today_news():
	print date.today().weekday()
	return redirect(url_for('show_news', date=get_today()))
	

@app.route('/agregar', methods=['GET','POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST':
		print request.form['time']
		g.db.execute('insert into news (text, type, time, date) values(?,?,?,?)',
					[request.form['text'], request.form['type'], request.form['time'], get_today()])
		g.db.commit()
		flash('New entry was succesfully posted')
		return redirect(url_for('today_news'))
	else:
		return render_template('agregar.html')


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
            return redirect(url_for('today_news'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('today_news'))
	
@app.route('/<date>')
def show_news(date):
	''' Renders el html con las noticias del dia especifico
		date debe estar en formato dd-mm-yyyy
	'''
	medios_cur = g.db.execute('select text, type, time from news where date = "%s" and type = "Medios" order by id desc' % date)
	medios_news = [dict(text=row[0], type=row[1], time=row[2]) for row in medios_cur.fetchall()]
	
	twitter_cur = g.db.execute('select text, type, time date from news where date = "%s" and type = "Twitter" order by id desc' % date)
	twitter_news = [dict(text=row[0], type=row[1], time=row[2]) for row in twitter_cur.fetchall()]

	radio_cur = g.db.execute('select text, type, time from news where date = "%s" and type = "Radio" order by id desc' % date)
	radio_news = [dict(text=row[0], type=row[1], time=row[2]) for row in radio_cur.fetchall()]

	return render_template('noticias.html', medios_news=medios_news, twitter_news=twitter_news, radio_news=radio_news)


if __name__ == '__main__':
	app.run()
