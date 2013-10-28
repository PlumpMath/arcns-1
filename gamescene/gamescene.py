# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
from panda3d.core import Point3
from direct.interval.IntervalGlobal import Sequence, Parallel

import json, sys, lang, os, time, scenebuilder

class gameScene(FSM,DirectObject):
    """ ****************************
    Méthodes pour l'initialisation
    **************************** """
    def __init__(self,app):
        self.app = app; FSM.__init__(self,"gameScene")
        self.defaultTransitions = {"Init":["Base","Cinematic"],"Base":["Cinematic","Explore"],"Cinematic":["Base","Explore"],"Explore":["Base","Cinematic"]}
        if self.app.main_config["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
        elif self.app.main_config["lang_chx"] == 1: self.app.speak = lang.en.en_lang
        #
        self.giroscope = render.attachNewNode("giroscope"); self.giroscope.setPos(0,0,0); self.giroscope.setHpr(0,0,0)
        #
        self.giroHpr = [0,0,0]
        #
        camera.reparentTo(self.giroscope); camera.setPos(0,-30,25); camera.lookAt(0,0,0)
        #
        # TODO : chargement des portes
        #
        #
        # DEBUG : test du passage de la scène et du display
        self.accept("a",self.returnMainMenu)
        self.accept("escape",sys.exit,[0])
        #
        self.accept("arrow_left",self.rotate_giro,[1])
        self.accept("arrow_right",self.rotate_giro,[-1])
        #
        ###
        #
        self.act_place = self.app.transit["place"]; self.actscene = scenebuilder.gamescene_builder[self.act_place]
        #
        self.dic_statics, self.dic_dynamics, self.dic_lights = self.app.arcstools.parse_scene(self.actscene,self)
        #
        self.loadmodels()
        #
        self.dic_gui = {}
        #
        self.dic_sounds = {}
        #
        self.dic_musics = {}
        #
        # DEBUG : test de l'appel pour la création d'une persoscene
        perso = self.app.crea_persoscene()
        ###
        #
        #
    # DEBUG : retour au menu principal (méthode de test)
    def returnMainMenu(self):
        taskMgr.add(self.app.main_screen,"return to main menu")
    ###
    # DEBUG : rotation du giroscope (méthode de test)
    def rotate_giro(self,sens):
        self.giroHpr[0] += 15*sens; self.giroscope.setHpr(self.giroHpr[0],self.giroHpr[1],self.giroHpr[2])
    ###
    def loadSfx(self):
        #
        # TODO : chargement des sons
        #
        pass
    def loadMusics(self):
        #
        # TODO : chargement des musiques
        #
        pass
    def loadGUI(self):
        #
        # TODO : chargement de l'interface GUI
        #
        pass
    def loadmodels(self):
        #
        # TODO : chargement des models additionnels
        #
        tmp_mod = Actor("mainscene/models/dynamics/main_gates.bam"); tmp_mod.reparentTo(camera)
        #
        tmp_mod.setPos(0,10,0); tmp_mod.setHpr(0,90,0); self.dic_dynamics["gates"] = tmp_mod
        #
        #
    """ ****************************
    méthodes pour contrôler la caméra
    **************************** """
    def activeCamControl(self):
        #
        # TODO : activation des contrôles de la caméra
        #
        pass
    def moveCam(self):
        #
        # TODO : gestion des contrôles de la caméra
        #
        pass
    """ ****************************
    méthodes pour l'état "Init"
    **************************** """
    def enterInit(self):
    	#
    	# TODO : méthode d'entrée dans l'état "Init" du gamescene
    	#
    	#
    	print "enterInit"
    	#
    def exitInit(self):
    	#
    	# TODO : méthode pour sortir de l'état "Init"
    	#
    	print "exitInit"
    	#
    	pass
    """ ****************************
    méthodes pour l'état "Base"
    **************************** """
    def enterBase(self):
    	#
    	# TODO : etat pour afficher une base (enterBase)
    	#
    	pass
    def exitBase(self):
    	#
    	# TODO : méthode de sortie de l'état "Base"
    	#
    	pass
    """ ****************************
    méthodes pour l'état "Cinematic"
    **************************** """
    def enterCinematic(self):
    	#
    	# TODO : méthode d'entrée dans l'état "Cinematic"
    	#
    	print "Cinematic state entering"
    	#
    def exitCinematic(self):
    	#
    	# TODO : moéthde de sortie de l'état "Cinematic"
    	#
    	print "Cinematic state exiting"
    	#
    """ ****************************
    méthodes pour l'état "Explore"
    **************************** """
    def enterExplore(self):
    	#
    	# TODO : méthode d'entrée dans l'état "Explore"
    	#
    	print "Explore state entering"
    	#
    def exitExplore(self):
    	#
    	# TODO : méthode de sortie de l'état "Explore"
    	#
    	print "Explore state exiting"
    	#
    """ ****************************
    méthodes pour la sortie de la scène de jeu
    **************************** """
    def close(self):
        self.ignoreAll();  taskMgr.remove(self.mouse_task); self.mouse_task = None
        #
        """
        for key in self.dic_anims:
            try: self.dic_anims[key].finish()
            except: pass
            self.dic_anims[key] = None
        """
        #
        for key in self.dic_lights:
        	render.clearLight(self.dic_lights[key]); self.dic_lights[key].removeNode()
        for key1 in self.dic_gui:
            for key2 in self.dic_gui[key1]:
                for t in self.dic_gui[key1][key2].options():
                    if t[0] == "command":
                        self.dic_gui[key1][key2]["command"] = None; break
                self.dic_gui[key1][key2].removeNode()
        for key in self.dic_statics: self.dic_statics[key].removeNode()
        for key in self.dic_dynamics: self.dic_dynamics[key].delete()
        for key in self.dic_sounds:
            self.dic_sounds[key].stop(); self.dic_sounds[key] = None
        for key in self.dic_musics:
            self.dic_musics[key].stop(); self.dic_musics[key] = None
        self.dic_statics = None; self.dic_dynamics = None; self.dic_anims = None
        self.dic_sounds = None; self.dic_musics = None
        #
        # TODO : suppression des éléments non classés
        #
        self.giroscope.removeNode()
        #
    # DEBUG : cette méthode n'aura plus d'utilité une fois le code de ce fichier terminé
    def __del__(self):
    	print "delete gamescene"
    ###

