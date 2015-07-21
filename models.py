#coding=utf-8
from app import db
import time
from datetime import datetime
import utils

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

def get_news_date_tipo(fecha_raw, tipo_noticia):
    tipo_cur = db.session.query(News).filter(News.date == fecha_raw, News.tipo == tipo_noticia).order_by(News.id.desc())
    tipo_news = [dict(text=row.text, tipo=row.tipo, time=time.strftime( "%I:%M %p", time.strptime(row.time, "%H:%M"))) for row in tipo_cur.all()]
    return tipo_news

def get_all_noticias(fecha_raw):
    noticias_query = db.session.query(News).filter(News.date == fecha_raw).order_by(News.id.desc())
    return noticias_query.all()

class Reportes(db.Model):
    __tablename__ = "reportes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    problema = db.Column(db.String(120))
    area = db.Column(db.String(120))
    localizacion_breve = db.Column(db.String(120))
    details = db.Column(db.Text)
    images = db.relationship("Images", cascade="all, delete-orphan")
    state = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, **kwargs):
        self.email = kwargs['email']
        self.date = datetime.now()
        self.likes = 0
        self.problema = kwargs['problema']
        self.area = kwargs['area']
        self.localizacion_breve = kwargs['localizacion_breve']
        self.details = kwargs['details']
        self.state = "Iniciado"

def get_all_reportes():
    reportes_query = db.session.query(Reportes)
    return reportes_query.all()

def get_reportes(problemas, estados, areas):
    reportes_cur = db.session.query(Reportes).order_by(Reportes.likes.desc())
    return [x for x in reportes_cur.all() if x.problema in problemas and x.state in estados and x.area in areas]

def get_reporte_by_id(el_id):
    return db.session.query(Reportes).get(int(el_id))

def get_amount_reportes_by_region():
    all_reportes = db.session.query(Reportes)
    amounts = []
    for region in utils.REGIONES:
        amounts.append(int(all_reportes.filter(Reportes.area == region).count()))
    return amounts

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

def get_user(username):
    return db.session.query(Users).filter(Users.username == username).first()

def valid_login(username, password):
    user = get_user(username)
    if user == None:
        return (False, "Usuario inválido")
    else:
        if utils.encrypt(password) == user.password:
            return (True, "")
        else:
            return (False, "Clave inválida")

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reportes.id',ondelete='CASCADE'))
    url = db.Column(db.String(120), unique=True)

    