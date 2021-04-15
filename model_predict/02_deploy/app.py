import os
import pandas as pd 
import numpy as np 
import flask
import pickle
from flask import Flask, render_template, request, jsonify

app=Flask(__name__)


@app.route("/test", methods=["GET"])
def ping():
    """
    Metodo para probar que la app esté funcionando correctamente.
    Ejecución: http://host:port/test
    """
    return jsonify({"response": "Running..."})


@app.route('/')
def index():
    """
    Metodo para acceder a la portada inicial de la app.
    Ejecución: http://host:port
    """ 
    return flask.render_template('index.html')

def ValuePredictor(to_predict_list):
    """
    Función que carga el modelo previamente entrenado y obtiene la predicción de los nuevos datos
    """
    to_predict = np.array(to_predict_list).reshape(1,2)
    loaded_model = pickle.load(open('model.pkl','rb'))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ['POST'])
def result():
    """
    Metodo para capturar los parametros de entrada y retornar el resultado de la predicción.
    Ejecución: Se ejecuta desde un FORM HTML en la página templates/index.html
    """
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
		
        if result == 1:
            prediction = "Compra"
        else:
            prediction = "No Compra"

        return render_template('index.html', prediction=prediction)



@app.route('/predict/params')
def result_params():
    """
    Metodo para calcular una predicción pasando los valores como parámetros en la URL y 
    retorna un JSON con el resultado.
    Ejecución: http://127.0.0.1:5000/predict/params?edad=XX&salario=YYYYY
    """
    args = request.args
    edad = args.get("edad")
    salario = args.get("salario")

    result = ValuePredictor([int(edad), int(salario)])
    if result == 1:
        prediction = "Compra"
    else:
        prediction = "No Compra"

    return jsonify({"prediccion": prediction})
	

if __name__ == '__main__':
	app.run(debug=True)