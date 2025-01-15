from flask import Flask, render_template, request
from scripts.black_scholes import black_scholes_call, black_scholes_put

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

        # Calcul des prix des options
        call_price = black_scholes_call(S, K, T, r, sigma)
        put_price = black_scholes_put(S, K, T, r, sigma)

        # Retour des résultats
        return render_template('index.html', call_result=call_price, put_result=put_price)

    except ValueError:
        return render_template('index.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
