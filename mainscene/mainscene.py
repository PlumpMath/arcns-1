# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.stdpy.file import *
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3, Vec4
from panda3d.core import PointLight, DirectionalLight, Spotlight, PerspectiveLens
from direct.interval.IntervalGlobal import Sequence, Parallel

import Tkinter, tkFileDialog, json, sys, lang


class mainScene(FSM,DirectObject):
    """ #****************************
    Méthodes pour l'initialisation
    """ #****************************
    def __init__(self,app):
        FSM.__init__(self,"mainScene"); self.defaultTransitions = {"Init":["MainMenu"],"MainMenu":["SubMenu"],"SubMenu":["MainMenu"]}
        camera.setPos(0,-62,12); camera.setHpr(0,-10,0); self.accept("escape",sys.exit,[0])
        self.app = app; self.version = "v0.0"
        if exists(self.app.curdir+"/config.json"):
            self.app.main_config = json.loads("".join([line.rstrip().lstrip() for line in file(self.app.curdir+"/config.json","rb")]))
        else:
            self.app.main_config = {"fullscreen":True,"lang_chx":0}
            try: mcf = open(self.app.curdir+"/config.json","w"); mcf.write(json.dumps(self.app.main_config)); mcf.close()
            except Exception,e: print e
        self.dic_lights = {}; self.activeLights()
        if self.app.main_config["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
        elif self.app.main_config["lang_chx"] == 1: self.app.speak = lang.en.en_lang
        self.dic_gui = {"main_menu":{},"camp_menu":{},"mission_menu":{},"net_menu":{},"option_menu":{}}; self.loadGUI()
        self.dic_statics = {}; self.dic_dynamics = {}; self.loadmodels();
        self.dic_tasks = {}; self.createTasks()
        self.vers_txt = OnscreenText(text=self.version,font=self.app.arcFont,pos=(1.15,-0.95),fg=(0,0,0,1),bg=(1,1,1,0.8))
    def activeLights(self):
        tmp_node = DirectionalLight("dir_light"); tmp_node.setColor(Vec4(0.8,0.8,0.8,1))
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(0,-70,0); render.setLight(tmp_lght); self.dic_lights["dir_top"] = tmp_lght
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(-30,-10,0); render.setLight(tmp_lght); self.dic_lights["dir_right"] = tmp_lght
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(30,-10,0); render.setLight(tmp_lght); self.dic_lights["dir_left"] = tmp_lght
        tmp_node = Spotlight("spot_aux_menu"); tmp_node.setColor(Vec4(0.8,0.8,0.8,1)); lens = PerspectiveLens(); tmp_node.setLens(lens)
        tmp_lght = render.attachNewNode(tmp_node); self.dic_lights["spot_aux_menu"] = tmp_lght
        render.setLight(tmp_lght); tmp_lght.lookAt(6,-0.5,-1.5); tmp_lght.setPos(-8,0,9)
    def loadGUI(self):
        #
        #TODO : toute les interfaces sont chargées à partir de cette fonction
        #
        print "loadGUI method"
        #
        #main_menu
        #
        #TODO : a construire
        #
        #tmp_gui = 
        #
        #
        #camp_menu
        #
        #TODO : à construire
        #
        #mission_menu
        #
        #TODO : à construire
        #
        #net_menu
        #
        #TODO : à construire
        #
        #option_menu
        #
        #TODO : à construire
        #
        #
    def loadmodels(self):
        #
        #TODO : tout les modèles sont chargés par cette fonction
        #
        #
        """
        arc_title = loader.loadModel("models/static/main_title"); arc_title.reparentTo(render)
        self.lst_decor.append(arc_title)
        """
        #
        #arrows & cards
        #
        #TODO : à construire
        #
        """
        arr_up = render.attachNewNode("arrow-up"); arr_up.setHpr(0,90,0); arr_up.setPos(4.5,1.5,7); arr_up.hide()
        self.app.arrow.instanceTo(arr_up); arr_up.reparentTo(render)
        self.app.lst_arrows.append({"name":"arr_up","status":0,"node":arr_up,"posn":[4.5,1.5,7],"posh":[4.5,1.7,7.2]})
        sqp_up = render.attachNewNode(self.app.c_arr.generate()); sqp_up.hide(); sqp_up.node().setIntoCollideMask(BitMask32.bit(1))
        sqp_up.node().setTag("arrow","up"); sqp_up.reparentTo(self.app.pickly_node); sqp_up.setPos(4.5,1.5,7)
        arr_dn = render.attachNewNode("arrow-dn"); arr_dn.setHpr(180,-90,0); arr_dn.setPos(4.5,1.5,5); arr_dn.hide()
        self.app.arrow.instanceTo(arr_dn); arr_dn.reparentTo(render)
        self.app.lst_arrows.append({"name":"arr_dn","status":0,"node":arr_dn,"posn":[4.5,1.5,5],"posh":[4.5,1.7,4.8]})
        sqp_dn = render.attachNewNode(self.app.c_arr.generate()); sqp_dn.hide(); sqp_dn.node().setIntoCollideMask(BitMask32.bit(1))
        sqp_dn.node().setTag("arrow","dn"); sqp_dn.reparentTo(self.app.pickly_node); sqp_dn.setPos(4.5,1.5,5.2)
        """
        #
        #gates and moving arcs
        tmp_mod = Actor("dynamics/main_gates"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,-48.2,9.5); tmp_mod.setHpr(0,80,0); self.dic_dynamics["gates"] = tmp_mod
        tmp_mod = Actor("dynamics/main_m_menu"); tmp_mod.reparentTo(render); tmp_mod.pose("load",1); self.dic_dynamics["arcs_main_menu"] = tmp_mod
        tmp_mod = Actor("dynamics/main_a_menu"); tmp_mod.reparentTo(render); tmp_mod.pose("load",1); self.dic_dynamics["arcs_aux_menu"] = tmp_mod
        #décors
        tmp_mod = base.loader.loadModel("statics/main_sol"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["sol"] = tmp_mod
        tmp_mod = base.loader.loadModel("statics/main_roofs"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["roofs"] = tmp_mod
        tmp_mod = base.loader.loadModel("statics/main_arcs_show"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,7.3,3); self.dic_statics["arcs_shower"] = tmp_mod
        #
        tmp_mod = base.loader.loadModel("statics/main_title"); tmp_mod.reparentTo(render); self.dic_statics["arc_title"] = tmp_mod
        #
        #
        #self.dic_dynamics["screens"] = None ####
        #self.dic_dynamics["persos_anims"] = None ####
        #
        #TODO : il ne manque que les écrans et les animations des personnages
        #
    def createTasks(self):
        self.dic_tasks["arcs_shower_interval"] = self.dic_statics["arcs_shower"].hprInterval(5,Point3(360,0,0),startHpr=Point3(0,0,0))
        self.dic_tasks["arcs_shower_pace"] = Sequence(self.dic_tasks["arcs_shower_interval"],name="arcs_shower_pace")
        #
        #TODO : création des task
        #
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
        self.dic_tasks["arcs_shower_pace"].loop()
        #
        #
        self.dic_dynamics["gates"].play("open_gates")
        #
        #TODO : lancement du mouvement de la caméra, de l'init du main menu arcs, et de la requête d'enterMainMenu
        #
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
        #TEST
        self.ignoreAll()
        #TEST
        #
        #
        for key in self.dic_lights: self.dic_lights[key].removeNode()
        for key1 in self.dic_gui:
            for key2 in self.dic_gui[key1]: self.dic_gui[key1][key2].removeNode()
        for key in self.dic_statics: self.dic_statics[key].removeNode()
        for key in self.dic_dynamics: self.dic_dynamics[key].delete()
        for key in self.dic_tasks: self.dic_tasks[key] = None
        #
        #
        self.dic_statics = None; self.dic_dynamics = None; self.dic_tasks = None
        #
        self.vers_txt.removeNode()
        #
        print "end close"
        #
    def __del__(self):
        print "delete mainscene"
