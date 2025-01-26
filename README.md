## Projet-CAL-IN

# prérequis:

-installer flask

pip install flask

-cloner le projet

git clone https://github.com/tarmyos/Projet-CAL-IN.git
# structure du projet
  
PROJET-CAL-IN/
  
│  
├── app.py                                      # Point d'entrée principal  
│  
├── templates/                                  # Contient les fichiers HTML  
│   └── index.html                              # page d'accueil  
│   └── european.html                           # Page calcul d'options européennes  
│   └── american.html                           # Page calcul d'options américaines  
│   └── bermudan.html                           # Page calcul d'options bermudiennes  
│   └── barrier.html                            # Page calcul d'options barrières  
│   └── asian.html                              # Page calcul d'options asiatiques  
│   └── lookback.html                           # Page calcul d'options lookback  
│  
├── static/                                     # Contient les fichiers CSS, JS, img, etc.  
│   └── style.css                               # Fichier CSS pour le style  
│  
├── scripts/                                    # Contient les scripts Python  
│   └── european_black_scholes.py               # Black Scholes option européenne (call/put)  
│   └── european_propagation_incertitudes.py    # Propagation des incertitudes Black Scholes  
│   └── graph_black_scholes                     # Créer et affiche graphiques (options et PnL)/S  
│   └── american_binomial.py                    # Loi binominale pour option americaine (call/put)  
│   └── bermudan_binomial.py                    # Loi binominale pour option bermudienne (call/put)  
│   └── barrier_monte_carlo.py                  # Simulation monte carlo option barrier (call/put)  
│   └── asian_monte_carlo.py                    # Simulation monte carlo option asiatique (call/put)  
│   └── lookback_monte_carlo.py                 # Simulation monte carlo option lookback (call/put)  
│   └── graph_monte_carlo.py                    # Créer et affiche le graphique de l'option (call/put)  
│  
└── README.md                                   # Documentation du projet  


# Lancer l'application (en local)

Se placer dans le dossier /PROJET-CALIN/ puis lancer avec la commande: 

python app.py



Normalement l'application démarre sur le port 8080 :

http://127.0.0.1:8080 adapter avec mon code  reercrie mpi ca avec le graphql

console de debuggage en mode développement sur :

 http://127.0.0.1:8080/console (en donnant le code PIN affiché dans le terminal qui a lancé app.py)
