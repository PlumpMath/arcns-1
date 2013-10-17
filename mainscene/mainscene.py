# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DGG
from direct.stdpy.file import *
from direct.actor.Actor import Actor
from panda3d.core import Point3, Vec4, TextNode, CardMaker, PointLight, DirectionalLight, Spotlight, PerspectiveLens, BitMask32
from panda3d.core import Multifile, VirtualFileSystem, Filename, Patchfile
from direct.interval.IntervalGlobal import Sequence, Parallel

import Tkinter, tkFileDialog, json, sys, lang, os, urllib, shutil

class mainScene(FSM,DirectObject):
    """ ****************************
    Méthodes pour l'initialisation
    **************************** """
    def __init__(self,app):
        FSM.__init__(self,"mainScene"); self.defaultTransitions = {"Init":["MainMenu"],"MainMenu":["SubMenu"],"SubMenu":["MainMenu"]}
        camera.setPos(0,-62,12); camera.setHpr(0,-10,0); self.accept("escape",sys.exit,[0])
        self.app = app; self.version = "v0.0"; self.nomove = False
        if exists("arcns_config.json"):
            self.app.main_config = json.loads("".join([line.rstrip().lstrip() for line in file("arcns_config.json","rb")]))
        else:
            self.app.main_config = {"fullscreen": [False], "lang_chx": 1,"music":True,"sounds":True,"music_vol":1,"sounds_vol":1}
            try:
            	mcf = open("arcns_config.json","w"); mcf.write(json.dumps(self.app.main_config)); mcf.close()
            except Exception,e: print e
        self.dic_lights = {}; self.activeLights()
        if self.app.main_config["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
        elif self.app.main_config["lang_chx"] == 1: self.app.speak = lang.en.en_lang
        self.states = {"main_chx":0,"main_lst":[]}; self.options = {}
        for key in self.app.main_config:
            if key == "fullscreen": self.options[key] = [self.app.main_config[key][0]]
            else: self.options[key] = self.app.main_config[key]
        #
        # DEBUG : commande pour les tests
        self.accept("d",self.app.game_screen)
        self.accept("t",self.testdef)
        ###
        #
        self.dic_sounds = {}; self.loadSfx()
        self.dic_gui = {"main_menu":{},"camp_menu":{},"mission_menu":{},"credits_menu":{},"option_menu":{},"aux_menu":{}}; self.loadGUI()
        self.dic_arrows= {}; self.dic_statics = {}; self.dic_dynamics = {}; self.loadmodels();
        self.dic_anims = {}; self.activeAnim()
        self.vers_txt = OnscreenText(text=self.version,font=self.app.arcFont,pos=(1.15,-0.95),fg=(0,0,0,1),bg=(1,1,1,0.8))
        self.dic_musics = {}; self.loadMusics(); self.dic_musics["mainscene_music"].setLoop(True)
        if self.app.main_config["music"]: self.dic_musics["mainscene_music"].play()
        #
        #
        #
        self.mouse_task = taskMgr.add(self.mouseTask,"mainscene mouse task")
    # DEBUG : fonction uniquement présente pour faciliter les tests
    def testdef(self):
        pass
    ###
    def loadSfx(self):
        self.dic_sounds["main_menu_sel"] = base.loader.loadSfx("mainscene/sounds/son_main_menu_sel.wav")
        self.dic_sounds["main_menu_switch"] = base.loader.loadSfx("mainscene/sounds/son_main_menu_main.wav")
        self.dic_sounds["main_menu_escape"] = base.loader.loadSfx("mainscene/sounds/son_main_menu_aux.wav")
        for key in self.dic_sounds: self.dic_sounds[key].setVolume(self.app.main_config["sounds_vol"])
    def loadMusics(self):
        #
        # TODO : changer le ".mp3" par ".wav" dès que la musique sera prête
        #
        self.dic_musics["mainscene_music"] = base.loader.loadMusic("mainscene/musics/main_music.mp3")
        #
        self.dic_musics["mainscene_music"].setVolume(self.app.main_config["music_vol"])
    # NOTE : cette méthode est temporaire, et sera à terme remplacer par l'outils de parsing des scènes
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
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["credits"],(-0.26,0,-0.47),self.actionMainMenu,scale=0.09)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["credits"] = tmp_gui; self.states["main_lst"].append("credits")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["options"],(-0.35,0,-0.58),self.actionMainMenu,scale=0.07)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["options"] = tmp_gui; self.states["main_lst"].append("options")
        tmp_gui = self.app.arcButton(self.app.speak["main_menu"]["quit"],(-0.41,0,-0.66),self.actionMainMenu,scale=0.05)
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED
        self.dic_gui["main_menu"]["quit"] = tmp_gui; self.states["main_lst"].append("quit")
        #camp_menu
        #
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["camp_menu"]["frame"] = tmp_frame
        #
        tmp_gui = self.app.arcLabel(self.app.speak["camp_menu"]["stitre"],(-0.8,0,0.7),0.15); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["camp_menu"]["stitre"] = tmp_gui
        #
        # TODO : éléments gui pour le camp_menu à construire ici
        #
        #mission_menu
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["mission_menu"]["frame"] = tmp_frame
        tmp_gui = self.app.arcLabel(self.app.speak["mission_menu"]["stitre"],(-0.8,0,0.7),0.15); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["mission_menu"]["stitre"] = tmp_gui
        #
        # TODO : éléments gui pour le mission_menu à construire ici
        #
        # DEBUG : label temporaire "W.I.P." pour le sous menu "Missions"
        tmp_gui = self.app.arcLabel("W.I.P.",(0,0,0),0.2); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["mission_menu"]["wip"] = tmp_gui
        ###
        #
        #credits_menu
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["credits_menu"]["frame"] = tmp_frame
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["stitre"],(-0.8,0,0.7),0.15); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["credits_menu"]["stitre"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["graph_lab"],(-0.5,0,0.4),0.1,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["graph_lab"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["graph_name"],(-0.5,0,0.3),txtalgn=TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["graph_name"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["dev_lab"],(0.5,0,0.4),0.1,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["dev_lab"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["dev_name"],(0.5,0,0.3),txtalgn=TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["dev_name"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["trad_lab"],(-0.5,0,-0.1),0.1,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["trad_lab"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["trad_name"],(-0.5,0,-0.2),txtalgn=TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["trad_name"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["music_lab"],(0.5,0,-0.1),0.1,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["music_lab"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["credits_menu"]["music_name"],(0.5,0,-0.2),txtalgn=TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["credits_menu"]["music_name"] = tmp_gui
        #option_menu
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["option_menu"]["frame"] = tmp_frame
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["stitre"],(-0.8,0,0.7),0.15); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["option_menu"]["stitre"] = tmp_gui
        lst_radio = [
            [self.app.speak["option_menu"]["windowed"],self.options["fullscreen"],[False],
                self.actionSubMenu,["","change_opt","win"],(-1,0,0.4),"windowed"],
            [self.app.speak["option_menu"]["fullscreen"],self.options["fullscreen"],[True],
                self.actionSubMenu,["","change_opt","win"],(-1,0,0.3),"fullscreen"]
        ]
        self.app.arcRadioButton(lst_radio,tmp_frame,self.dic_gui["option_menu"])
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["lang_chx"],(-1.05,0,0.15)); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["option_menu"]["lang_chx"] = tmp_gui
        txt = None
        if self.options["lang_chx"] == 0: "Français"
        elif self.options["lang_chx"] == 1: "English"
        tmp_gui = self.app.arcOptMenu(txt,(-0.45,0,0.15),["Français","English"],self.options["lang_chx"],
            self.actionSubMenu,extraArgs=["change_opt","lang"])
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["lang_opt"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["music_vol"],(-1.05,0,-0.2)); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["option_menu"]["music_vol"] = tmp_gui
        tmp_gui = self.app.arcCheckButton(self.app.speak["option_menu"]["music_mute"],(0.3,0,-0.2),
            self.actionSubMenu,(1 if self.options["music"] else 0),extraArgs=["change_opt","music_mute"])
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["music_mute"] = tmp_gui
        tmp_gui = self.app.arcSlider((-0.3,0,-0.3),1,(0,1),self.options["music_vol"],0.1,self.actionSubMenu,[None,"change_opt","music_vol"])
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["music_slider"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["sound_vol"],(-1.05,0,-0.5)); tmp_gui.reparentTo(tmp_frame)
        self.dic_gui["option_menu"]["sound_vol"] = tmp_gui
        tmp_gui = self.app.arcCheckButton(self.app.speak["option_menu"]["sound_mute"],(0.3,0,-0.5),
            self.actionSubMenu,(1 if self.options["sounds"] else 0),extraArgs=["change_opt","sound_mute"])
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["sound_mute"] = tmp_gui
        tmp_gui = self.app.arcSlider((-0.3,0,-0.6),1,(0,1),self.options["sounds_vol"],0.1,self.actionSubMenu,[None,"change_opt","sounds_vol"])
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["sound_slider"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["maj_verify"],(0.5,0,0.4),self.checkMajStarter)
        tmp_gui.reparentTo(tmp_frame); self.dic_gui["option_menu"]["maj_verify"] = tmp_gui
        #formulaire de mise à jour
        tmp_frame2 = DirectFrame(); self.dic_gui["option_menu"]["maj_frame"] = tmp_frame2
        tmp_frame2.hide(); tmp_frame2.reparentTo(self.app.voile)
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_stitre"],(0,0,0.4),0.15,TextNode.ACenter)
        tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_stitre"] = tmp_gui
        tmp_gui = self.app.arcWaitBar((0,0,0),0.8,4,0,self.app.speak["option_menu"]["maj_progress"])
        tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_progress"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_err0"],(0,0,0.1),0.1,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_err0"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["maj_retry"],(-0.3,0,-0.1),self.checkMajStarter,txtalgn=TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_retry"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["maj_cancel"],(0.3,0,-0.1),self.cancelMaj,txtalgn=TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_cancel"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_err1"],(0,0,0.1),0.1,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_err1"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_nomaj"],(0,0,0.1),0.1,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_nomaj"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_update"],(0,0,0.1),0.1,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_update"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["maj_doit"],(-0.3,0,-0.1),self.doMajStarter,txtalgn=TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_doit"] = tmp_gui
        tmp_gui = self.app.arcWaitBar((0,0,0),0.8,4,0,self.app.speak["option_menu"]["maj_upgrade"])
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_upgrade"] = tmp_gui
        tmp_gui = self.app.arcLabel(self.app.speak["option_menu"]["maj_success"],(0,0,0),0.1,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_success"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["maj_quit"],(0,0,-0.4),self.endingMaj,0.11,TextNode.ACenter)
        tmp_gui.hide(); tmp_gui.reparentTo(tmp_frame2); self.dic_gui["option_menu"]["maj_quit"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["btn_valid"],(-0.9,0,-0.8),self.actionSubMenu,extraArgs=["valid_opt"])
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["option_menu"]["btn_valid"] = tmp_gui
        tmp_gui = self.app.arcButton(self.app.speak["option_menu"]["btn_reset"],(-0.5,0,-0.8),self.actionSubMenu,extraArgs=["cancel_opt"])
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["option_menu"]["btn_reset"] = tmp_gui
        #aux_menu
        tmp_frame = DirectFrame(); tmp_frame.hide(); self.dic_gui["aux_menu"]["frame"] = tmp_frame
        tmp_gui = self.app.arcButton(self.app.speak["aux_menu"]["return_btn"],(0,0,-0.8),self.actionSubMenu,extraArgs=["quit"])
        tmp_gui.reparentTo(tmp_frame); tmp_gui["state"] = DGG.DISABLED; self.dic_gui["aux_menu"]["return_btn"] = tmp_gui
    def loadmodels(self):
        #arrows & cards
        arr_up = render.attachNewNode("main arrow up"); arr_up.setHpr(0,90,0); arr_up.setPos(6.2,1.5,7.3); arr_up.hide()
        self.app.arrow_mod.instanceTo(arr_up); arr_up.reparentTo(render)
        arr_up_crd = render.attachNewNode(self.app.card_arrow.generate()); arr_up_crd.node().setIntoCollideMask(BitMask32.bit(1)); arr_up_crd.hide()
        arr_up_crd.node().setTag("arrow","mainup"); arr_up_crd.reparentTo(self.app.pickly_node); arr_up_crd.setPos(6.2,1.7,7)
        self.dic_arrows["arrow_up"] = {"node":arr_up,"card":arr_up_crd,"status":0,"posn":[6.2,1.5,7.3],"posh":[6.2,1.7,7.5]}
        arr_dn = render.attachNewNode("main arrow down"); arr_dn.setHpr(180,-90,0);  arr_dn.setPos(6.2,1.5,5); arr_dn.hide()
        self.app.arrow_mod.instanceTo(arr_dn); arr_dn.reparentTo(render)
        arr_dn_crd = render.attachNewNode(self.app.card_arrow.generate()); arr_dn_crd.node().setIntoCollideMask(BitMask32.bit(1)); arr_dn_crd.hide()
        arr_dn_crd.node().setTag("arrow","maindn"); arr_dn_crd.reparentTo(self.app.pickly_node); arr_dn_crd.setPos(6.2,1.7,5.2)
        self.dic_arrows["arrow_dn"] = {"node":arr_dn,"card":arr_dn_crd,"status":0,"posn":[6.2,1.5,5],"posh":[6.2,1.7,4.8]}
        #
        #
        # TODO : flèches pour les différents sous-menus à construire ici
        #
        # NOTE : toutes la partie entre ### est temporaire, en attente que le module de parsing fonctionne
        ###
        #gates and moving arcs
        tmp_mod = Actor("mainscene/models/dynamics/main_gates.bam"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,-48.2,9.5); tmp_mod.setHpr(0,80,0); self.dic_dynamics["gates"] = tmp_mod
        tmp_mod = Actor("mainscene/models/dynamics/main_m_menu.bam"); tmp_mod.reparentTo(render)
        tmp_mod.pose("load",1); self.dic_dynamics["arcs_main_menu"] = tmp_mod
        tmp_mod = Actor("mainscene/models/dynamics/main_a_menu.bam"); tmp_mod.reparentTo(render)
        tmp_mod.pose("load",1); self.dic_dynamics["arcs_aux_menu"] = tmp_mod
        #décors
        #
        #tmp_mod = base.loader.loadModel("mainscene/models/statics/main_sol.bam"); tmp_mod.reparentTo(render)
        #tmp_mod.setPos(0,0,0); self.dic_statics["sol"] = tmp_mod
        #
        tmp_mod = base.loader.loadModel("mainscene/models/statics/socle_base.bam"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["socle_base"] = tmp_mod
        #
        tmp_mod = base.loader.loadModel("mainscene/models/statics/main_roofs.bam"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,0,0); self.dic_statics["roofs"] = tmp_mod
        tmp_mod = base.loader.loadModel("mainscene/models/statics/main_arcs_show.bam"); tmp_mod.reparentTo(render)
        tmp_mod.setPos(0,7.3,3); self.dic_statics["arcs_shower"] = tmp_mod
        #
        tmp_mod = base.loader.loadModel("mainscene/models/statics/main_title.bam"); tmp_mod.reparentTo(render)
        self.dic_statics["arc_title"] = tmp_mod
        ###
        #
    def activeAnim(self):
        tmp_anim = self.dic_statics["arcs_shower"].hprInterval(5,Point3(360,0,0),startHpr=Point3(0,0,0))
        self.dic_anims["arcs_shower_pace"] = Sequence(tmp_anim,name="arcs_shower_pace")
        self.dic_anims["cam_move_init"] = camera.posInterval(4,Point3(0,-25,12))
        self.dic_anims["move_texts"] = None
        self.dic_anims["cam_move_maintosub"] = Parallel(name="main to sub")
        self.dic_anims["cam_move_maintosub"].append(camera.posInterval(2,Point3(-4,-1,7)))
        self.dic_anims["cam_move_maintosub"].append(camera.hprInterval(2,Point3(-90,-10,0)))
        self.dic_anims["cam_move_subtomain"] = Parallel(name="sub to main")
        self.dic_anims["cam_move_subtomain"].append(camera.posInterval(2,Point3(0,-25,12)))
        self.dic_anims["cam_move_subtomain"].append(camera.hprInterval(2,Point3(0,-10,0)))
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
        self.app.change_cursor("main"); self.dic_gui["main_menu"]["frame"].show(); taskMgr.add(self.reactiveMainMenu,"reactive MainMenu")
        self.dic_arrows["arrow_up"]["status"] = 1; self.dic_arrows["arrow_dn"]["status"] = 1
        self.dic_gui["main_menu"][self.states["main_lst"][self.states["main_chx"]]]["state"] = DGG.NORMAL
    def exitMainMenu(self):
        pass
    def actionMainMenu(self,value="valid"):
        if not self.nomove: return
        if value == "click":
            if self.dic_arrows["arrow_up"]["status"] == 2: value = "up"
            elif self.dic_arrows["arrow_dn"]["status"] == 2: value = "down"
            else: return
        self.dic_gui["main_menu"][self.states["main_lst"][self.states["main_chx"]]]["state"] = DGG.DISABLED
        if value == "down" or value == "up":
            sens = None
            if value == "down" and self.states["main_chx"] > 0: sens = True
            elif value == "up" and self.states["main_chx"] < 4: sens = False
            if sens != None:
                self.dic_arrows["arrow_up"]["status"] = 1
                self.dic_arrows["arrow_up"]["node"].setPos(self.dic_arrows["arrow_up"]["posn"][0]
                    ,self.dic_arrows["arrow_up"]["posn"][1],self.dic_arrows["arrow_up"]["posn"][2])
                self.dic_arrows["arrow_dn"]["status"] = 1
                self.dic_arrows["arrow_dn"]["node"].setPos(self.dic_arrows["arrow_dn"]["posn"][0]
                    ,self.dic_arrows["arrow_dn"]["posn"][1],self.dic_arrows["arrow_dn"]["posn"][2])
                if self.app.main_config["sounds"]: self.dic_sounds["main_menu_switch"].play()
                self.states["main_chx"] += (-1 if sens else 1)
                self.dic_arrows["arrow_up"]["node"].hide(); self.dic_arrows["arrow_dn"]["node"].hide()
                pos_texts = [(-0.41,0,0.31),(-0.35,0,0.22),(-0.26,0,0.1),(-0.19,0,-0.04),(-0.15,0,-0.2),
                    (-0.19,0,-0.34),(-0.26,0,-0.47),(-0.35,0,-0.58),(-0.41,0,-0.66)]
                scale_texts = [0.05,0.07,0.09,0.1,0.12,0.1,0.09,0.07,0.05]
                try: self.dic_anims["move_texts"].finish()
                except: pass
                self.dic_anims["move_texts"] = None; self.dic_anims["move_texts"] = Parallel(name="MainMenu movement")
                for it in range(5):
                    tmp_anim = self.dic_gui["main_menu"][self.states["main_lst"][it]].posInterval(0.4,Point3(pos_texts[4-self.states["main_chx"]+it]))
                    self.dic_anims["move_texts"].append(tmp_anim)
                    tmp_anim = self.dic_gui["main_menu"][self.states["main_lst"][it]].scaleInterval(0.4,scale_texts[4-self.states["main_chx"]+it])
                    self.dic_anims["move_texts"].append(tmp_anim)
                self.dic_dynamics["arcs_main_menu"].play("state_"+str(self.states["main_chx"]+(1 if sens else -1))+"_"+str(self.states["main_chx"]))
                self.nomove = False; self.dic_anims["move_texts"].start(); taskMgr.doMethodLater(0.4,self.reactiveMainMenu,"reactive MainMenu")
            else:
                self.dic_gui["main_menu"][self.states["main_lst"][self.states["main_chx"]]]["state"] = DGG.NORMAL
        elif value == "valid":
            if self.app.main_config["sounds"]: self.dic_sounds["main_menu_sel"].play()
            self.ignoreAll(); self.accept("escape",sys.exit,[0]); self.nomove = False
            if self.states["main_chx"] == 4: sys.exit(0)
            else: self.launchSubMenu()
    def reactiveMainMenu(self,task):
        self.nomove = True
        if self.states["main_chx"] < 4: self.dic_arrows["arrow_up"]["node"].show()
        if self.states["main_chx"] > 0: self.dic_arrows["arrow_dn"]["node"].show()
        self.dic_gui["main_menu"][self.states["main_lst"][self.states["main_chx"]]]["state"] = DGG.NORMAL
        #capture de la souris
        self.accept("mouse1",self. actionMainMenu,["click"]); self.accept("wheel_up",self.actionMainMenu,["up"])
        self.accept("wheel_down",self.actionMainMenu,["down"])
        #capture du clavier
        self.accept("arrow_up",self.actionMainMenu,["up"]); self.accept("arrow_down",self.actionMainMenu,["down"])
        self.accept("enter",self.actionMainMenu,["valid"])
        return task.done
    def launchSubMenu(self):
        self.app.change_cursor("blank"); self.dic_gui["main_menu"]["frame"].hide()
        self.dic_arrows["arrow_up"]["status"] = 0; self.dic_arrows["arrow_dn"]["status"] = 0
        self.dic_arrows["arrow_up"]["node"].hide(); self.dic_arrows["arrow_dn"]["node"].hide()
        self.dic_anims["cam_move_maintosub"].start()
        taskMgr.doMethodLater(1,self.subArcsTask,"anim aux arcs task")
        taskMgr.doMethodLater(2.5,self.goSubMenuTask,"aff sub menu task")
    def goSubMenuTask(self,task):
        self.request("SubMenu"); return task.done
    """ ****************************
    Méthodes pour l'état "SubMenu"
    **************************** """
    def enterSubMenu(self):
        self.app.change_cursor("main"); frame = None; self.accept("escape",self.actionSubMenu,["quit"])
        if self.states["main_chx"] == 0:
            frame = "camp_menu"
            #
            # TODO : self.accept des touches fléchées et de la touche entrée pour le sous menu "Campagne"
            #
        elif self.states["main_chx"] == 1:
            frame = "mission_menu"
            #
            # TODO : self.accept des touches fléchées et de la touche entrée pour le sous menu "Missions"
            #
        elif self.states["main_chx"] == 2: frame = "credits_menu"
        elif self.states["main_chx"] == 3:
            frame = "option_menu"; self.accept("enter",self.actionSubMenu,["valid_opt"])
        self.dic_gui[frame]["frame"].show(); self.dic_gui["aux_menu"]["frame"].show()
        self.dic_gui["aux_menu"]["return_btn"]["state"] = DGG.NORMAL
    def exitSubMenu(self):
        pass
    def actionSubMenu(self,val1,val2=None,val3=None):
        if val1 == "quit":
            if self.app.main_config["sounds"]: self.dic_sounds["main_menu_escape"].play()
            self.app.change_cursor("blank"); frame = None
            if self.states["main_chx"] == 0:
                #
                # TODO : vérifier qu'il n'y a rien a faire avant de quitter le sous menu "campagne"
                #
                frame = "camp_menu"
            elif self.states["main_chx"] == 1:
                #
                # TODO : vérifier qu'il n'y a rien à faire avant de quitter le sous menu "missions"
                #
                frame = "mission_menu"
            elif self.states["main_chx"] == 2: frame = "credits_menu"
            elif self.states["main_chx"] == 3:
                self.actionSubMenu("cancel_opt"); frame = "option_menu"
            self.dic_gui[frame]["frame"].hide(); self.dic_gui["aux_menu"]["frame"].hide()
            self.ignoreAll(); self.accept("escape",sys.exit,[0])
            self.dic_anims["cam_move_subtomain"].start()
            taskMgr.doMethodLater(1,self.subArcsTask,"anim aux arcs task")
            taskMgr.doMethodLater(2.5,self.goMainMenuTask,"aff main menu task")
            self.dic_gui["aux_menu"]["return_btn"]["state"] = DGG.DISABLED
            #
            # TODO : remise à zéro des options et DGG.DISABLED sur les boutons
            #
        elif val1 == "cancel_opt":
            if self.app.main_config["sounds"]: self.dic_sounds["main_menu_escape"].play()
            for key in self.options:
                if key == "fullscreen":
                    if self.options[key][0] != self.app.main_config[key][0]:
                        self.dic_gui["option_menu"]["windowed"]["indicatorValue"] = (0 if self.app.main_config["fullscreen"][0] else 1)
                        self.dic_gui["option_menu"]["windowed"].setIndicatorValue()
                        self.dic_gui["option_menu"]["fullscreen"]["indicatorValue"] = (1 if self.app.main_config["fullscreen"][0] else 0)
                        self.dic_gui["option_menu"]["fullscreen"].setIndicatorValue()
                else:
                    if self.options[key] != self.app.main_config[key]:
                        if key == "lang_chx": self.dic_gui["option_menu"]["lang_opt"].set(self.app.main_config[key])
                        elif key == "music":
                            self.dic_gui["option_menu"]["music_mute"]["indicatorValue"] = self.app.main_config[key]
                            self.dic_gui["option_menu"]["music_mute"].setIndicatorValue()
                        elif key == "sounds":
                            self.dic_gui["option_menu"]["sound_mute"]["indicatorValue"] = self.app.main_config[key]
                            self.dic_gui["option_menu"]["sound_mute"].setIndicatorValue()
                        elif key == "music_vol": self.dic_gui["option_menu"]["music_slider"]["value"] = self.app.main_config[key]
                        elif key == "sounds_vol": self.dic_gui["option_menu"]["sound_slider"]["value"] = self.app.main_config[key]
            for key in self.app.main_config:
                if key == "fullscreen": self.options[key][0] = self.app.main_config[key][0]
                else: self.options[key] = self.app.main_config[key]
            self.dic_gui["option_menu"]["btn_valid"]["state"] = DGG.DISABLED
            self.dic_gui["option_menu"]["btn_reset"]["state"] = DGG.DISABLED
        elif val1 == "valid_opt":
            if self.app.main_config["sounds"]: self.dic_sounds["main_menu_sel"].play()
            if self.options["lang_chx"] != self.app.main_config["lang_chx"]:
                if self.options["lang_chx"] == 0: self.app.speak = lang.fr.fr_lang
                elif self.options["lang_chx"] == 1: self.app.speak = lang.en.en_lang
                for key1 in self.app.speak:
                    for key2 in self.app.speak[key1]: self.dic_gui[key1][key2]["text"] = self.app.speak[key1][key2]
            if self.options["music"] != self.app.main_config["music"]:
                if self.options["music"]: self.dic_music["mainscene_music"].play()
                else: self.dic_music["mainscene_music"].stop()
            if self.options["sounds_vol"] != self.app.main_config["sounds_vol"]:
                for key in self.dic_sounds: self.dic_sounds[key].setVolume(self.options["sounds_vol"])
            if self.options["music_vol"] != self.app.main_config["music_vol"]: self.dic_music["mainscene_music"].setVolume(self.options["music_vol"])
            for key in self.app.main_config:
                if key == "fullscreen": self.app.main_config[key][0] = self.options[key][0]
                else: self.app.main_config[key] = self.options[key]
            mcf = open("arcns_config.json","w"); mcf.write(json.dumps(self.options)); mcf.close()
            self.dic_gui["option_menu"]["btn_valid"]["state"] = DGG.DISABLED
            self.dic_gui["option_menu"]["btn_reset"]["state"] = DGG.DISABLED
        elif val2 == "change_opt":
            if val3 == "win": pass
            elif val3 == "lang":
                if val1 == "Français": self.options["lang_chx"] = 0
                elif val1 == "English": self.options["lang_chx"] = 1
            elif val3 == "music_mute": self.options["music"] = bool(val1)
            elif val3 == "sound_mute": self.options["sounds"] = bool(val1)
            elif val3 == "music_vol": self.options["music_vol"] = int(self.dic_gui["option_menu"]["music_slider"]["value"]*100)/100.0
            elif val3 == "sounds_vol": self.options["sounds_vol"] = int(self.dic_gui["option_menu"]["sound_slider"]["value"]*100)/100.0
            self.dic_gui["option_menu"]["btn_valid"]["state"] = DGG.DISABLED
            self.dic_gui["option_menu"]["btn_reset"]["state"] = DGG.DISABLED
            for key in self.options:
                if not self.options[key] == self.app.main_config[key]:
                    self.dic_gui["option_menu"]["btn_valid"]["state"] = DGG.NORMAL
                    self.dic_gui["option_menu"]["btn_reset"]["state"] = DGG.NORMAL
                    break
        #
        # TODO : reste des actions ici
        #
        print "val1 : "+str(val1)
        print "val2 : "+str(val2)
        print "val3 : "+str(val3)
        #
        # NOTE : code pour l'import et l'export
        """   Tkinter open filepicker and dirpicker
        root = Tkinter.Tk(); root.withdraw()
        print tkFileDialog.askopenfilename(filetypes=[("Saves","*.save"),("All","*")])
        print tkFileDialog.askdirectory()
        """
        #
    def checkMajStarter(self):
        self.dic_gui["option_menu"]["maj_success"].hide(); self.dic_gui["option_menu"]["maj_quit"].hide()
        self.dic_gui["option_menu"]["maj_retry"].hide(); self.dic_gui["option_menu"]["maj_retry"]["command"] = self.checkMajStarter
        self.dic_gui["option_menu"]["maj_err0"].hide(); self.dic_gui["option_menu"]["maj_err1"].hide()
        self.dic_gui["option_menu"]["maj_nomaj"].hide(); self.dic_gui["option_menu"]["maj_update"].hide()
        self.dic_gui["option_menu"]["maj_doit"].hide(); self.dic_gui["option_menu"]["maj_upgrade"].hide()
        self.dic_gui["option_menu"]["maj_cancel"].hide(); self.dic_gui["option_menu"]["maj_progress"].show()
        self.dic_gui["option_menu"]["frame"].hide(); self.dic_gui["aux_menu"]["frame"].hide()
        self.app.voile.show(); self.ignoreAll(); self.dic_gui["option_menu"]["maj_frame"].show()
        self.app.change_cursor("blank"); self.dic_gui["option_menu"]["maj_progress"]["value"] = 0
        taskMgr.doMethodLater(0.1,self.majTask,"check maj task")
    def doMajStarter(self):
        self.dic_gui["option_menu"]["maj_cancel"].hide()
        self.dic_gui["option_menu"]["maj_retry"].hide(); self.dic_gui["option_menu"]["maj_retry"]["command"] = self.doMajStarter
        self.dic_gui["option_menu"]["maj_update"].hide(); self.dic_gui["option_menu"]["maj_doit"].hide()
        self.dic_gui["option_menu"]["maj_err0"].hide(); self.dic_gui["option_menu"]["maj_err1"].hide()
        lst = listdir("arcns_tmp")
        for elt in lst:
            if not elt == "arcns_multifiles.json": os.unlink("arcns_tmp/"+elt)
        self.dic_gui["option_menu"]["maj_progress"]["value"] = 5; self.dic_gui["option_menu"]["maj_upgrade"].show()
        self.app.change_cursor("blank"); self.ignoreAll(); self.dic_gui["option_menu"]["maj_upgrade"]["value"] = 0
        taskMgr.doMethodLater(0.1,self.majTask,"do maj task")
    def majTask(self,task):
        if self.dic_gui["option_menu"]["maj_progress"]["value"] == 0:
            if not exists("arcns_tmp"):
                try: os.mkdir("arcns_tmp")
                except Exception,e:
                    print e; self.labelMaj(); return task.done
            self.dic_gui["option_menu"]["maj_progress"]["value"] = 1; return task.again
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 1:
            try:
                urllib.urlretrieve("http://www.arcns.net/arcns_multifiles.json","arcns_tmp/arcns_multifiles.json")
            except Exception,e:
                print e; self.labelMaj(); return task.done
            self.dic_gui["option_menu"]["maj_progress"]["value"] = 2; return task.again
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 2:
            try:
                self.tmp_multifiles = json.loads("".join([line.rstrip().lstrip() for line in file("arcns_tmp/arcns_multifiles.json","rb")]))
            except Exception,e:
                print e; self.labelMaj(); return task.done
            self.dic_gui["option_menu"]["maj_progress"]["value"] = 3; return task.again
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 3:
            for key in self.app.arcns_multifiles:
                if self.app.arcns_multifiles[key] < self.tmp_multifiles[key]: self.dic_gui["option_menu"]["maj_progress"]["value"] = 4
                else: del self.tmp_multifiles[key]
            self.labelMaj(); return task.done
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 0:
            try:
                for key in self.tmp_multifiles:
                    fln = "patch_"+key+"_r"+str(self.app.arcns_multifiles[key])+"_r"+str(self.tmp_multifiles[key])+".mf"
                    urllib.urlretrieve("http://www.arcns.net/patchs/"+fln,"arcns_tmp/"+fln)
                self.dic_gui["option_menu"]["maj_upgrade"]["value"] = 1; return task.again
            except Exception,e:
                print e; self.labelMaj(); return task.done
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 1:
            try:
                for key in self.tmp_multifiles: shutil.copy("arcns_mfs/"+key+"_r"+str(self.app.arcns_multifiles[key])+".mf","arcns_tmp")
                self.dic_gui["option_menu"]["maj_upgrade"]["value"] = 2; return task.again
            except Exception,e:
                print e; self.labelMaj(); return task.done
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 2:
            try:
                p = Patchfile(); m = Multifile()
                for key in self.tmp_multifiles:
                    fln = "patch_"+key+"_r"+str(self.app.arcns_multifiles[key])+"_r"+str(self.tmp_multifiles[key])
                    m.openRead("arcns_tmp/"+fln+".mf"); m.extractSubfile(0,"arcns_tmp/"+fln+".patch"); m.close()
                    rtn = p.apply(Filename("arcns_tmp/"+fln+".patch"),Filename("arcns_tmp/"+key+"_r"+str(self.app.arcns_multifiles[key])+".mf"))
                    if not rtn:
                        self.labelMaj(); return task.done
                    else: os.rename("arcns_tmp/"+key+"_r"+str(self.app.arcns_multifiles[key])+".mf","arcns_tmp/"+key+"_r"+str(self.tmp_multifiles[key])+".mf")
                self.dic_gui["option_menu"]["maj_upgrade"]["value"] = 3; return task.again
            except Exception,e:
                print e; self.labelMaj(); return task.done
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 3:
            try:
                for key in self.tmp_multifiles:
                    shutil.copy("arcns_tmp/"+key+"_r"+str(self.tmp_multifiles[key])+".mf","arcns_mfs")
                self.dic_gui["option_menu"]["maj_upgrade"]["value"] = 4; return task.again
            except Exception,e:
                print e; self.labelMaj(); return task.done
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 4:
            for key in self.tmp_multifiles:
                oldnb = self.app.arcns_multifiles[key]; self.app.arcns_multifiles[key] = self.tmp_multifiles[key]
                mcm = open("arcns_multifiles.json","w"); mcm.write(json.dumps(self.app.arcns_multifiles)); mcm.close()
                self.tmp_multifiles[key] = oldnb; os.unlink("arcns_mfs/"+key+"_r"+str(oldnb)+".mf")
            self.dic_gui["option_menu"]["maj_success"].show(); self.dic_gui["option_menu"]["maj_quit"].show()
            self.dic_gui["option_menu"]["maj_upgrade"].hide(); self.accept("enter",self.endingMaj)
            self.app.change_cursor("main"); return task.done
    def labelMaj(self):
        self.app.change_cursor("main"); self.accept("escape",self.cancelMaj); val_btn = "retry"
        self.accept("enter",(self.checkMajStarter if self.dic_gui["option_menu"]["maj_progress"] == 5 else self.doMajStarter))
        self.dic_gui["option_menu"]["maj_progress"].hide(); self.dic_gui["option_menu"]["maj_upgrade"].hide()
        if self.dic_gui["option_menu"]["maj_progress"]["value"] == 0: self.dic_gui["option_menu"]["maj_err0"].show()
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 1: self.dic_gui["option_menu"]["maj_err1"].show()
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 2: self.dic_gui["option_menu"]["maj_err1"].show()
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 3: self.dic_gui["option_menu"]["maj_nomaj"].show()
        elif self.dic_gui["option_menu"]["maj_progress"]["value"] == 4:
            val_btn = "doit"; self.dic_gui["option_menu"]["maj_update"].show()
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 0: self.dic_gui["option_menu"]["maj_err1"].show()
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 1: self.dic_gui["option_menu"]["maj_err0"].show()
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 2: self.dic_gui["option_menu"]["maj_err0"].show()
        elif self.dic_gui["option_menu"]["maj_upgrade"]["value"] == 3: self.dic_gui["option_menu"]["maj_err0"].show()
        self.dic_gui["option_menu"]["maj_cancel"].show(); self.dic_gui["option_menu"]["maj_"+val_btn].show()
    def cancelMaj(self):
        if exists("arcns_tmp"):
            lst = listdir("arcns_tmp")
            for elt in lst: os.unlink("arcns_tmp/"+elt)
            os.rmdir("arcns_tmp")
        self.app.voile.hide(); self.ignoreAll(); self.dic_gui["option_menu"]["maj_frame"].hide()
        self.dic_gui["option_menu"]["frame"].show(); self.dic_gui["aux_menu"]["frame"].show()
        self.accept("enter",self.actionSubMenu,["valid_opt"]); self.accept("escape",self.actionSubMenu,["quit"])
    def endingMaj(self):
        executable = sys.executable; args = sys.argv[:]; args.insert(0, sys.executable); os.execvp(executable, args)
    def goMainMenuTask(self,task):
        self.request("MainMenu"); return task.done
    def subArcsTask(self,task):
        if self.state == "MainMenu": self.dic_dynamics["arcs_aux_menu"].play("load")
        elif self.state == "SubMenu": self.dic_dynamics["arcs_aux_menu"].play("unload")
        return task.done
    """ ****************************
    Méthodes pour la sortie du menu principal
    **************************** """
    def launchGame(self):
        #
        # TODO : lancement du jeu. Ce n'est pas un changement de state, c'est une exécution de méthode simple, avec des tasks
        #
        # TODO : modification de self.app.speak, pour prendre le bon fichier de traduction pour l'ensemble du jeu dans le package de la gamescene
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
        self.ignoreAll();  taskMgr.remove(self.mouse_task); self.mouse_task = None
        self.states = None
        for key in self.dic_anims:
            try: self.dic_anims[key].finish()
            except: pass
            self.dic_anims[key] = None
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
        for key in self.dic_sounds:
            self.dic_sounds[key].stop(); self.dic_sounds[key] = None
        for key in self.dic_musics:
            self.dic_musics[key].stop(); self.dic_musics[key] = None
        self.dic_statics = None; self.dic_dynamics = None; self.dic_anims = None
        self.dic_sounds = None; self.dic_musics = None
        self.vers_txt.removeNode()
    # DEBUG : cette fonction n'aura plus d'utilité une fois le code de la scène terminé
    def __del__(self):
        print "delete mainscene"
    ###
