# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:30:59 2026

@author: bruhd
"""

from zeep import Client
from zeep.transports import Transport

client = Client(
    'https://etrs013-architecture-orientes-services.onrender.com/?wsdl',
    transport=Transport(cache=None)
)

resultat = client.service.calculer_temps_trajet(
    distance=436,
    autonomie=100,
    temps_chargement=30
)
print("Réponse Cloud :", resultat)