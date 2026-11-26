# Planificateur de Trajet en Véhicule Électrique (ETRS013)

Application Web reposant sur une **Architecture Orientée Services (SOA)** permettant de planifier un itinéraire en véhicule électrique en tenant compte de l'autonomie du véhicule, du temps de trajet et des arrêts de recharge nécessaires.

* **Formation :** Université Savoie Mont Blanc (USMB) — Module ETRS013
* **Auteur :** Abdul Hamid Turkan

---

## Architecture Globale des Services

Le projet s'articule autour de 5 briques :

1. **Service SOAP (`soap_service/`) — *[Déployé]*** : Calcule le temps total de trajet (temps de conduite + recharges) et le nombre d'arrêts nécessaires à partir de la distance, de l'autonomie et de la durée de charge.
2. **Service REST — Bornes de recharge (IRVE)** : Recherche les stations de recharge disponibles à proximité des coordonnées GPS d'arrêt (OpenData Réseaux Énergies).
3. **Service REST — Cartographie & Itinéraire** : Calcule le tracé routier et génère la carte interactive (OpenRouteService / Folium).
4. **Service GraphQL — Catalogue de véhicules** : Récupère la liste des véhicules électriques et leurs caractéristiques techniques (API Chargetrip).
5. **API REST exposée** : Met à disposition un endpoint JSON permettant à une application tierce d'exploiter le service avec une autre interface.

---

## Structure du Dépôt

```text
ETRS013_Architecture_Orientes_Services/
├── README.md              # Documentation globale du projet
└── soap_service/          # Brique 1 : Service Web SOAP (Python / Spyne)
    ├── soap_service.py    # Code du serveur SOAP et définition des opérations RPC
    ├── requirements.txt   # Dépendances Python installées par la plateforme Cloud
    ├── Procfile           # Commande de démarrage du serveur sur le Cloud
    └── test.py            # Script client Zeep pour interroger le service à distance
```

---

## Hébergement Cloud & Accès au Service SOAP

### Source et infrastructure
* **Plateforme Cloud :** [Render](https://render.com) (instance Web Service gratuite).
* **Source du déploiement :** Déploiement continu connecté au dépôt GitHub `abdu2973/ETRS013_Architecture_Orientes_Services` (branche `main`, répertoire racine `soap_service/`).
* **Stack technique :** Python, Spyne (protocole SOAP 1.1) et serveur WSGI (`wsgiref`).

### Démarrage (réveil) de l'instance Cloud
L'instance gratuite Render se met automatiquement en veille après **15 minutes d'inactivité**. Pour démarrer le service avant une utilisation :
1. Ouvrir l'URL du **Descripteur WSDL** dans un navigateur (ou lancer une première requête client) afin de déclencher le réveil du conteneur.
2. Patienter **30 à 60 secondes** jusqu'à l'affichage du document XML WSDL.
3. Le service est alors actif et prêt à traiter les requêtes SOAP.

### Liens d'accès
* **Dépôt Git :** https://github.com/abdu2973/ETRS013_Architecture_Orientes_Services
* **Descripteur WSDL (Service SOAP) :** https://etrs013-architecture-orientes-services.onrender.com/?wsdl
* **Endpoint SOAP :** https://etrs013-architecture-orientes-services.onrender.com

### Exemple d'appel client (Python / Zeep)
```python
from zeep import Client
from zeep.transports import Transport

client = Client(
    '[https://etrs013-architecture-orientes-services.onrender.com/?wsdl](https://etrs013-architecture-orientes-services.onrender.com/?wsdl)',
    transport=Transport(cache=None)
)

resultat = client.service.calculer_temps_trajet(
    distance=436,
    autonomie=100,
    temps_chargement=30
)
print(resultat)  # Résultat : 7h27 (4 recharge(s))
```

---

## Exécution Locale

Pour lancer le serveur SOAP en local :

```bash
cd soap_service
pip install -r requirements.txt
python soap_service.py
```

Le descripteur WSDL local est accessible à l'adresse : `http://127.0.0.1:8000/?wsdl`.
