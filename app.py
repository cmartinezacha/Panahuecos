#coding=utf-8
###imports
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash
import utils

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

DEBUG = True
SECRET_KEY = 'development key'
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/pre-registration'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
heroku = Heroku(app)
db = SQLAlchemy(app)

import models

@app.template_filter('datetime')
def datetime_filter(date_time):
    temp = date_time.strftime('%b %-d - %-I:%M%p').split(" ")
    return " ".join([utils.MES_INGLES_ESP[temp[0]]]+temp[1:])

@app.route('/')
def today_news():
    return redirect(url_for('show_news', fecha_raw= utils.get_today()))
    
@app.route('/agregar', methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        new = models.News(request.form['type'],request.form['time'],request.form['text'], utils.get_today())
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('today_news'))
    else:
        return render_template('agregar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        valid, error = utils.valid_login(request.form['username'], request.form['password'])
        if valid:
            session['logged_in'] = True
            return redirect(url_for('add_entry'))            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('today_news'))
    
@app.route('/<fecha_raw>')
def show_news(fecha_raw):
    ''' Renders el html con las noticias del dia especifico date debe estar en formato dd-mm-yyyy '''

    if not utils.fecha_valida(fecha_raw):
        abort(404)
    medios_news = models.get_news_date_tipo(fecha_raw, "Medios")
    twitter_news = models.get_news_date_tipo(fecha_raw, "Twitter")
    radio_news = models.get_news_date_tipo(fecha_raw, "Radio")
    return render_template('noticias.html', medios_news = medios_news, twitter_news = twitter_news, radio_news = radio_news, 
                                            fecha_entera = utils.translate_day(fecha_raw), fecha_raw = fecha_raw)

@app.route('/reportes', methods=['GET', 'POST'])
def show_reportes():
    if request.method == 'POST':
        form = request.form
        reporte = models.Reportes(email=form['email'], problema=form['problema'], area=form['area'], 
                                  localizacion_breve=form['localizacion'], details=form['details'])
        db.session.add(reporte)
        db.session.commit()
    else:
        checkboxes = "todos"

    return render_template('reportes.html', reportes=models.get_all_reportes(), regiones=utils.REGIONES,
                                            problemas=utils.TIPOS_DE_PROBLEMAS)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
