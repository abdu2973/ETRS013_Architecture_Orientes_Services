# Planificateur de Trajet en Véhicule Électrique (ETRS013)

Application Web en **Architecture Orientée Services (SOA)** permettant de calculer un itinéraire en véhicule électrique selon son autonomie, la distance et les arrêts de recharge nécessaires.

* **Formation :** Université Savoie Mont Blanc (USMB) — Module ETRS013
* **Auteur :** Abdul Hamid Turkan

---

## Architecture des Services

1. **Service SOAP (`soap_service/`) — *[En cours]*** : Calcule le temps total de trajet (conduite + recharges) et le nombre d'arrêts.
2. **Service REST (Bornes IRVE)** : Récupère les stations de recharge proches des points d'arrêt GPS (OpenData Réseaux Énergies).
3. **Service REST (Cartographie)** : Calcule l'itinéraire routier et affiche la carte interactive (OpenRouteService / Folium).
4. **Service GraphQL (Véhicules)** : Fournit la liste des véhicules électriques et leur autonomie (API Chargetrip).
5. **API REST exposée** : Expose un endpoint JSON permettant à un client tiers d'utiliser le calculateur avec une autre interface.

---

## Structure du Projet

```text
info802-trajet-ve/
├── README.md              # Documentation générale du projet
└── soap_service/          # Brique 1 : Service Web SOAP
    ├── soap_service.py    # Code du serveur SOAP (Python / Spyne)
    ├── requirements.txt   # Liste des librairies Python à installer automatiquement sur le Cloud
    └── Procfile           # Commande de démarrage du serveur exécutée par l'hébergeur Cloud
```

---

## Exécution Locale (Tests sur PC)

Permet de faire tourner et valider le service sur sa propre machine avant de le mettre en ligne sur le Cloud :

```bash
cd soap_service
pip install -r requirements.txt   # Installe les dépendances si elles ne sont pas déjà sur le PC
python soap_service.py            # Démarre le serveur SOAP en local
```

Une fois lancé, le descripteur **WSDL** est accessible sur : `http://127.0.0.1:8000/?wsdl`

---

## Déploiement Cloud

* **URL de l'application / WSDL :** *À compléter*
