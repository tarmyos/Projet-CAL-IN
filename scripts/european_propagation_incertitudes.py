import math
from scipy.stats import norm
from scripts.black_scholes import black_scholes_call, black_scholes_put

def propagation_incertitudes_call(S, K, T, r, sigma, dS, dK, dT, dr, dSigma):
    """
    Calcule l'incertitude associée d'une option call en utilisant la propagation des erreurs.
    """
    call_price, d1, d2 = black_scholes_call(S, K, T, r, sigma)
    
    # Dérivées partielles 
    dCall_dS = norm.cdf(d1)  
    dCall_dK = -math.exp(-r * T) * norm.cdf(d2)
    dCall_dr = -K * T * math.exp(-r * T) * norm.cdf(d2)
    dCall_dSigma = S * math.sqrt(T) * (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * d1**2)
    dCall_dT = -S * math.sqrt(T) * (1 / (2 * math.sqrt(2 * math.pi))) * math.exp(-0.5 * d1**2)
    
    # Propagation des incertitudes pour l'option call
    delta_call = math.sqrt( (dCall_dS * dS)**2 + (dCall_dK * dK)**2 + (dCall_dr * dr)**2 + (dCall_dSigma * dSigma)**2 + (dCall_dT * dT)**2)
    
    return call_price, delta_call

def propagation_incertitudes_put(S, K, T, r, sigma, dS, dK, dT, dr, dSigma):
    """
    Calcule l'incertitude associée d'une option put en utilisant la propagation des erreurs.
    """
    put_price, d1, d2 = black_scholes_put(S, K, T, r, sigma)
    
    # Dérivées partielles pour l'option put
    dPut_dS = -norm.cdf(-d1)
    dPut_dK = math.exp(-r * T) * norm.cdf(-d2)
    dPut_dr = K * T * math.exp(-r * T) * norm.cdf(-d2)
    dPut_dSigma = -S * math.sqrt(T) * (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * d1**2)
    dPut_dT = S * math.sqrt(T) * (1 / (2 * math.sqrt(2 * math.pi))) * math.exp(-0.5 * d1**2)
    
    # Propagation des incertitudes pour l'option put
    delta_put = math.sqrt((dPut_dS * dS)**2 + (dPut_dK * dK)**2 + (dPut_dr * dr)**2 + (dPut_dSigma * dSigma)**2 + (dPut_dT * dT)**2)
    
    return put_price, delta_put