# -*- coding: utf-8 -*-

from direct.stdpy.file import *

import json

class arcsTools:
    def __init__(self):
        #
        # TODO : création des dictionnaires, pour éviter le chargement multiple
        #
        self.dic_mods = {}
        #

    def parse_scene(self,scene,zone):
        #
        # TODO : fonction pour parser le fichier source d'une zone
        #
        # TODO : chargement du fichier source
        #
        zone = json.loads("".join([line.rstrip().lstrip() for line in file(zone,"rb")]))
        #
        # TODO : création des lumières
        #
        #
        # TODO : vérification du chargement ou non des modèles
        #
        # TODO : chargment des modèles, et mise en mémoire
        #
        # TODO : chargement des animations
        #
    
    def parse_perso(self,perso):
        #
        # TODO : fonction pour parser le fichier source d'un personnage
        #
        pass

