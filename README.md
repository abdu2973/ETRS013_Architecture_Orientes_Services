# Planificateur de Trajet en Véhicule Électrique (INFO802)

Application Web en **Architecture Orientée Services (SOA)** permettant de calculer un itinéraire en véhicule électrique selon son autonomie, la distance et les arrêts de recharge nécessaires.

* **Formation :** Université Savoie Mont Blanc (USMB) — Module INFO802 / ETRS013
* **Auteur :** Abdul Hamid Turkan

---

## Architecture des Services

1. **Service SOAP (`soap_service/`) — *[Déployé sur le Cloud]*** : Calcule le temps total de trajet (conduite + recharges) et le nombre d'arrêts à partir de la distance, de l'autonomie et de la durée de charge.
2. **Service REST (Bornes IRVE)** : Récupère les stations de recharge proches des points d'arrêt GPS (OpenData Réseaux Énergies).
3. **Service REST (Cartographie)** : Calcule l'itinéraire routier et affiche la carte interactive (OpenRouteService / Folium).
4. **Service GraphQL (Véhicules)** : Fournit la liste des véhicules électriques et leur autonomie (API Chargetrip).
5. **API REST exposée** : Expose un endpoint JSON permettant à un client tiers d'utiliser le calculateur avec une autre interface.

---

## Structure du Projet

```text
ETRS013_Architecture_Orientes_Services/
├── README.md              # Documentation générale du projet
└── soap_service/          # Brique 1 : Service Web SOAP
    ├── soap_service.py    # Code du serveur SOAP (Python / Spyne)
    ├── requirements.txt   # Liste des librairies Python installées automatiquement par le Cloud
    ├── Procfile           # Commande de démarrage du serveur exécutée par l'hébergeur Cloud
    └── test.py            # Script client Zeep pour tester le service à distance
```

---

## Déploiement Cloud & Accès au Service

### 1. Source et infrastructure d'hébergement
* **Hébergeur Cloud :** [Render](https://render.com) (instance Web Service gratuite).
* **Déploiement continu :** Le serveur est directement relié au dossier `soap_service/` de ce dépôt GitHub (`branche main`). À chaque mise à jour du code, Render installe les dépendances (`pip install -r requirements.txt`) et démarre le serveur (`python soap_service.py`).
* **Technologies :** Python, Spyne (protocole SOAP 1.1) et `wsgiref`.

### 2. Comment démarrer (réveiller) le service Cloud
L'instance gratuite de Render se met automatiquement en veille après **15 minutes d'inactivité**. Avant d'interroger le service depuis un client Python :
1. Clique sur le lien **Descripteur WSDL** ci-dessous pour envoyer une première requête HTTP.
2. Patienter **30 à 60 secondes** le temps que le conteneur redémarre et affiche le fichier XML WSDL dans ton navigateur.
3. Une fois le XML affiché, le serveur est actif et répond instantanément aux appels SOAP.

### 3. Liens d'accès
* **Dépôt Git du projet :** https://github.com/abdu2973/ETRS013_Architecture_Orientes_Services
* **Descripteur WSDL du service SOAP :** https://etrs013-architecture-orientes-services.onrender.com/?wsdl
* **Endpoint SOAP (URL racine) :** https://etrs013-architecture-orientes-services.onrender.com

### 4. Exemple d'appel client à distance (Python / Zeep)
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
print(resultat)  # Affiche : 7h27 (4 recharge(s))
```

---

## Exécution Locale (Tests sur PC)

Pour exécuter le serveur SOAP en local avant déploiement :

```bash
cd soap_service
pip install -r requirements.txt
python soap_service.py
```

Le WSDL local est ensuite accessible sur `http://127.0.0.1:8000/?wsdl`.
