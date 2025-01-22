import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI environments
import matplotlib.pyplot as plt
import base64
import io

def graph_call(discounted_payoff):
    """
    Génère un graphique pour la moyenne des prix simulés (Call).
    
    Arguments :
    - discounted_payoff : Liste ou tableau contenant les valeurs des payoffs actualisés pour le Call.
    
    Retourne :
    - Une image encodée en base64 du graphique.
    """
    plt.figure(figsize=(10, 6))

    # Calculer la moyenne cumulative des payoffs
    moyenne_cumulative = [sum(discounted_payoff[:i+1]) / (i+1) for i in range(len(discounted_payoff))]

    # Tracer la courbe
    plt.plot(moyenne_cumulative, label="Moyenne cumulée (Call)", color="blue")

    plt.xlabel("Simulation")
    plt.ylabel("Prix moyen actualisé")
    plt.title("Moyenne cumulée des payoffs actualisés - Option Call")
    plt.legend(loc="upper right")
    plt.grid(alpha=0.3)

    # Sauvegarder le graphique dans un buffer en mémoire
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return encoded_image

def graph_put(discounted_payoff):
    """
    Génère un graphique pour la moyenne des prix simulés (Put).
    
    Arguments :
    - discounted_payoff : Liste ou tableau contenant les valeurs des payoffs actualisés pour le Put.
    
    Retourne :
    - Une image encodée en base64 du graphique.
    """
    plt.figure(figsize=(10, 6))

    # Calculer la moyenne cumulative des payoffs
    moyenne_cumulative = [sum(discounted_payoff[:i+1]) / (i+1) for i in range(len(discounted_payoff))]

    # Tracer la courbe
    plt.plot(moyenne_cumulative, label="Moyenne cumulée (Put)", color="red")

    plt.xlabel("Simulation")
    plt.ylabel("Prix moyen actualisé")
    plt.title("Moyenne cumulée des payoffs actualisés - Option Put")
    plt.legend(loc="upper right")
    plt.grid(alpha=0.3)

    # Sauvegarder le graphique dans un buffer en mémoire
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return encoded_image
