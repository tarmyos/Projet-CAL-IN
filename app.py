from flask import Flask, render_template, request
from scripts.european_black_scholes import black_scholes_call, black_scholes_put
from scripts.european_propagation_incertitudes import propagation_incertitudes_call, propagation_incertitudes_put
from scripts.american_binomial import binomial_american_call, binomial_american_put
from scripts.bermudan_binomial import binomial_bermudan_call, binomial_bermudan_put
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', call_result=None, put_result=None)

@app.route('/european', methods=['GET', 'POST'])
def european():
    if request.method == 'GET':
        return render_template('european.html')
    else:
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
            return render_template('european.html', call_result=call_price, put_result=put_price, call_uncertainty=delta_call, put_uncertainty=delta_put)

        except ValueError:
            return render_template('european.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées", call_uncertainty="Erreur dans les entrées", put_uncertainty="Erreur dans les entrées")


@app.route('/american', methods=['GET', 'POST'])
def american():
    if request.method == 'GET':
        return render_template('american.html')
    else:
        try:
            # Récupération des données du formulaire
            S = float(request.form['S'])
            K = float(request.form['K'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            n = int(request.form['n'])

            # Calcul du prix de l'option américaine Call et Put
            call_price = binomial_american_call(S, K, T, r, sigma, n)
            put_price = binomial_american_put(S, K, T, r, sigma, n)

            # Retour des résultats
            return render_template('american.html', call_result=call_price, put_result=put_price)
        
        except ValueError:
            return render_template('american.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées")

@app.route('/bermudan', methods=['GET', 'POST'])
def bermudian():
    if request.method == 'GET' :
        return render_template('bermudan.html')
    else:
        try:
            # Récupération des données du formulaire
            S = float(request.form['S'])
            K = float(request.form['K'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            n = int(request.form['n'])
            exercise_times_str = request.form.getlist('exercise_times')
            exercise_times = [float(t) for t in exercise_times_str]


            # Calcul du prix de l'option bermudienne Call et Put
            call_price = binomial_bermudan_call(S, K, T, r, sigma, n , exercise_times)
            put_price = binomial_bermudan_put(S, K, T, r, sigma, n , exercise_times)

            # Retour des résultats
            return render_template('bermudan.html', call_result=call_price, put_result=put_price)
        except ValueError:
            return render_template('bermudan.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées")

@app.route('/barrier', methods=['GET'])
def barrier():
    return render_template('barrier.html')

@app.route('/asian', methods=['GET'])
def asian():
    return render_template('asian.html')

@app.route('/lookback', methods=['GET'])
def lookback():
    return render_template('lookback.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
