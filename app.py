from flask import Flask, render_template, request
from scripts.black_scholes import black_scholes_call, black_scholes_put
from scripts.propagation_incertitudes import propagation_incertitudes_call, propagation_incertitudes_put

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', call_result=None, put_result=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Récupération des données du formulaire
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])

        # Incertitudes
        dS = float(request.form['dS'])
        dK = float(request.form['dK'])
        dT = float(request.form['dT'])
        dr = float(request.form['dr'])
        dSigma = float(request.form['dSigma'])


        # Calcul des prix des options et de leurs incertitudes associées
        call_price, delta_call = propagation_incertitudes_call(S, K, T, r, sigma, dS, dK, dT, dr, dSigma)
        put_price, delta_put = propagation_incertitudes_put(S, K, T, r, sigma, dS, dK, dT, dr, dSigma)

        # Retour des résultats
        return render_template('index.html', call_result=call_price, put_result=put_price, call_uncertainty=delta_call, put_uncertainty=delta_put)

    except ValueError:
        return render_template('index.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées", call_uncertainty="Erreur dans les entrées", put_uncertainty="Erreur dans les entrées")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
