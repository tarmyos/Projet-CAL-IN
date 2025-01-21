import numpy as np
import math

def simulate_lookback_call(S0, T, r, sigma, n):

    """
    Calcule le prix d'une option call lookback avec la méthode de Monte Carlo.
    """

    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées

    for i in range(n):
        S = S0
        for t in range(1, 252):
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

    # Calcul du prix maximum atteint sur chaque trajectoire
    max_price = np.max(paths, axis=1)

    # Calculer le payoff pour une option call lookback
    payoff = np.maximum(max_price - S0, 0)

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    call_price = np.mean(discounted_payoff)
    delta_call = np.std(discounted_payoff) / math.sqrt(n)

    return call_price, delta_call


def simulate_lookback_put(S0, T, r, sigma, n):

    """
    Calcule le prix d'une option put lookback avec la méthode de Monte Carlo.
    """
    
    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées

    for i in range(n):
        S = S0
        for t in range(1, 252):
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

    # Calcul du prix minimum atteint sur chaque trajectoire
    min_price = np.min(paths, axis=1)

    # Calculer le payoff pour une option put lookback
    payoff = np.maximum(S0 - min_price, 0)

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    put_price = np.mean(discounted_payoff)
    delta_put = np.std(discounted_payoff) / math.sqrt(n)

    return put_price, delta_put
