from flask import Flask, request, session, g, redirect, url_for, \
	              abort, render_template, flash

app = Flask(__name__)
DEBUG = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def mostrar_noticias():
	twitter_news = ["@mi abuela", "@mauidesaint", "@rmartinelli es un maricon"]
	medios_news = ["NO HAY CLASES MANANA", "Me gusta la lasagna", "quiero tomates."]
	radios_news = ["wao noventaiciete y medio"]
	# return render_template('noticias.html')
	return render_template('noticias.html', twitter_news=twitter_news, medios_news=medios_news, radios_news=radios_news)

if __name__ == '__main__':
	app.run()