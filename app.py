#coding=utf-8
###imports

from flask import Flask, request, session, g, redirect, url_for, \
	              abort, render_template, flash
from contextlib import closing
from datetime import date
import time
import datetime
from hashlib import sha256
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
# Los comments con un # son los mios (Fernando), los que tienen 3 # son
# los que vinieron con el codigo.

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'b20b0f63ce2ed361e8845d6bf2e59811aaa06ec96bcdb92f9bc0c5a25e83c9a6'
PASSWORD = 'd1775cdbcf90d7864101da3f728d64ef357441361dc31db4d6d62cf3e34c3656'
#SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/pre-registration'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
heroku = Heroku(app)
db = SQLAlchemy(app)

# db.drop_all()
# db.create_all()

class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(120), unique=False)
    time = db.Column(db.String(120), unique=False)
    text = db.Column(db.Text, unique=False)
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

def translate_day(fecha_raw):
	'''Transforma un fecha en formato dd-mm-yyyy a 
	"Dia # de Mes de Año"
	'''
	dia_ingles_esp = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", \
						  "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}

	mes_ingles_esp = {"Jan":"Enero", "Feb":"Febrero", "Mar":"Marzo", "Apr":"Abril", \
						  "May":"Mayo", "Jun":"Junio", "Jul":"Julio","Aug":"Agosto","Sep":"Septiembre", \
						  "Oct":"Octubre","Nov":"Noviembre","Dec":"Diciembre"}

	fecha_entera_ingles = date(day=int(fecha_raw[0:2]), month=int(fecha_raw[3:5]), year=int(fecha_raw[6:])).strftime('%A %d %b %Y').split(' ', 3)
	fecha_entera_esp = dia_ingles_esp[fecha_entera_ingles[0]] + ' '+ \
						   fecha_entera_ingles[1] + ' de '+ \
						   mes_ingles_esp[fecha_entera_ingles[2]] + ' de '+ \
						   fecha_entera_ingles[3]
	return fecha_entera_esp


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
		return redirect(url_for('login'))
	if request.method == 'POST':
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
				
	medios_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Medios")
	medios_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in medios_cur.all()]
	
	twitter_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Twitter")
	twitter_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in twitter_cur.all()]

	radio_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == "Radio")
	radio_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in radio_cur.all()]

	return render_template('noticias.html', medios_news=medios_news, twitter_news=twitter_news, radio_news=radio_news, 
											fecha_entera=translate_day(fecha_raw), fecha_raw=fecha_raw)

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500

if __name__ == '__main__':
	app.run()
