# Planificateur de Trajet en Véhicule Électrique (INFO802)

Application Web basée sur une **Architecture Orientée Services (SOA)** permettant de planifier un itinéraire en véhicule électrique en tenant compte de l'autonomie du véhicule, du temps de trajet et des arrêts de recharge nécessaires.

* **Formation :** Université Savoie Mont Blanc (USMB) — Module INFO802 / ETRS013
* **Auteur :** Abdul Hamid Turkan

---

## Architecture des Services

L'application repose sur l'orchestration de 5 services :

1. **Service SOAP (`soap_service/`) — *[En cours de déploiement]***
   * Calcul du temps total de trajet (conduite + recharges) et du nombre d'arrêts nécessaires à partir de la distance, de l'autonomie et du temps de chargement.
2. **Service REST — Bornes de recharge (IRVE)**
   * Localisation des stations de recharge disponibles à proximité des points d'arrêt GPS (OpenData Réseaux Énergies).
3. **Service REST — Cartographie & Itinéraire**
   * Calcul du tracé routier et affichage interactif sur carte (OpenRouteService / Folium).
4. **Service GraphQL — Catalogue de véhicules**
   * Récupération des modèles de véhicules électriques et de leurs caractéristiques techniques (API Chargetrip).
5. **API REST exposée**
   * Mise à disposition d'un endpoint JSON permettant à un client tiers d'exploiter le calculateur avec une autre interface.

---

## Structure du Projet

```text
info802-trajet-ve/
├── README.md
└── soap_service/          # Brique 1 : Service Web SOAP (Python / Spyne)
    ├── soap_service.py
    ├── requirements.txt
    └── Procfile
