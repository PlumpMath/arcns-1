# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
from direct.gui.DirectGui import DirectFrame, DGG
from panda3d.core import Point3, TextNode, BitMask32
from direct.interval.IntervalGlobal import Sequence, Parallel

import json, sys, lang, os, time, scenebuilder

class gameScene(FSM,DirectObject):
    """ ****************************
    Méthodes pour l'initialisation
    **************************** """
    def __init__(self,app):
        self.app = app; FSM.__init__(self,"gameScene")
        self.defaultTransitions = {"Init":["Base"],"Base":["Cinematic","Explore"],"Cinematic":["Base","Explore"],"Explore":["Base","Cinematic"]}
        if self.app.main_config["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
        elif self.app.main_config["lang_chx"] == 1: self.app.speak = lang.en.en_lang
        self.giroscope = render.attachNewNode("giroscope"); self.giroscope.setPos(0,0,0); self.giroscope.setHpr(0,0,0)
        self.giroHpr = [0,0,0]; self.giroPos = [0,0,0]; camera.reparentTo(self.giroscope); camera.setPos(0,-34,25); camera.lookAt(0,0,0)
        #
        self.camMove = {"strapCam":[0,0,0],"rotCam":[0,0,0]}
        #
        #
        # DEBUG : test du passage de la scène et du display
        self.accept("a",self.returnMainMenu)
        self.accept("escape",sys.exit,[0])
        ###
        #
        self.dic_gui = {"wait_visual":{},"main_visual":{},"tuto_visual":{},"base_visual":{},"explore_visual":{}}
        self.loadGUI(); self.dic_gui["wait_visual"]["frame"].show()
        self.act_place = self.app.transit["place"]; self.actscene = scenebuilder.gamescene_builder[self.act_place]
        self.type_place = 0 #0 : base; 1 : explore; 2 : cinematic
        self.dic_statics, self.dic_dynamics, self.dic_lights = self.app.arcstools.parse_scene(self.actscene,self)
        self.loadmodels(); self.dic_anims = {}; self.activeAnim()
        self.dic_sounds = {}; self.loadSfx(); self.dic_musics = {}; self.loadMusics()
        #
        # TODO : voir pour une tâche en "again" pour la gestion de la souris
        #
    # DEBUG : retour au menu principal (méthode de test)
    def returnMainMenu(self):
        taskMgr.add(self.app.main_screen,"return to main menu")
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
        #frame de chargement
        tmp_frame = DirectFrame(); self.dic_gui["wait_visual"]["frame"] = tmp_frame; tmp_frame.hide()
        tmp_gui = self.app.arcLabel(self.app.speak["wait_visual"]["titre"],(0,0,0.4),0.15,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["wait_visual"]["titre"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["wait_visual"]["waiting_text"],(0,0,0),0.1,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["wait_visual"]["waiting_text"] = tmp_gui
        #frame principale
        #
        # TODO : frame principale, présente tout le temps
        #
        tmp_frame = DirectFrame(); self.dic_gui["main_visual"]["frame"] = tmp_frame; tmp_frame.hide()
        #
        # TODO : barre de boutons pour quitter, les options, l'aide, etc
        #
        tmp_gui = self.app.arcButton(self.app.speak["main_visual"]["quit"],(-0.75,0,0.95),None,0.06,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["main_visual"]["quit"] = tmp_gui
        #
        #
        #tmp_gui = self.app.arcButton(self.app.speak["main_visual"][""],(-0.4,0,0.95),None,0.06,TextNode.ACenter)
        #tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["main_visual"][""] = tmp_gui
        #
        #
        tmp_gui = self.app.arcButton(self.app.speak["main_visual"]["option"],(0.4,0,0.95),None,0.06,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["main_visual"]["option"] = tmp_gui
        #
        #
        tmp_gui = self.app.arcButton(self.app.speak["main_visual"]["help"],(0.75,0,0.95),None,0.06,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["main_visual"]["help"] = tmp_gui
        #
        #
        #frame "tutoriel"
        #
        # TODO : frame s'affichant uniquement lors de la création d'une partie
        #
        tmp_frame = DirectFrame(); self.dic_gui["tuto_visual"]["frame"] = tmp_frame; tmp_frame.hide()
        #
        #
        #frame "base"
        #
        # TODO : frame lorsque l'unité est dans une base
        #
        tmp_frame = DirectFrame(); self.dic_gui["base_visual"]["frame"] = tmp_frame; tmp_frame.hide()
        #
        #
        #frame "explore"
        #
        # TODO : frame lorsque l'unité est sortie
        #
        tmp_frame = DirectFrame(); self.dic_gui["explore_visual"]["frame"] = tmp_frame; tmp_frame.hide()
        #
        #
    def loadmodels(self):
        tmp_mod = Actor("mainscene/models/dynamics/main_gates.bam"); tmp_mod.reparentTo(camera)
        tmp_mod.setPos(0,14,0); tmp_mod.setHpr(0,90,0); self.gates = tmp_mod
        #
        # TODO : chargement des models additionnels
        #
        #
    def activeAnim(self):
        self.cam_anim_enter = Parallel(name="cam gates enter")
        self.cam_anim_enter.append(camera.posInterval(1,Point3(0,-29,25)))
        self.cam_anim_enter.append(self.gates.posInterval(1,Point3(0,9,0)))
        self.cam_anim_exit = Parallel(name="cam gates exit")
        self.cam_anim_exit.append(camera.posInterval(1,Point3(0,-34,25)))
        self.cam_anim_exit.append(self.gates.posInterval(1,Point3(0,14,0)))
        #
        # TODO : chargement des animations
        #
        #
    def mouseTask(self,task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            #
            # TODO : capture de la souris
            #
            #
        return task.cont
    """ ****************************
    méthodes pour contrôler la caméra
    **************************** """
    def activeCamControl(self):
        self.accept("arrow_left",self.captureCamControl,["strap","left","down"])
        self.accept("arrow_left-up",self.captureCamControl,["strap","left","up"])
        self.accept("arrow_right",self.captureCamControl,["strap","right","down"])
        self.accept("arrow_right-up",self.captureCamControl,["strap","right","up"])
        self.accept("shift",self.captureCamControl,["rot","down"]); self.accept("shift-up",self.captureCamControl,["rot","up"])
        #
        # TODO : activation des contrôles de la caméra
        #
        #
        #
        pass
    def captureCamControl(self,cmd1,cmd2=None,cmd3=None):
        #
        # TODO : capture des contrôles de la caméra
        #
        print cmd1
        print cmd2
        print cmd3
        #
        pass
    def moveCam(self,task):
        #
        # TODO : gestion des contrôles de la caméra
        #
        #
        return task.cont
    """ ****************************
    méthodes pour l'état "Init"
    **************************** """
    def enterInit(self):
    	self.gates.play("open_gates"); taskMgr.doMethodLater(7,self.initTasks,"entering cam")
    	taskMgr.doMethodLater(9,self.initTasks,"change state"); self.task_chx = 0
    	self.dic_gui["wait_visual"]["frame"].hide()
    def exitInit(self):
    	pass
    def initTasks(self,task):
        if self.task_chx == 0:
            self.cam_anim_enter.start(); self.task_chx = 1
        elif self.task_chx == 1: self.request("Base")
        return task.done
    """ ****************************
    méthodes pour l'état "Base"
    **************************** """
    def enterBase(self):
    	self.app.change_cursor("main"); self.dic_gui["main_visual"]["frame"].show()
    	#
    	# TODO : etat pour afficher une base (enterBase)
    	#
    	self.activeCamControl()
    	#
    	#
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
    def delete_actscene(self):
        for key in self.dic_anims:
            try: self.dic_anims[key].finish()
            except: pass
            self.dic_anims[key] = None
        for key in self.dic_lights:
        	render.clearLight(self.dic_lights[key]); self.dic_lights[key].removeNode()
        for key in self.dic_statics: self.dic_statics[key].removeNode()
        for key in self.dic_dynamics: self.dic_dynamics[key].delete()
        self.dic_statics = None; self.dic_dynamics = None; self.dic_anims = None
    def close(self):
        self.ignoreAll();
        #
        #taskMgr.remove(self.mouse_task); self.mouse_task = None
        #
        for key in self.dic_sounds:
            self.dic_sounds[key].stop(); self.dic_sounds[key] = None
        for key in self.dic_musics:
            self.dic_musics[key].stop(); self.dic_musics[key] = None
        for key1 in self.dic_gui:
            for key2 in self.dic_gui[key1]:
                for t in self.dic_gui[key1][key2].options():
                    if t[0] == "command":
                        self.dic_gui[key1][key2]["command"] = None; break
                self.dic_gui[key1][key2].removeNode()
        self.dic_sounds = None; self.dic_musics = None
        #
        # TODO : suppression des éléments non classés
        #
        self.giroscope.removeNode(); self.gates.delete()
        try:
            self.cam_anim_enter.finish(); self.cam_anim_exit.finish()
        except: pass
        del self.cam_anim_exit; del self.cam_anim_enter
        #
    # DEBUG : cette méthode n'aura plus d'utilité une fois le code de ce fichier terminé
    def __del__(self):
    	print "delete gamescene"
    ###

