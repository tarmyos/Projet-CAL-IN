import math

def binomial_american_call(S, K, T, r, sigma, n):
    """
    Calcule le prix d'une option américaine Call en utilisant l'arbre binomial.

    n: Nombre d'intervalles dans l'arbre binomial (n=100 par défaut)
    
    Retourne le prix de l'option call.
    """
    # Calcul des paramètres de l'arbre binomial
    dt = T / n  # Durée de chaque intervalle
    u = math.exp(sigma * math.sqrt(dt))  # Facteur de montée
    d = 1 / u  # Facteur de descente
    p = (math.exp(r * dt) - d) / (u - d)  # Probabilité de montée
    disc = math.exp(-r * dt)  # Facteur de discount
    
    # Initialisation de l'arbre des options à l'échéance
    option_tree = [[0 for _ in range(n+1)] for _ in range(n+1)]
    
    # Calcul du prix des options à l'échéance
    for i in range(n+1):
        option_tree[n][i] = max(0, S * u**i * d**(n-i) - K)
    
    # Remontée dans l'arbre pour calculer le prix de l'option
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            option_tree[i][j] = max(S * u**j * d**(i-j) - K, disc * (p * option_tree[i+1][j+1] + (1-p) * option_tree[i+1][j]))
    
    return option_tree[0][0]


def binomial_american_put(S, K, T, r, sigma, n):
    """
    Calcule le prix d'une option américaine Put en utilisant l'arbre binomial.
    
    n: Nombre d'intervalles dans l'arbre binomial (n=100 par défaut)
    
    Retourne le prix de l'option put.
    """
    # Calcul des paramètres de l'arbre binomial
    dt = T / n  # Durée de chaque intervalle
    u = math.exp(sigma * math.sqrt(dt))  # Facteur de montée
    d = 1 / u  # Facteur de descente
    p = (math.exp(r * dt) - d) / (u - d)  # Probabilité de montée
    disc = math.exp(-r * dt)  # Facteur de discount
    
    # Initialisation de l'arbre des options à l'échéance
    option_tree = [[0 for _ in range(n+1)] for _ in range(n+1)]
    
    # Calcul du prix des options à l'échéance
    for i in range(n+1):
        option_tree[n][i] = max(0, K - S * u**i * d**(n-i))
    
    # Remontée dans l'arbre pour calculer le prix de l'option
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            option_tree[i][j] = max(K - S * u**j * d**(i-j), disc * (p * option_tree[i+1][j+1] + (1-p) * option_tree[i+1][j]))
    
    return option_tree[0][0]
