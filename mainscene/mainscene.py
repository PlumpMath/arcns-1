# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DGG
from direct.stdpy.file import *
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3, Vec4, CardMaker, PointLight, DirectionalLight, Spotlight, PerspectiveLens, BitMask32
from direct.interval.IntervalGlobal import Sequence, Parallel

import Tkinter, tkFileDialog, json, sys, lang

class mainScene(FSM,DirectObject):
    """ ****************************
    Méthodes pour l'initialisation
    **************************** """
    def __init__(self,app):
        FSM.__init__(self,"mainScene"); self.defaultTransitions = {"Init":["MainMenu"],"MainMenu":["SubMenu"],"SubMenu":["MainMenu"]}
        camera.setPos(0,-62,12); camera.setHpr(0,-10,0); self.accept("escape",sys.exit,[0])
        self.app = app; self.version = "v0.0"; self.nomove = False
        if exists(self.app.curdir+"/config.json"):
            self.app.main_config = json.loads("".join([line.rstrip().lstrip() for line in file(self.app.curdir+"/config.json","rb")]))
        else:
            self.app.main_config = {"fullscreen":True,"lang_chx":0}
            try:
            	mcf = open(self.app.curdir+"/config.json","w"); mcf.write(json.dumps(self.app.main_config)); mcf.close()
            except Exception,e: print e
        self.dic_lights = {}; self.activeLights()
        if self.app.main_config["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
        elif self.app.main_config["lang_chx"] == 1: self.app.speak = lang.en.en_lang
        #
        self.cust_path = ("" if base.appRunner else "mainscene/models/")
        #
        # DEBUG : self.states n'est pas encore validé, il pourrait changer
        self.states = {"main_chx":0,"main_lst":[]}
        ###
        #
        # DEBUG : commande pour les tests
        self.accept("d",self.app.game_screen)
        ###
        #
        #
        self.dic_gui = {"main_menu":{},"camp_menu":{},"mission_menu":{},"maj_menu":{},"option_menu":{}}; self.loadGUI()
        self.dic_arrows= {}; self.dic_statics = {}; self.dic_dynamics = {}; self.loadmodels();
        self.dic_anims = {}; self.activeAnim()
        self.vers_txt = OnscreenText(text=self.version,font=self.app.arcFont,pos=(1.15,-0.95),fg=(0,0,0,1),bg=(1,1,1,0.8))
        #
        #
        self.mouse_task = taskMgr.add(self.mouseTask,"mainscene mouse task")
    def activeLights(self):
        tmp_node = DirectionalLight("dir_light"); tmp_node.setColor(Vec4(0.8,0.8,0.8,1))
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(0,-70,0); render.setLight(tmp_lght); self.dic_lights["dir_top"] = tmp_lght
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(-30,-10,0); render.setLight(tmp_lght); self.dic_lights["dir_right"] = tmp_lght
        tmp_lght = render.attachNewNode(tmp_node); tmp_lght.setHpr(30,-10,0); render.setLight(tmp_lght); self.dic_lights["dir_left"] = tmp_lght
        tmp_node = Spotlight("spot_aux_menu"); tmp_node.setColor(Vec4(0.8,0.8,0.8,1)); lens = PerspectiveLens(); tmp_node.setLens(lens)
        tmp_lght = render.attachNewNode(tmp_node); self.dic_lights["spot_aux_menu"] = tmp_lght
        render.setLight(tmp_lght); tmp_lght.lookAt(6,-0.5,-1.5); tmp_lght.setPos(-8,0,9)
    def loadGUI(self):
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["main_menu"]["frame"] = tmp_frame
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["campaign"],(-0.15,0,-0.2),self.actionMainMenu,scale=0.12)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["campaign"] = tmp_gui; self.states["main_lst"].append("campaign")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["mission"],(-0.19,0,-0.34),self.actionMainMenu,scale=0.1)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["mission"] = tmp_gui; self.states["main_lst"].append("mission")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["maj"],(-0.26,0,-0.47),self.actionMainMenu,scale=0.09)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["maj"] = tmp_gui; self.states["main_lst"].append("maj")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["options"],(-0.35,0,-0.58),self.actionMainMenu,scale=0.07)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["options"] = tmp_gui; self.states["main_lst"].append("options")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["quit"],(-0.41,0,-0.66),self.actionMainMenu,scale=0.05)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["quit"] = tmp_gui; self.states["main_lst"].append("quit")
        #
        # DEBUG : zone de création d'éléments gui temporaires
        #tmp_gui
        ###
        #
        #camp_menu
        #
        tmp_frame = DirectFrame()#; tmp_frame.hide()
        #
        self.dic_gui["camp_menu"]["frame"] = tmp_frame
        #
        #
        # TODO : éléments gui pour le camp_menu à construire ici
        #
        #mission_menu
        #
        # TODO : éléments gui pour le mission_menu à construire ici
        #
        #maj_menu
        #
        # TODO : éléments gui pour le maj_menu à construire ici
        #
        #option_menu
        #
        # TODO : éléments gui pour le option_menu à construire ici
        #
        #
    def loadmodels(self):
        #arrows & cards
        arr_up = render.attachNewNode("main arrow up"); arr_up.setHpr(0,90,0); arr_up.setPos(4.5,1.5,7); arr_up.hide()
        self.app.arrow_mod.instanceTo(arr_up); arr_up.reparentTo(render)
        arr_up_crd = render.attachNewNode(self.app.card_arrow.generate()); arr_up_crd.node().setIntoCollideMask(BitMask32.bit(1)); arr_up_crd.hide()
        arr_up_crd.node().setTag("arrow","mainup"); arr_up_crd.reparentTo(self.app.pickly_node); arr_up_crd.setPos(4.5,1.7,7)
        self.dic_arrows["arrow_up"] = {"node":arr_up,"card":arr_up_crd,"status":0,"posn":[4.5,1.5,7],"posh":[4.5,1.7,7.2]}
        arr_dn = render.attachNewNode("main arrow down"); arr_dn.setHpr(180,-90,0);  arr_dn.setPos(4.5,1.5,5); arr_dn.hide()
        self.app.arrow_mod.instanceTo(arr_dn); arr_dn.reparentTo(render)
        arr_dn_crd = render.attachNewNode(self.app.card_arrow.generate()); arr_dn_crd.node().setIntoCollideMask(BitMask32.bit(1)); arr_dn_crd.hide()
        arr_dn_crd.node().setTag("arrow","maindn"); arr_dn_crd.reparentTo(self.app.pickly_node); arr_dn_crd.setPos(4.5,1.7,5.2)
        self.dic_arrows["arrow_dn"] = {"node":arr_dn,"card":arr_dn_crd,"status":0,"posn":[4.5,1.5,5],"posh":[4.5,1.7,4.8]}
        #
        # TODO : flèches pour les différents sous-menus à construire ici
        #
        #gates and moving arcs
        tmp_mod = Actor(self.cust_path+"dynamics/main_gates"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,-48.2,9.5); tmp_mod.setHpr(0,80,0); self.dic_dynamics["gates"] = tmp_mod
        tmp_mod = Actor(self.cust_path+"dynamics/main_m_menu"); tmp_mod.reparentTo(render)
        tmp_mod.pose("load",1); self.dic_dynamics["arcs_main_menu"] = tmp_mod
        tmp_mod = Actor(self.cust_path+"dynamics/main_a_menu"); tmp_mod.reparentTo(render)
        tmp_mod.pose("load",1); self.dic_dynamics["arcs_aux_menu"] = tmp_mod
        #décors
        tmp_mod = base.loader.loadModel(self.cust_path+"statics/main_sol"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["sol"] = tmp_mod
        tmp_mod = base.loader.loadModel(self.cust_path+"statics/main_roofs"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["roofs"] = tmp_mod
        tmp_mod = base.loader.loadModel(self.cust_path+"statics/main_arcs_show"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,7.3,3); self.dic_statics["arcs_shower"] = tmp_mod
        #
        tmp_mod = base.loader.loadModel(self.cust_path+"statics/main_title"); tmp_mod.reparentTo(render); self.dic_statics["arc_title"] = tmp_mod
        #
        #
        #self.dic_dynamics["screens"] = None ####
        #self.dic_dynamics["persos_anims"] = None ####
        #
        # TODO : il ne manque que les écrans et les animations des personnages
        #
    def activeAnim(self):
        tmp_anim = self.dic_statics["arcs_shower"].hprInterval(5,Point3(360,0,0),startHpr=Point3(0,0,0))
        self.dic_anims["arcs_shower_pace"] = Sequence(tmp_anim,name="arcs_shower_pace")
        self.dic_anims["cam_move_init"] = camera.posInterval(4,Point3(0,-25,12))
        #
        # TODO : suite des animations à charger
        #
        #
    def mouseTask(self,task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.app.pickerRay.setFromLens(base.camNode,mpos.getX(),mpos.getY())
            self.app.mouse_trav.traverse(self.app.pickly_node)
            if self.app.mouse_hand.getNumEntries() > 0 and self.nomove:
                if self.state == "MainMenu":
                    tag = self.app.mouse_hand.getEntry(0).getIntoNode().getTag("arrow")
                    nod = None
                    if tag == "mainup": nod = self.dic_arrows["arrow_up"]
                    elif tag == "maindn": nod = self.dic_arrows["arrow_dn"]
                    if not nod == None:
                        nod["status"] = 2; nod["node"].setPos(nod["posh"][0],nod["posh"][1],nod["posh"][2])
                elif self.state == "subMenu":
                    #
                    # TODO :gestion des flèches lorsque l'un des sous-menus est activé
                    #
                    pass
            elif self.nomove:
                for key in self.dic_arrows:
                    if self.dic_arrows[key]["status"] == 2:
                        self.dic_arrows[key]["status"] = 1
                        self.dic_arrows[key]["node"].setPos(self.dic_arrows[key]["posn"][0],self.dic_arrows[key]["posn"][1],self.dic_arrows[key]["posn"][2])
        return task.cont
    """ ****************************
    Méthodes pour l'état "Init"
    **************************** """
    def enterInit(self):
        self.dic_anims["arcs_shower_pace"].loop(); self.dic_dynamics["gates"].play("open_gates")
        self.task_chx = 0; taskMgr.doMethodLater(6.5,self.initTasks,"cam movement")
        taskMgr.doMethodLater(9,self.initTasks,"play arcs_main_menu load anim")
        taskMgr.doMethodLater(11,self.initTasks,"request for the next state")
    def exitInit(self):
        pass
    def initTasks(self,task):
        if self.task_chx == 0: #moving camera
            self.dic_anims["cam_move_init"].start(); self.task_chx += 1
        elif self.task_chx == 1: #launch arcs_m_menu animation
            self.dic_dynamics["arcs_main_menu"].play("load"); self.task_chx += 1
        elif self.task_chx == 2: self.request("MainMenu")
        return task.done
    """ ****************************
    Méthodes pour l'état "MainMenu"
    **************************** """
    def enterMainMenu(self):
        self.app.change_cursor("main"); self.dic_gui["main_menu"]["frame"].show(); self.nomove = True
        #
        # TODO : système de gestion des arrows, pour savoir lesquels ils faut afficher
        #
        if self.states["main_chx"] < 4: self.dic_arrows["arrow_up"]["node"].show()
        if self.states["main_chx"] > 0: self.dic_arrows["arrow_dn"]["node"].show()
        #
        self.dic_arrows["arrow_up"]["status"] = 1; self.dic_arrows["arrow_dn"]["status"] = 1
        #
        #
        self.dic_gui["main_menu"][self.states["main_lst"][self.states["main_chx"]]]["state"] = DGG.NORMAL
        #capture de la souris
        self.accept("mouse1",self. actionMainMenu,["click"])
        self.accept("wheel_up",self.actionMainMenu,["up"])
        self.accept("wheel_down",self.actionMainMenu,["down"])
        #capture du clavier
        self.accept("arrow_up",self.actionMainMenu,["up"])
        self.accept("arrow_down",self.actionMainMenu,["down"])
        self.accept("enter",self.actionMainMenu,["valid"])
    def exitMainMenu(self):
        pass
    def actionMainMenu(self,value):
        if not self.nomove: return
        if value == "click":
            #
            # TODO : click de la souris
            #
            #value = "valid"
            #
            pass
        if value == "down":
            if self.states["main_chx"] > 0:
                #
                # TODO : animation de la descente du menu principal
                #
                self.nomove = False
                #
            else: return
        elif value == "up":
            if self.states["main_chx"] < 4:
                #
                # TODO : montée du menu principal
                #
                self.nomove = False
                #
            else: return
        elif value == "valid":
            #
            # TODO : validation du menu principal
            #
            for key in self.states["main_lst"]: self.dic_gui["main_menu"][key]["state"] = DGG.DISABLED
            #
            print "validation"
            #
            self.ignoreAll(); self.accept("escape",sys.exit,[0]); self.nomove = False
            #
        #
    """ ****************************
    Méthodes pour l'état "SubMenu"
    **************************** """
    def enterSubMenu(self):
        #
        # TODO : simple affichage des différents sous-menus
        #
        pass
    def exitSubMenu(self):
        #
        # TODO : retour au menu principal depuis un sous-menu
        #
        pass
    def actionSubMenu(self,value):
        #
        # TODO : actions possibles pour l'état "SubMenu"
        #
        #self.ignoreAll(); self.accept("escape",sys.exit,[0])
        #
        # NOTE : code pour l'import et l'export
        """   Tkinter open filepicker and dirpicker
        root = Tkinter.Tk(); root.withdraw()
        print tkFileDialog.askopenfilename(filetypes=[("Saves","*.save"),("All","*")])
        print tkFileDialog.askdirectory()
        """
        #
        pass
    """ ****************************
    Méthodes pour la sortie du menu principal
    **************************** """
    def launchGame(self):
        #
        # TODO : lancement du jeu. Ce n'est pas un changement de state, c'est une exécution de méthode simple, avec des tasks
        #
        # TODO : animation de sortie du menu principal
        #
        print "launchGame method"
        #
        self.ignoreAll(); self.accept("escape",sys.exit,[0])
        #
        # TODO : lancement de la task pour lancer game_screen dans main.py, et changer de FSM / scene
        #
        # TODO : remplissage de la variable de transition
        #
        #self.app.transit = {}
        #
    def close(self):
        #
        #
        print "close method"
        #
        # TODO : ajout des dicts à effacer lors de la suppression de la scène
        #
        self.ignoreAll();  taskMgr.remove(self.mouse_task); self.mouse_task = None
        self.states = None
        for key in self.dic_lights:
        	render.clearLight(self.dic_lights[key]); self.dic_lights[key].removeNode()
        for key1 in self.dic_gui:
            for key2 in self.dic_gui[key1]:
                for t in self.dic_gui[key1][key2].options():
                    if t[0] == "command":
                        self.dic_gui[key1][key2]["command"] = None; break
                self.dic_gui[key1][key2].removeNode()
        for key in self.dic_arrows:
            self.dic_arrows[key]["node"].removeNode(); self.dic_arrows[key]["card"].removeNode()
        for key in self.dic_statics: self.dic_statics[key].removeNode()
        for key in self.dic_dynamics: self.dic_dynamics[key].delete()
        for key in self.dic_anims:
        	self.dic_anims[key].finish(); self.dic_anims[key] = None
        #
        #
        self.dic_statics = None; self.dic_dynamics = None; self.dic_anims = None
        #
        self.vers_txt.removeNode()
        #
        print "end close"
        #
    # DEBUG : cette fonction n'aura plus d'utilité une fois le code de la scène terminé
    def __del__(self):
        print "delete mainscene"
    ###
