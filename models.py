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