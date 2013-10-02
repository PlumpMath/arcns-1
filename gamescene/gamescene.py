# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
#
from panda3d.core import Point3, Vec4, DirectionalLight
#
from direct.interval.IntervalGlobal import Sequence, Parallel

import sys, lang

class gameScene(FSM,DirectObject):
    """ ****************************
    Méthodes pour l'initialisation
    **************************** """
    def __init__(self,app):
        self.app = app; FSM.__init__(self,"gameScene")
        self.defaultTransitions = {"Init":["Base","Cinematic"],"Base":["Cinematic","Explore"],"Cinematic":["Base","Explore"],"Explore":["Base","Cinematic"]}
        #
        # TODO : positionnement de la caméra
        #
        print "init du gameScene FSM"
        #
        # DEBUG : test du passage de la scène et du display
        self.accept("a",self.app.main_screen)
        self.accept("escape",sys.exit,[0])
        #
        self.tmp_mod = base.loader.loadModel("mainscene/models/statics/main_arcs_show")
        self.tmp_mod.reparentTo(render)
        #
        tmp_node = DirectionalLight("test_dir_light"); tmp_node.setColor(Vec4(0.8,0.8,0.8,1))
        self.tmp_lght = render.attachNewNode(tmp_node); self.tmp_lght.setHpr(0,-70,0); render.setLight(self.tmp_lght)
        #
        #
        #
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
    	#
    	# TODO : clean de l'objet avant sa suppression
    	#
    	# TODO : vérifier s'il y a des persoscene actives, et les cloturer avant de passer à la suite
    	#
    	print "close method"
    	#
    	self.ignoreAll()
    	#
    	# DEBUG : nettoyage des tests
    	self.tmp_mod.removeNode()
    	render.clearLight(self.tmp_lght); self.tmp_lght.removeNode()
    	###
    	#
    	#
    def __del__(self):
    	print "delete gamescene"

