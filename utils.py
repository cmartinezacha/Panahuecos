#coding=utf-8
from datetime import date
from datetime import datetime
from hashlib import sha256

USERNAME = 'b20b0f63ce2ed361e8845d6bf2e59811aaa06ec96bcdb92f9bc0c5a25e83c9a6'
PASSWORD = 'd1775cdbcf90d7864101da3f728d64ef357441361dc31db4d6d62cf3e34c3656'
DIA_INGLES_ESP = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", \
                          "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}
MES_INGLES_ESP = {"Jan":"Enero", "Feb":"Febrero", "Mar":"Marzo", "Apr":"Abril", \
                          "May":"Mayo", "Jun":"Junio", "Jul":"Julio","Aug":"Agosto","Sep":"Septiembre", \
                          "Oct":"Octubre","Nov":"Noviembre","Dec":"Diciembre"}
REGIONES = ['Panamá Oeste', 'Panamá Este', 'San Miguelito', 'Colón', 'Bocas del Toro',
            'Chiriquí', 'Veraguas', 'Coclé', 'Herrera', 'Los Santos', 'Darién', 'Ngobe Bugle']
TIPOS_DE_PROBLEMAS = ['Hueco', 'Cajones Pluviales', 'Alcantarilla', 'Puente', 'Otro']



def fecha_valida(fecha_raw):
    if len(fecha_raw) != 10 or len(fecha_raw.split("-")) != 3:
        return False
    return True

def translate_day(fecha_raw):
    '''Transforma un fecha en formato dd-mm-yyyy a 
    "Dia # de Mes de Año"
    '''
    fecha_entera_ingles = date(day=int(fecha_raw[0:2]), month=int(fecha_raw[3:5]), year=int(fecha_raw[6:])).strftime('%A %d %b %Y').split(' ', 3)
    fecha_entera_esp = DIA_INGLES_ESP[fecha_entera_ingles[0]] + ' '+ \
                           fecha_entera_ingles[1] + ' de '+ \
                           MES_INGLES_ESP[fecha_entera_ingles[2]] + ' de '+ \
                           fecha_entera_ingles[3]
    return fecha_entera_esp

def get_today():
    '''Regresa la fecha de hoy en formato dd-mm-yyyy'''
    today = date.today().isoformat().split("-") # regresa la fecha de hoy en formato [YYYY, MM, DD]
    today.reverse()
    return "-".join(today)

def valid_login(user, password):
    error = ""
    valid = False
    if sha256(user).hexdigest() != USERNAME:
        error = 'Usuario invalido'
    elif sha256(password).hexdigest() != PASSWORD:
        error = 'Clave invalida'
    else:
        valid = True
    return (valid, error)

