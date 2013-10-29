# -*- coding: utf-8 -*-

from panda3d.core import DirectionalLight, Spotlight, PerspectiveLens, Vec4
from direct.stdpy.file import *

import json

class arcsTools:
    def __init__(self):
        self.dir_light = DirectionalLight("dir_light"); self.dir_light.setColor(Vec4(0.8,0.8,0.8,1))
        self.spot_light = Spotlight("spotlight"); self.spot_light.setColor(Vec4(0.8,0.8,0.8,1))
        lens = PerspectiveLens(); self.spot_light.setLens(lens)
        #
        # TODO : création des dictionnaires, pour éviter le chargement multiple
        #
        self.dic_statics = {}; self.dic_dynamics = {}
        #

    def parse_scene(self,scene,parent=None):
        tmp_statics = scene["statics"]; lst_statics = {}; it = 0
        for elt in tmp_statics["sol"]:
            if not self.dic_statics.has_key(elt): self.dic_statics[elt] = base.loader.loadModel(elt+".bam")
            for posrot in tmp_statics["sol"][elt]:
                tmp_inst = render.attachNewNode("sol_"+str(it)); self.dic_statics[elt].instanceTo(tmp_inst)
                tmp_inst.setPos(posrot[0][0]*4.8,posrot[0][1]*4.8,posrot[0][2]*4.8); tmp_inst.setHpr(posrot[1][0],posrot[1][1],posrot[1][2])
                tmp_inst.reparentTo(render); lst_statics["sol_"+str(it)] = tmp_inst
                #
                # TODO : génération de la carte si besoin
                #
                # TODO : voir pour le navigational mesh ici
                #
                it += 1
        for key in ["nord","sud","est","ouest"]:
            for elt in tmp_statics["bords"][key]:
                #
                print elt
                #
                if key == "nord":
                    #
                    #
                    pass
                elif key == "sud":
                    #
                    #
                    pass
                elif key == "est":
                    #
                    #
                    pass
                elif key == "ouest":
                    #
                    #
                    pass
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
        tmp_dynamics = scene["dynamics"]; lst_dynamics = {}
        #
        for elt in tmp_dynamics:
            #
            #
            #
            pass
        #
        #
        tmp_lights = scene["lights"]; lst_lights = {}
        for lght in tmp_lights:
            tmp_lght = None
            if lght[0] == 0:
                tmp_lght = render.attachNewNode(self.spot_light)
                tmp_lght.lookAt(lght[2][0],lght[2][1],lght[2][2]); tmp_lght.setPos(lght[1][0],lght[1][1],lght[1][2])
            elif lght[0] == 1:
                tmp_lght = render.attachNewNode(self.dir_light); tmp_lght.setHpr(lght[2][0],lght[2][1],lght[2][2])
            if lght[3]:
                if lght[4] != None: lght[4].setLight(tmp_lght)
                else: render.setLight(tmp_lght)
            lst_lights[lght[5]] = tmp_lght
        #
        #
        #
        return lst_statics, lst_dynamics, lst_lights
    
    def parse_perso(self,perso):
        #
        # TODO : fonction pour parser le fichier source d'un personnage
        #
        pass

