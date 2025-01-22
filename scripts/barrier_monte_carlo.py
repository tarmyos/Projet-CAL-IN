import numpy as np
import math

def simulate_barrier_call(S0, K, T, r, sigma, B, n, barrier_type):
    """
    Calcule le prix d'une option barrière knock-in call avec la méthode de Monte Carlo.
    """
    # Simulation de n trajectoires de prix
    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées
    hit_barrier = np.zeros(n)  # Indicateur si la barrière a été atteinte

    # Simulation de chaque trajectoire
    for i in range(n):
        S = S0
        for t in range(1, 252):
            # Générer un mouvement brownien
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

            # Vérifier si la barrière est atteinte ou franchie
            if barrier_type == "knock-in" and S >= B:
                hit_barrier[i] = 1  # Barrière atteinte (option devient active)
                break
            elif barrier_type == "knock-out" and S >= B:
                hit_barrier[i] = -1  # Barrière franchie (option devient invalide)
                break

    # Calculer le payoff pour une option call
    payoff = np.zeros(n)
    for i in range(n):
        if hit_barrier[i] == 1:  # Barrière atteinte (option devient valide pour knock-in)
            payoff[i] = max(paths[i, -1] - K, 0)  # Payoff pour un call
        else:
            payoff[i] = 0  # Pas de payoff si la barrière n'est pas atteinte ou l'option est knock-out

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    call_price = np.mean(discounted_payoff)
    delta_call = np.std(discounted_payoff) / math.sqrt(n)

    return call_price, delta_call, discounted_payoff


def simulate_barrier_put(S0, K, T, r, sigma, B, n, barrier_type):
    """
    Calcule le prix d'une option barrière knock-in put avec la méthode de Monte Carlo.
    """
    # Simulation de n trajectoires de prix
    dt = T / 252  # Diviser l'année en jours de bourse (252 jours par an)
    paths = np.zeros((n, 252))  # Trajectoires simulées
    hit_barrier = np.zeros(n)  # Indicateur si la barrière a été atteinte

    # Simulation de chaque trajectoire
    for i in range(n):
        S = S0
        for t in range(1, 252):
            # Générer un mouvement brownien
            dW = np.random.normal(0, math.sqrt(dt))
            S = S * math.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            paths[i, t] = S

            # Vérifier si la barrière est atteinte ou franchie
            if barrier_type == "knock-in" and S >= B:
                hit_barrier[i] = 1  # Barrière atteinte (option devient active)
                break
            elif barrier_type == "knock-out" and S >= B:
                hit_barrier[i] = -1  # Barrière franchie (option devient invalide)
                break

    # Calculer le payoff pour une option put
    payoff = np.zeros(n)
    for i in range(n):
        if hit_barrier[i] == 1:  # Barrière atteinte (option devient valide pour knock-in)
            payoff[i] = max(K - paths[i, -1], 0)  # Payoff pour un put
        else:
            payoff[i] = 0  # Pas de payoff si la barrière n'est pas atteinte ou l'option est knock-out

    # Actualisation des payoffs
    discounted_payoff = np.exp(-r * T) * payoff

    # Estimation du prix de l'option
    put_price = np.mean(discounted_payoff)
    delta_put = np.std(discounted_payoff) / math.sqrt(n)

    return put_price, delta_put, discounted_payoff
