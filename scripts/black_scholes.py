import math
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    Calcule le prix d'une option call selon la formule de Black-Scholes.
    
    S: Prix de l'actif sous-jacent
    K: Prix d'exercice
    T: Temps jusqu'à l'échéance (en années)
    r: Taux d'intérêt sans risque
    sigma: Volatilité
    """
    # Calcul des paramètres d1 et d2
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    # Calcul du prix de l'option call
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price
