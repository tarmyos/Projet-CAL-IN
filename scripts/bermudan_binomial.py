import math

def binomial_bermudan_call(S, K, T, r, sigma, n, exercise_times):
    """
    Calcule le prix d'une option bermudienne Call en utilisant l'arbre binomial.

    exercise_times: Liste des fractions du temps total (entre 0 et 1) où l'option peut être exercée.
    
    Retourne le prix de l'option call.
    """
    dt = T / n  # Durée de chaque intervalle
    u = math.exp(sigma * math.sqrt(dt))  # Facteur de montée
    d = 1 / u  # Facteur de descente
    p = (math.exp(r * dt) - d) / (u - d)  # Probabilité de montée
    disc = math.exp(-r * dt)  # Facteur de discount
    
    # Convertir les fractions de temps en indices d'intervalles
    exercise_indices = [int(t * n) for t in exercise_times]
    
    # Initialisation de l'arbre des options à l'échéance
    option_tree = [[0 for _ in range(n+1)] for _ in range(n+1)]
    
    # Calcul du prix des options à l'échéance
    for i in range(n+1):
        option_tree[n][i] = max(0, S * u**i * d**(n-i) - K)
    
    # Remontée dans l'arbre pour calculer le prix de l'option
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            continuation_value = disc * (p * option_tree[i+1][j+1] + (1-p) * option_tree[i+1][j])
            intrinsic_value = S * u**j * d**(i-j) - K
            if i in exercise_indices:
                option_tree[i][j] = max(intrinsic_value, continuation_value)
            else:
                option_tree[i][j] = continuation_value
    
    return option_tree[0][0]

def binomial_bermudan_put(S, K, T, r, sigma, n, exercise_times):
    """
    Calcule le prix d'une option bermudienne Put en utilisant l'arbre binomial.

    exercise_times: Liste des fractions du temps total (entre 0 et 1) où l'option peut être exercée.
    
    Retourne le prix de l'option put.
    """
    dt = T / n  # Durée de chaque intervalle
    u = math.exp(sigma * math.sqrt(dt))  # Facteur de montée
    d = 1 / u  # Facteur de descente
    p = (math.exp(r * dt) - d) / (u - d)  # Probabilité de montée
    disc = math.exp(-r * dt)  # Facteur de discount
    
    # Convertir les fractions de temps en indices d'intervalles
    exercise_indices = [int(t * n) for t in exercise_times]
    
    # Initialisation de l'arbre des options à l'échéance
    option_tree = [[0 for _ in range(n+1)] for _ in range(n+1)]
    
    # Calcul du prix des options à l'échéance
    for i in range(n+1):
        option_tree[n][i] = max(0, K - S * u**i * d**(n-i))
    
    # Remontée dans l'arbre pour calculer le prix de l'option
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            continuation_value = disc * (p * option_tree[i+1][j+1] + (1-p) * option_tree[i+1][j])
            intrinsic_value = K - S * u**j * d**(i-j)
            if i in exercise_indices:
                option_tree[i][j] = max(intrinsic_value, continuation_value)
            else:
                option_tree[i][j] = continuation_value
    
    return option_tree[0][0]
