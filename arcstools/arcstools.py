# -*- coding: utf-8 -*-

from direct.stdpy.file import *

import json

class arcsTools:
    def __init__(self):
        #
        # TODO : création des dictionnaires, pour éviter le chargement multiple
        #
        self.dic_statics = {}; self.dic_dynamics = {}
        #

    def parse_scene(self,scene):
        tmp_statics = scene["statics"]; lst_statics = {}; it = 0
        for elt in tmp_statics["sol"]:
            if not self.dic_statics.has_key(elt): self.dic_statics[elt] = base.loader.loadModel(elt+".bam")
            for posrot in tmp_statics["sol"][elt]:
                tmp_inst = render.attachNewNode("sol_"+str(it)); self.dic_statics[elt].instanceTo(tmp_inst)
                tmp_inst.setPos(posrot[0]*4.8,posrot[1]*4.8,posrot[2]*4.8); tmp_inst.setHpr(posrot[3],posrot[4],posrot[5])
                tmp_inst.reparentTo(render); lst_statics["sol_"+str(it)] = tmp_inst
                it += 1
        for key in ["nord","sud","est","ouest"]:
            for elt in tmp_statics["bords"][key]:
                #
                print elt
                #
                #
                pass
            for elt in tmp_statics["murs"][key]:
                #
                print elt
                #
                #
                pass
            for elt in tmp_statics["decors"][key]:
                #
                print elt
                #
                #
                pass
        #
        # TODO : chargement des animations
        #
        #
        # TODO : création des lumières
        #
        #
        # TODO : retour de la liste des instances
        #
        print self.dic_statics
        print lst_statics
        #
        return lst_statics
        #
    
    def parse_perso(self,perso):
        #
        # TODO : fonction pour parser le fichier source d'un personnage
        #
        pass

