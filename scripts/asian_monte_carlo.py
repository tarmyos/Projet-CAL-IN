import numpy as np
import math

def simulate_asian_call(S0, K, T, r, sigma, n, moyenne_type):
    """
    Calcule le prix d'une option call asiatique avec la méthode de Monte Carlo.
    """
    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées

    for i in range(n):
        S = S0
        for t in range(1, 252):
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

    # Calcul de la moyenne des prix sur chaque trajectoire
    if moyenne_type == 'arithmétique':
        average_price = np.mean(paths, axis=1)
    else:
        average_price = np.exp(np.mean(np.log(paths + 1e-10), axis=1)) # éviter log(0) avec une petite valeur ajoutée

    # Calculer le payoff pour une option call asiatique
    payoff = np.maximum(average_price - K, 0)

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    call_price = np.mean(discounted_payoff)
    delta_call = np.std(discounted_payoff) / math.sqrt(n)

    return call_price, delta_call


def simulate_asian_put(S0, K, T, r, sigma, n, moyenne_type):
    """
    Calcule le prix d'une option put asiatique avec la méthode de Monte Carlo.
    """
    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées

    for i in range(n):
        S = S0
        for t in range(1, 252):
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

    # Calcul de la moyenne des prix sur chaque trajectoire
    if moyenne_type == 'arithmétique':
        average_price = np.mean(paths, axis=1)
    else:
        average_price = np.exp(np.mean(np.log(paths + 1e-10), axis=1)) # éviter log(0) avec une petite valeur ajoutée

    # Calculer le payoff pour une option put asiatique
    payoff = np.maximum(K - average_price, 0)

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    put_price = np.mean(discounted_payoff)
    delta_put = np.std(discounted_payoff) / math.sqrt(n)

    return put_price, delta_put
