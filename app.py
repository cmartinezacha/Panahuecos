#coding=utf-8
###imports
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash
import utils
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
import os
from flask import send_from_directory
import sys
import json
import boto
reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG = True
SECRET_KEY = 'development key'
ACCESS_KEY = 'AKIAI72XWNTOKHIWS42Q'
SECRET_ACCESS_KEY = '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'
S3_BUCKET= 'mopresponde' #Cambiar linea dependiendo de persona
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/pre-registration'
UPLOAD_FOLDER = 'static/images/'

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

@app.template_filter('reportes_filter_state')
def reportes_filter(reportes, keyword):
    return reportes.filter(models.Reportes.state == keyword).count()

@app.template_filter('reportes_filter_problema')
def reportes_filter(reportes, keyword):
    return reportes.filter(models.Reportes.problema == keyword).count()

@app.template_filter('days_filter')
def days_filter(days):
    today_position = utils.get_today_position()
    last_seven_days = days[today_position+1:]+days[:today_position+1]
    return last_seven_days

def s3_upload(source_file, file_name, acl='public-read'):
    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["ACCESS_KEY"], app.config["SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    sml = b.new_key(file_name)
    sml.set_contents_from_string(source_file.read())
    sml.set_acl(acl)
    return 

@app.route('/')
def home():
    return redirect(url_for('show_reportes'))

@app.route('/noticias')
def today_news():
    return redirect(url_for('show_news', fecha_raw= utils.get_today()))

@app.route('/signin', methods=['POST'])
def sign_in():
    username = request.form['email']
    password = request.form['password']
    valid, error = models.valid_login(username, password)
    if valid:
        session['logged_in'] = True
        session['username'] = username
        return json.dumps({'status':'ok'})
    return json.dumps({'status':'error', 'error': error})

@app.route('/signup', methods=['POST'])
def sign_up():
    username = request.form['email']
    password = request.form['password']
    if models.get_user(username) == None:
        user = models.Users(username,utils.encrypt(password))
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['username'] = username
        return json.dumps({'status':'ok'})
    #return redirect(url_for('show_news', fecha_raw= utils.get_today()))
    return json.dumps({'status':'error','error':'Usuario ya existe'})

@app.route('/estadisticas', methods=['GET','POST'])
def show_stats():
    if request.method == 'POST':
        problema = request.form.get('problema','Todos')
        region = request.form.get('region','Todas')
        reportes = db.session.query(models.Reportes)
        if problema != "Todos":
            reportes = reportes.filter(models.Reportes.problema == problema)
        if region != "Todas":
            reportes = reportes.filter(models.Reportes.area == region)
    else:
        problema = ""
        region = ""
        reportes = db.session.query(models.Reportes)
    return render_template('estadisticas.html', reportes=reportes, problemaSeleccionado=problema, 
                            regionSeleccionada=region,
                            amounts_by_region=models.get_amount_reportes_by_region(reportes), 
                            regiones=utils.REGIONES, problemas=utils.PROBLEMAS, 
                            amounts_by_day=models.get_amount_reportes_last_seven_days(reportes),
                            amounts_completed=models.get_amount_reportes_completed(reportes))

@app.route('/agregar', methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        new = models.News("",request.form['time'],request.form['text'], utils.get_today())
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('today_news'))
    else:
        return render_template('agregar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if 'nueva_cuenta' in request.form:
            user = models.Users(request.form['username'],utils.encrypt(request.form['password']))
            db.session.add(user)
            db.session.commit()
        else:
            valid, error = models.valid_login(request.form['username'], request.form['password'])
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
    noticias = models.get_all_noticias(fecha_raw)
    return render_template('noticias.html', noticias=noticias, fecha_entera = utils.translate_day(fecha_raw), fecha_raw = fecha_raw)

@app.route('/reportes', methods=['GET', 'POST'])
def show_reportes():
    if request.method == 'POST':
        problemas_checkiados = request.form.getlist('problema')
        estados_checkiados = request.form.getlist('estado')
        regiones_checkiadas = request.form.getlist('region')
        reportes = models.get_reportes(problemas_checkiados, 
                                       estados_checkiados, 
                                       regiones_checkiadas)
    else:
        problemas_checkiados = utils.PROBLEMAS
        estados_checkiados = utils.ESTADOS
        regiones_checkiadas = utils.REGIONES
        reportes = models.get_all_reportes()
    return render_template('reportes.html', reportes=reportes, regiones=utils.REGIONES, regiones_checkiadas=regiones_checkiadas,
                                            problemas=utils.PROBLEMAS, problemas_checkiados=problemas_checkiados, 
                                            estados=utils.ESTADOS, estados_checkiados=estados_checkiados)

@app.route('/reportes/agregar', methods=['POST'])
def add_reporte():
    form = request.form
    upload = request.files['file']
    reporte = models.Reportes(email=form['email'], problema=form['problema'], area=form['area'], 
                              localizacion_breve=form['localizacion'], details=form['details'])
    db.session.add(reporte)
    db.session.flush()
    if upload.filename != "":
        filename = secure_filename(upload.filename)
        ext = filename.rsplit('.')[-1]
        url = str(reporte.id)+"_0."+ext
        new_image = models.Images(reporte_id=reporte.id, url=url)
        db.session.add(new_image)
        reporte.images.append(new_image)
        s3_upload(upload, url)
    db.session.commit()
    return redirect(url_for('show_reportes'))

@app.route('/reportes/cambiar', methods=['POST'])
def edit_reporte():
    form = request.form
    reporte = db.session.merge(models.get_reporte_by_id(int(form['id'])))
    upload = request.files['file']
    image_count = len(reporte.images)
    if upload.filename != "":
        filename = secure_filename(upload.filename)
        ext = filename.rsplit('.')[-1]
        url = str(reporte.id)+"_"+str(image_count)+"."+ext
        new_image = models.Images(reporte_id=int(form['id']), url=url)
        db.session.add(new_image)
        reporte.images.append(new_image) 
        s3_upload(upload, url)
    reporte.area = form['area']
    reporte.state = form['estado']
    reporte.problema = form['problema']
    reporte.localizacion_breve = form['localizacion']
    reporte.details = form['details']
    reporte.date_changed = utils.get_now()
    db.session.commit()
    return redirect(url_for('show_reportes'))

@app.route('/reportes/agregar-foto', methods=['POST'])
def agregar_foto():
    form = request.form
    reporte = db.session.merge(models.get_reporte_by_id(int(form['id'])))
    upload = request.files['file']
    image_count = len(reporte.images)
    filename = secure_filename(upload.filename)
    ext = filename.rsplit('.')[-1]
    url = str(reporte.id)+"_"+str(image_count)+"."+ext
    new_image = models.Images(reporte_id=int(form['id']), url=url)
    db.session.add(new_image)
    reporte.images.append(new_image) 
    s3_upload(upload, url)
    db.session.commit()
    return redirect(url_for('show_reportes'))

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
