<<<<<<< HEAD
#coding=utf-8
###imports
import sqlite3
||||||| merged common ancestors
	###imports
import sqlite3
=======
#coding=utf-8
###imports
>>>>>>> d5701be62d89fab1c6468fea1f29f0e11f709d01
from flask import Flask, request, session, g, redirect, url_for, \
	              abort, render_template, flash
from contextlib import closing
from datetime import date
import locale
import time
import datetime
from hashlib import sha256
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
# Los comments con un # son los mios (Fernando), los que tienen 3 # son
# los que vinieron con el codigo.

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = sha256('admin').hexdigest()
PASSWORD = sha256('default').hexdigest()
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/pre-registration'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#heroku = Heroku(app)
db = SQLAlchemy(app)

# db.drop_all()
# db.create_all()

class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(120), unique=False)
    time = db.Column(db.String(120), unique=False)
    text = db.Column(db.String(120), unique=False)
    date = db.Column(db.String(120), unique=False)

    def __init__(self, tipo, time, text, date):
        self.tipo = tipo
        self.time = time
        self.text = text
        self.date = date
 
### The closing() function allows us to keep a connection open for the duration 
### of the with block.
### Open_resource: opens a file from the resource location, and allows
### you to read from it. 

def get_today():
	'''Regresa la fecha de hoy en formato dd-mm-yyyy'''
	today = date.today().isoformat().split("-") # regresa la fecha de hoy en formato [YYYY, MM, DD]
	today.reverse()
	return "-".join(today)

@app.route('/')
def today_news():
	return redirect(url_for('show_news', fecha_raw=get_today()))
	

@app.route('/agregar', methods=['GET','POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST':
		print "aquiii"
		new = News(request.form['type'],request.form['time'],request.form['text'],get_today())
		db.session.add(new)
		db.session.commit()
		return redirect(url_for('today_news'))
	else:
		return render_template('agregar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if sha256(request.form['username']).hexdigest() != app.config['USERNAME']:
            error = 'Usuario invalido'
        elif sha256(request.form['password']).hexdigest() != app.config['PASSWORD']:
            error = 'Clave invalida'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('add_entry'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('today_news'))
	
@app.route('/<fecha_raw>')
def show_news(fecha_raw):
	''' Renders el html con las noticias del dia especifico
		date debe estar en formato dd-mm-yyyy
	'''
	locale.setlocale(locale.LC_TIME, "es_ES")

				
	medios_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Medios")
	medios_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in medios_cur.all()]
	
	twitter_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Twitter")
	twitter_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in twitter_cur.all()]

	radio_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Radio")
	radio_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in radio_cur.all()]

	fecha_entera = date(day=int(fecha_raw[0:2]), month=int(fecha_raw[4:5]),  year=int(fecha_raw[6:10])).strftime('%A %d %B %Y')
	fecha_entera = fecha_entera.split(' ', 3)
	fecha_entera = fecha_entera[0].capitalize() + ' ' + fecha_entera[1].capitalize() + ' de ' + fecha_entera[2].capitalize() + ' de ' + fecha_entera[3].capitalize()
	return render_template('noticias.html', medios_news=medios_news, twitter_news=twitter_news, radio_news=radio_news, 
											fecha_entera=fecha_entera, fecha_raw=fecha_raw)


if __name__ == '__main__':
	app.run()
