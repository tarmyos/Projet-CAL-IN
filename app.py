from flask import Flask, render_template, request
import math
import numpy as np
from scripts.black_scholes import black_scholes_call

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Récupération des données du formulaire
    S = float(request.form['S'])  # Prix de l'actif sous-jacent
    K = float(request.form['K'])  # Prix d'exercice
    T = float(request.form['T'])  # Temps jusqu'à l'échéance
    r = float(request.form['r'])  # Taux d'intérêt sans risque
    sigma = float(request.form['sigma'])  # Volatilité

    # Appeler la fonction Black-Scholes pour calculer le prix de l'option
    option_price = black_scholes_call(S, K, T, r, sigma)

    # Retourner le résultat à l'utilisateur
    return render_template('index.html', result=option_price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
