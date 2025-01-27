import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scripts.european_black_scholes import black_scholes_call, black_scholes_put

# Fonction pour générer les graphiques des options Call et Put avec leur PnL
def generate_black_scholes_graphs(S0, K, T, r, sigma):
    # Vérification que tous les paramètres sont positifs
    if S0 <= 0 or K <= 0 or T <= 0 or r <= 0 or sigma <= 0:
        raise ValueError("Erreur: Tous les paramètres doivent être positifs.")

    # Plage des prix de l'actif sous-jacent de 0 à 2*S0
    S_values = list(range(1, int(2 * K) + 1))  # Plage plus large pour éviter de petits échantillons
        
    # Calcul du prix initial de l'option Call et Put
    call_price_initial = black_scholes_call(S0, K, T, r, sigma)[0]
    put_price_initial = black_scholes_put(S0, K, T, r, sigma)[0]
        
    # Calcul des prix et du PnL pour l'option Call
    call_prices = [black_scholes_call(S, K, T, r, sigma)[0] for S in S_values]
    call_pnls = [max(S - K, 0) - call_price_initial for S in S_values]

    # Calcul des prix et du PnL pour l'option Put
    put_prices = [black_scholes_put(S, K, T, r, sigma)[0] for S in S_values]
    put_pnls = [max(K - S, 0) - put_price_initial for S in S_values]

    # --- Graphique pour l'Option Call ---
    plt.figure(figsize=(8, 6))
    plt.plot(S_values, call_prices, label='Option Call', color='blue')
    plt.plot(S_values, call_pnls, label='PnL Call', color='green', linestyle='--')
    plt.title("Option Call et PnL (Black-Scholes)")
    plt.xlabel("Prix de l'actif sous-jacent (S)")
    plt.ylabel("Valeur de l'option / PnL")
    plt.legend()
    plt.grid(True)

    # Sauvegarder l'image du graphique Call dans un buffer
    img_call = BytesIO()
    plt.savefig(img_call, format='png')
    img_call.seek(0)
    graph_url_call = base64.b64encode(img_call.getvalue()).decode('utf8')

    # --- Graphique pour l'Option Put ---
    plt.figure(figsize=(8, 6))
    plt.plot(S_values, put_prices, label='Option Put', color='red')
    plt.plot(S_values, put_pnls, label='PnL Put', color='orange', linestyle='--')
    plt.title("Option Put et PnL (Black-Scholes)")
    plt.xlabel("Prix de l'actif sous-jacent (S)")
    plt.ylabel("Valeur de l'option / PnL")
    plt.legend()
    plt.grid(True)

    # Sauvegarder l'image du graphique Put dans un buffer
    img_put = BytesIO()
    plt.savefig(img_put, format='png')
    img_put.seek(0)
    graph_url_put = base64.b64encode(img_put.getvalue()).decode('utf8')

    return graph_url_call, graph_url_put
