#coding=utf-8
from app import db
import time

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

class Reportes(db.Model):
    __tablename__ = "reportes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    problema = db.Column(db.String(120), unique=False)
    area = db.Column(db.String(120))
    localizacion_breve = db.Column(db.String(120))
    details = db.Column(db.Text)
    image = db.Column(db.String(120))
    state = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, email, date, likes, problema, area, localizacion_breve, details, image, state):
        self.email = email
        self.date = date
        self.likes = 1
        self.problema = problema
        self.area = area
        self.localizacion_breve = localizacion_breve
        self.details = details
        self.state = "Iniciado"


def get_reportes(problemas, estados, areas):
    reportes_cur = db.session.query(Reportes).filter(Reportes.problema in problemas,
                                                     Reportes.state in estados,
                                                     Reportes.area in areas).order_by(Reportes.likes.desc())
    return
    