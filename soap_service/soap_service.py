# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:13:08 2026

@author: bruhd
"""

import os
import math
from spyne import Application, rpc, ServiceBase, Float, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class TrajetService(ServiceBase):
    @rpc(Float, Float, Float, _returns=Unicode)
    def calculer_temps_trajet(ctx, distance, autonomie, temps_chargement):
        """
        Calcule le temps total d'un trajet en véhicule électrique.
        - distance : distance totale du trajet (en km)
        - autonomie : autonomie maximale du véhicule (en km)
        - temps_chargement : durée d'une recharge (en minutes)
        """
        if autonomie <= 0 or distance < 0 or temps_chargement < 0:
            return "Erreur : les valeurs doivent être positives."

        # 1. Nombre d'arrêts nécessaires (0 arrêt si distance <= autonomie, math ceil pour arrondir au supérieur, -1 car on part charger)
        nb_recharges = max(0, math.ceil(distance / autonomie) - 1)

        # 2. Temps total passé à recharger (en minutes)
        temps_recharge_total = nb_recharges * temps_chargement

        # 3. Temps de conduite estimé (sur une moyenne de 80 km/h)
        vitesse_moyenne = 80.0
        temps_conduite = (distance / vitesse_moyenne) * 60

        # 4. Conversion du total en format "XhYY"
        temps_total_min = round(temps_conduite + temps_recharge_total)
        heures = temps_total_min // 60
        minutes = temps_total_min % 60

        return f"{heures}h{minutes:02d} ({nb_recharges} recharge(s))"
    # forcer l'affichage en 7h05 au lieu de 7h5 


# Configuration de l'application SOAP 1.1 et génération du WSDL
application = Application(
    [TrajetService],
    'usmb.info802.trajet.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    # 0.0.0.0 et variable PORT pour fonctionner en local ET sur le Cloud
    port = int(os.environ.get('PORT', 8000))
    server = make_server('0.0.0.0', port, wsgi_application)
    print(f"Service SOAP démarré sur http://127.0.0.1:{port}/?wsdl")
    server.serve_forever()