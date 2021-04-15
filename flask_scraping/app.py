import flask
from flask import Flask, render_template, request, jsonify

import requests
import bs4
from bs4 import BeautifulSoup

app=Flask(__name__)


@app.route('/')
def index():
	"""
	Metodo para acceder a la portada inicial de la app.
	Ejecución: http://host:port
	""" 
	return flask.render_template('index.html')



def buscar(articulo):
	"""
	Metodo para buscar el precio de un articulo 
	"""
	url = "https://listado.mercadolibre.com.co/"+articulo

	#conducting a request of the stated URL above:
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")

	lst_articulo = []
	for div in soup.find_all(name="div", attrs={"class":"ui-search-result__content-wrapper"}):
		titulo = div.find("h2", attrs={"class":"ui-search-item__title"}).text
		precio = div.find("span", attrs={"class":"price-tag-fraction"}).text

		lst_articulo.append([titulo, precio])

	return lst_articulo


@app.route('/consultar', methods = ['POST'])
def result():
	"""
	Metodo para buscar el precio de un articulo 
	"""
	if request.method == 'POST':	# cambiarlo a GET!!!
		result = buscar(request.form["articulo"])
		
		return render_template('index.html', items=result)


if __name__ == '__main__':
	app.run(debug=True)
