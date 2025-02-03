from flask import Flask, render_template, request
import numpy as np
from scripts.european_black_scholes import black_scholes_call, black_scholes_put
from scripts.european_propagation_incertitudes import propagation_incertitudes_call, propagation_incertitudes_put
from scripts.american_binomial import binomial_american_call, binomial_american_put
from scripts.bermudan_binomial import binomial_bermudan_call, binomial_bermudan_put
from scripts.barrier_monte_carlo import simulate_barrier_call, simulate_barrier_put
from scripts.asian_monte_carlo import simulate_asian_call, simulate_asian_put
from scripts.lookback_monte_carlo import simulate_lookback_call, simulate_lookback_put
from scripts.graph_monte_carlo import graph_call, graph_put
from scripts.graph_black_scholes import generate_black_scholes_graphs
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', call_result=None, put_result=None)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'logo_CAL-IN.png', mimetype='image/png')

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
            #dS = float(request.form['dS'])
            dS = 0
            #dK = float(request.form['dK'])
            dK = 0
            dT = float(request.form['dT'])
            dr = float(request.form['dr'])
            dSigma = float(request.form['dSigma'])

            # Type d'option
            option_type = request.form['optionType']

            # Calcul des prix des options et de leurs incertitudes associées
            call_price, delta_call = propagation_incertitudes_call(S, K, T, r, sigma, dS, dK, dT, dr, dSigma)
            put_price, delta_put = propagation_incertitudes_put(S, K, T, r, sigma, dS, dK, dT, dr, dSigma)

           #  Arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)
            delta_call = np.round(delta_call, 2)
            delta_put = np.round(delta_put, 2)

            # Générer les graphiques des options Call et Put
            graph_url_call, graph_url_put = generate_black_scholes_graphs(S, K, T, r, sigma)

            # Retour des résultats
            return render_template('european.html', call_result=call_price, put_result=put_price, 
                                   call_uncertainty=delta_call, put_uncertainty=delta_put, 
                                   graph_url_call=graph_url_call, graph_url_put=graph_url_put, option_type=option_type, S=S, K=K)

        except ValueError:
            return render_template('european.htl', call_result="Erreur dans les entrées", 
                                   put_result="Erreur dans les entrées", 
                                   call_uncertainty="Erreur dans les entrées", 
                                   put_uncertainty="Erreur dans les entrées")


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

            # Type d'option
            option_type = request.form['optionType']

            # Calcul du prix de l'option américaine Call et Put
            call_price = binomial_american_call(S, K, T, r, sigma, n)
            put_price = binomial_american_put(S, K, T, r, sigma, n)

            # arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)

            # Retour des résultats
            return render_template('american.html', call_result=call_price, put_result=put_price,
                                    option_type=option_type, S=S, K=K)
        
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

            # Type d'option
            option_type = request.form['optionType']

            # Calcul du prix de l'option bermudienne Call et Put
            call_price = binomial_bermudan_call(S, K, T, r, sigma, n , exercise_times)
            put_price = binomial_bermudan_put(S, K, T, r, sigma, n , exercise_times)

            # arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)

            # Retour des résultats
            return render_template('bermudan.html', call_result=call_price, put_result=put_price,
                                   option_type=option_type, S=S, K=K)
        except ValueError:
            return render_template('bermudan.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées")

@app.route('/barrier', methods=['GET', 'POST'])
def barrier():
    if request.method == 'GET' :
        return render_template('barrier.html')
    else:
        try:
            # Récupération des données du formulaire
            S = float(request.form['S'])
            K = float(request.form['K'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            B = float(request.form['B'])
            n = int(request.form['n'])
            barrier_type = request.form['btype']
            
            # Type d'option
            option_type = request.form['optionType']

            # Calcul du prix de l'option bermudienne Call et Put
            call_price, delta_call, call_discounted_payoff = simulate_barrier_call(S, K, T, r, sigma, B, n, barrier_type)
            put_price, delta_put, put_discounted_payoff = simulate_barrier_put(S, K, T, r, sigma, B, n, barrier_type)

            # arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)
            delta_call = np.round(delta_call, 2)
            delta_put = np.round(delta_put, 2)

            # Générer les graphiques des trajectoires Monte Carlo
            call_graph = graph_call(call_discounted_payoff)
            put_graph = graph_put(put_discounted_payoff)

            # Retour des résultas
            return render_template('barrier.html', call_result=call_price, call_uncertainty=delta_call,
                                    put_result=put_price, put_uncertainty=delta_put, call_graph=call_graph,
                                    put_graph=put_graph, option_type=option_type, S=S, K=K)
        except ValueError:
            return render_template('barrier.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées")

@app.route('/asian', methods=['GET', 'POST'])
def asian():
    if request.method == 'GET':
        return render_template('asian.html')
    else:
        try:
            # Récupération des données du formulaire
            moyenne_type = request.form['moyenne_type']
            S = float(request.form['S'])
            K = float(request.form['K'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            n = int(request.form['n'])

            # Type d'option
            option_type = request.form['optionType']

            # Calcul du prix de l'option asiatique Call et Put
            call_price, delta_call,call_discounted_payoff = simulate_asian_call(S, K, T, r, sigma, n, moyenne_type)
            put_price, delta_put,put_discounted_payoff = simulate_asian_put(S, K, T, r, sigma, n, moyenne_type)

            # arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)
            delta_call = np.round(delta_call, 2)
            delta_put = np.round(delta_put, 2)

            # Générer les graphiques des trajectoires Monte Carlo
            call_graph = graph_call(call_discounted_payoff)
            put_graph = graph_put(put_discounted_payoff)

            # Retour des résultats
            return render_template('asian.html',moyenne_type=moyenne_type, call_result=call_price,
                                    put_result=put_price, call_uncertainty=delta_call,
                                    put_uncertainty=delta_put, call_graph=call_graph,
                                    put_graph=put_graph, option_type=option_type, S=S, K=K)
        except ValueError:
            return render_template('asian.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées", call_uncertainty="Erreur dans les entrées", put_uncertainty="Erreur dans les entrées")

@app.route('/lookback', methods=['GET', 'POST'])
def lookback():
    if request.method == 'GET':
        return render_template('lookback.html')
    else:
        try:
            # Récupération des données du formulaire
            S = float(request.form['S'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            n = int(request.form['n'])

            # Type d'option
            option_type = request.form['optionType']

            # Calcul du prix de l'option lookback Call et Put
            call_price, delta_call, call_discounted_payoff = simulate_lookback_call(S, T, r, sigma, n)
            put_price, delta_put, put_discounted_payoff = simulate_lookback_put(S, T, r, sigma, n)

            # arrondir les résultats au deuxième chiffre après la virgule
            call_price = np.round(call_price, 2)
            put_price = np.round(put_price, 2)
            delta_call = np.round(delta_call, 2)
            delta_put = np.round(delta_put, 2)

            # Générer les graphiques des trajectoires Monte Carlo
            call_graph = graph_call(call_discounted_payoff)
            put_graph = graph_put(put_discounted_payoff)

            # Retour des résultats
            return render_template('lookback.html', call_result=call_price, put_result=put_price,
                                    call_uncertainty=delta_call, put_uncertainty=delta_put,
                                    call_graph=call_graph, put_graph=put_graph, option_type=option_type,
                                    S=S, K=K)
        except ValueError:
            return render_template('lookback.html', call_result="Erreur dans les entrées", put_result="Erreur dans les entrées", call_uncertainty="Erreur dans les entrées", put_uncertainty="Erreur dans les entrées")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
