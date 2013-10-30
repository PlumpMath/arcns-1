# -*- coding: utf-8 -*-

from panda3d.core import DirectionalLight, Spotlight, PerspectiveLens, Vec4
from direct.stdpy.file import *
from direct.gui.DirectGui import DirectFrame, DGG

import json

class arcsTools:
    def __init__(self,app):
        self.app = app
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
                spot_light = Spotlight("spotlight"); spot_light.setColor(Vec4(lght[1][0],lght[1][1],lght[1][2],lght[1][3]))
                lens = PerspectiveLens(); spot_light.setLens(lens); tmp_lght = render.attachNewNode(spot_light)
                tmp_lght.lookAt(lght[3][0],lght[3][1],lght[3][2]); tmp_lght.setPos(lght[2][0],lght[2][1],lght[2][2])
            elif lght[0] == 1:
                dir_light = DirectionalLight("dir_light"); dir_light.setColor(Vec4(lght[1][0],lght[1][1],lght[1][2],lght[1][3]))
                tmp_lght = render.attachNewNode(dir_light); tmp_lght.setHpr(lght[3][0],lght[3][1],lght[3][2])
            if lght[4]:
                if lght[5] != None: lght[5].setLight(tmp_lght)
                else: render.setLight(tmp_lght)
            lst_lights[lght[6]] = tmp_lght
        #
        #
        #
        return lst_statics, lst_dynamics, lst_lights
    
    def parse_perso(self,perso):
        #
        # TODO : fonction pour parser le fichier source d'un personnage
        #
        pass

    def parse_gui(self,gui):
        lst_gui = {}
        for key1 in gui:
            lst_gui[key1] = {}
            for key2 in gui[key1]:
                lst_gui[key1][key2] = DirectFrame()
                if gui[key1][key2]["parent"] != None: lst_gui[key1][key2].reparentTo(gui[key1][key2]["parent"])
                if gui[key1][key2]["hide"]: lst_gui[key1][key2].hide()
                for elt in gui[key1][key2]["elts"]:
                    tmp = gui[key1][key2]["elts"][elt]; tmp_gui = None
                    if tmp["type"] == "button":
                        tmp_text = (tmp["text"] if tmp.has_key("text") else self.app.speak[key1][elt])
                        tmp_gui = self.app.arcButton(tmp_text,tmp["pos"],tmp["cmd"],tmp["scale"],tmp["algn"],tmp["extra"],tmp["sound"])
                        if tmp.has_key("disabled") and not tmp["disabled"]: pass
                        else: tmp_gui["state"] = DGG.DISABLED
                    elif tmp["type"] == "label":
                        tmp_text = (tmp["text"] if tmp.has_key("text") else self.app.speak[key1][elt])
                        tmp_gui = self.app.arcLabel(tmp_text,tmp["pos"],tmp["scale"],tmp["algn"])
                    elif tmp["type"] == "radio":
                        for sub in tmp["elts"]:
                            sub.append(sub[0]); sub[0] = self.app.speak[key1][sub[0]]
                        self.app.arcRadioButton(tmp["elts"],lst_gui[key1][key2],lst_gui[key1],tmp["scale"],tmp["algn"])
                        continue
                    elif tmp["type"] == "optmenu":
                        tmp_text = (tmp["text"] if tmp.has_key("text") else self.app.speak[key1][elt])
                        tmp_gui = self.app.arcOptMenu(tmp_text,tmp["pos"],tmp["items"],tmp["init"],tmp["cmd"],tmp["scale"],tmp["change"],tmp["algn"],tmp["extra"])
                    elif tmp["type"] == "checkbox":
                        tmp_gui = self.app.arcCheckButton(self.app.speak[key1][elt],tmp["pos"],tmp["cmd"],tmp["val"],tmp["scale"],tmp["box"],tmp["algn"],tmp["extra"])
                    elif tmp["type"] == "slider":
                        tmp_gui = self.app.arcSlider(tmp["pos"],tmp["scale"],tmp["inter"],tmp["init"],tmp["pas"],tmp["cmd"],tmp["extra"],tmp["orient"])
                    elif tmp["type"] == "waitbar":
                        #
                        tmp_text = (tmp["text"] if tmp.has_key("text") else self.app.speak[key1][elt])
                        tmp_gui = self.app.arcWaitBar(tmp["pos"],tmp["scale"],tmp["range"],tmp["val"],tmp_text)
                        #
                        #
                    #
                    #
                    tmp_gui.reparentTo(lst_gui[key1][key2]); lst_gui[key1][elt] = tmp_gui
                    if tmp["hide"]: tmp_gui.hide()
        return lst_gui

