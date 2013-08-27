# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.file import *

import Tkinter, tkFileDialog, json, sys

"""
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import Point3, Vec4, Vec3, BitMask32, NodePath, PandaNode, TextNode
from panda3d.core import PointLight, DirectionalLight, Spotlight, AmbientLight, PerspectiveLens
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay
from panda3d.core import Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomPrimitive, GeomTriangles

import direct.directbase.DirectStart
import math, os, sys, json, time
"""

class mainScene(FSM,DirectObject):
    """ #****************************
    Méthodes pour l'initialisation
    """ #****************************
    def __init__(self,app):
        FSM.__init__(self,"mainScene"); self.defaultTransitions = {"Init":["MainMenu"],"MainMenu":["SubMenu"],"SubMenu":["MainMenu"]}
        camera.setPos(0,-62,12); camera.setHpr(0,-10,0); self.accept("escape",sys.exit,[0]); self.app = app; self.version = "v0.0"
        #
        if exists(self.app.curdir+"/config.json"):
            self.app.main_config = json.loads("".join([line.rstrip().lstrip() for line in file(self.app.curdir+"/config.json","rb")]))
        else:
            #
            self.app.main_config = {"lang":[],"fullscreen":True,"lang_chx":0}
            #
            #TODO : vérifier s'il n'y a pas quelque chose à rajouter
            #
            try: mcf = open(self.app.curdir+"/config.json","w"); mcf.write(json.dumps(self.app.main_config)); mcf.close()
            except Exception,e: print e
        #
        #TODO : génération des lumières
        #
        self.activeLights()
        #
        #TODO : génération des menus
        #
        self.loadGUI()
        #
        self.dic_statics = {}; self.dic_dynamics = {}; self.loadmodels()
        #
        #TODO : écriture en 'None' des tasks et autres
        #
        self.dic_tasks = {}
        #
        #
        self.vers_txt = OnscreenText(text=self.version,font=self.app.arcFont,pos=(1.15,-0.95),fg=(0,0,0,1),bg=(1,1,1,0.8))
    def activeLights(self):
        #
        #TODO : initialiser toutes les lampes
        #
        print "activeLights method"
        #
        #
    def loadGUI(self):
        #
        #TODO : toute les interfaces sont chargées à partir de cette fonction
        #
        print "loadGUI method"
        #
        #
    def loadmodels(self):
        #
        #TODO : tout les modèles sont chargés par cette fonction
        #
        print "loadmodels method"
        #
        """
        arc_title = loader.loadModel("models/static/main_title"); arc_title.reparentTo(render)
        self.lst_decor.append(arc_title)
        """
        #
        #TODO
        #
        #
        #environnement
        tmp_mod = base.loader.loadModel("statics/main_sol"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["sol"] = tmp_mod
        tmp_mod = base.loader.loadModel("statics/main_roofs"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["roofs"] = tmp_mod
        #
        """
        self.arcs_shower = loader.loadModel("statics/main_arcs_show"); self.arcs_shower.reparentTo(render); self.arcs_shower.setPos(0,7.3,3)
        #
        #
        self.arcs_shower_hprInterv = arcs_shower.hprInterval(5,Point3(360,0,0),startHpr=Point3(0,0,0))
        #arcs_shower_pace = Sequence(arcs_shower_hprInterv,name="arcs_shower_pace")
        #
        """
        #
        #self.dic_dynamics["screens"] = None ####
        #self.dic_dynamics["persos_anims"] = None ####
        #
        #TODO : il ne manque que les écrans et les animations des personnages
        #
    """ #****************************
    Méthodes pour l'état "Init"
    """ #****************************
    def enterInit(self):
        #
        #
        #TODO : entrée dans l'état inital, avec la porte fermée
        #TODO : lancement du mouvement de caméra et de l'ouverture de la porte
        #
        #TODO : lancement des tasks
        #
        #self.arcs_shower_pace.loop()
        #
        pass
    def exitInit(self):
        #
        #TODO : clear des tasks
        #
        pass
    """ #****************************
    Méthodes pour l'état "MainMenu"
    """ #****************************
    def enterMainMenu(self):
        #
        #TODO : mise en place des captures
        #
        #TODO : affichage du menu principal, et mise en place des intéractions
        #
        pass
    def exitMainMenu(self):
        #
        #TODO : lancement de l'animation pour arriver au états correspondant aux différents sous-menus
        #
        pass
    """ #****************************
    Méthodes pour l'état "SubMenu"
    """ #****************************
    def enterSubMenu(self):
        #
        #TODO : simple affichage des différents sous-menus
        #
        #TODO : le code ci-dessous apartiendra à une méthode de cet état
        """   Tkinter open filepicker and dirpicker
        root = Tkinter.Tk(); root.withdraw()
        print tkFileDialog.askopenfilename(filetypes=[("Saves","*.save"),("All","*")])
        print tkFileDialog.askdirectory()
        """
        #
        #
        pass
    def exitSubMenu(self):
        #
        #TODO : correspond au retour au menu principal
        #
        pass
    """ #****************************
    Méthodes pour la sortie du menu principal
    """ #****************************
    def launchGame(self):
        #
        #TODO : lancement du jeu. Ce n'est pas un changement de state, c'est une exécution de méthode simple, avec des tasks
        #
        print "launchGame method"
        #
        #
        self.ignoreAll()
        #
    def close(self):
        #
        print "close method"
        #
        #TODO : ajout des dicts à effacer
        #
        for key in self.dic_statics: self.dic_statics[key].removeNode()
        for key in self.dic_dynamics: self.dic_dynamics[key].delete()
        #
        for key in self.dic_tasks: self.dic_tasks[key] = None
        #
        self.dic_statics = None; self.dic_dynamics = None; self.dic_tasks = None
        #
        self.vers_txt.removeNode()
    def __del__(self):
        print "delete mainscene"
