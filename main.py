# -*- coding: utf-8 -*-

from panda3d.core import loadPrcFile

loadPrcFile("config.prc")

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import Vec4, TextNode, CardMaker, NodePath, PandaNode, AmbientLight, LightRampAttrib
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32
from panda3d.core import WindowProperties
from pandac.PandaModules import TransparencyAttrib

import direct.directbase.DirectStart

#TEST
import sys
#TEST

class ArcnsApp(DirectObject):
    def __init__(self):
        #
        base.disableMouse(); base.setBackgroundColor(1,1,1); self.arcFont = base.loader.loadFont("misc/firstv2.ttf")
        #
        cm = CardMaker("cursor"); cm.setFrame(0,0.1,-0.13,0); self.cust_mouse = render.attachNewNode(cm.generate()); self.cust_mouse_tex = {}
        #
        self.cust_mouse_tex["blank"] = loader.loadTexture("models/cursors/blank_cursor.png")
        self.cust_mouse_tex["main"] = loader.loadTexture("models/cursors/main_cursor.png")
        #
        self.change_cursor("blank"); self.cust_mouse.setTransparency(TransparencyAttrib.MAlpha)
        self.cust_mouse.reparentTo(render2d); self.cust_mouse.setBin("gui-popup",100)
        base.mouseWatcherNode.setGeometry(self.cust_mouse.node()); self.activeCartoonFilter()
        self.alghtnode = AmbientLight("ambient light"); self.alghtnode.setColor(Vec4(0.4,0.4,0.4,1))
        self.alght = render.attachNewNode(self.alghtnode); render.setLight(self.alght)
        self.voile = DirectFrame(frameSize=(-2,2,-2,2),frameColor=(0,0,0,0.8)); self.voile.setBin("gui-popup",1); self.voile.hide()
        self.mouse_trav = CollisionTraverser(); self.mouse_hand = CollisionHandlerQueue()
        self.pickerNode = CollisionNode("mouseRay"); self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1)); self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay); self.mouse_trav.addCollider(self.pickerNP,self.mouse_hand)
        self.pickly_node = render.attachNewNode("pickly_node")
        from mainscene.mainscene import mainScene
        #
        #
        #TODO : vérifier l'utilité d'une scène de cinématique
        #
        from persoscene.persoscene import persoScene
        #
        #
        from gamescene.gamescene import gameScene
        #
        #TEST
        self.accept("d",self.testdel)
        self.accept("q",sys.exit,[0])
        #TEST
        #
        #self.curdir = base.appRunner.p3dFilename.getDirname(); self.main_config = None; self.speak = None
        self.curdir = "../"; self.main_config = None; self.speak = None
        #
        self.scene = mainScene(self); self.scene.request("Init")
        #
        #TEST
        #self.accept("t",self.scene.actionMainMenu)
        #TEST
        #
        #
    #TEST
    def testdel(self):
        print "testdel"
        #
        self.scene.close()
        #
        self.scene = None
        #
        print "end testdel"
        #
    #TEST
    def activeCartoonFilter(self):
        #
        #TODO : vérifier l'utilité de cette fonction et voir pour le changement entre mainscene et gamescene
        #
        self.rampnode = NodePath(PandaNode("ramp node")); self.rampnode.setAttrib(LightRampAttrib.makeSingleThreshold(0.1,0.7))
        self.rampnode.setShaderAuto(); base.cam.node().setInitialState(self.rampnode.getState())
        self.filters = CommonFilters(base.win,base.cam); self.filterok = self.filters.setCartoonInk(separation=1)
        #
    def change_cursor(self,chx):
        self.cust_mouse.setTexture(self.cust_mouse_tex[chx])
    def arcButton(self,txt,pos,cmd,scale=0.08,txtalgn=TextNode.ALeft,extraArgs=[]): #override button
        ndp = DirectButton(text=txt,scale=scale,text_font=self.arcFont,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_align=txtalgn,extraArgs=extraArgs)
        ndp._DirectGuiBase__componentInfo["text2"][0].setFg((0.03,0.3,0.8,1))
        ndp._DirectGuiBase__componentInfo["text3"][0].setFg((0.3,0.3,0.3,1))
        ndp["command"] = cmd; return ndp
    def arcLabel(self,txt,pos,scale=0.08,txtalgn=TextNode.ALeft): #override label
        ndp = DirectLabel(text=txt,scale=scale,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_font=self.arcFont,text_align=txtalgn)
        return ndp
    def arcOptMenu(self,txt,pos,items,init=0,cmd=None,scale=0.08,change=1,txtalgn=TextNode.ALeft,extraArgs=[]):
        ndp = DirectOptionMenu(text=txt,scale=scale,pos=pos,items=items,initialitem=init,textMayChange=change,text_font=self.arcFont,
            text_align=txtalgn,text_bg=(1,1,1,0.8),relief=None,highlightColor=(0.03,0.3,0.8,1),popupMarker_relief=None,
            popupMarker_pos=(0,0,0),popupMarkerBorder=(0,0),item_text_font=self.arcFont,extraArgs=extraArgs)
        ndp["command"] = cmd; return ndp
    def arcRadioButton(self,lst_rad,parent,gui,scale=0.08,txtalgn=TextNode.ALeft): #override radio button
        lst_radio = []
        for elt in lst_rad:
            ndp = DirectRadioButton(text=elt[0],variable=elt[1],value=elt[2],extraArgs=elt[4],
                text_align=txtalgn,scale=scale,pos=elt[5],text_font=self.arcFont,text_bg=(1,1,1,0.8),relief=None)
            ndp["command"] = elt[3],; lst_radio.append(ndp)
        for elt in lst_radio:
            elt.setOthers(lst_radio); elt.reparentTo(parent); gui.append(elt)
    def arcEntry(self,pos,txt="",cmd=None,scale=0.08,nlines=1): #override entry
        ndp = DirectEntry(pos=pos,text=txt,scale=scale,numLines=nlines,entryFont=self.arcFont,frameColor=(1,1,1,0.8),relief=DGG.RIDGE)
        ndp["command"] = cmd; return ndp
    def game_screen(self):
        #
        #TODO : retour à la fenêtre telle qu'elle doit être pour le menu principal
        #TODO : cette méthode est appelé depuis le close d'une gamescene, lorsque le joueur retourne au menu principal
        #
        pass
    def game_screen(self):
        #
        #TODO : cette méthode doit être appelé lorsque le joueur lance une partie
        #TODO : Elle est appelé par un task lancé depuis le close de la mainscene
        #
        wp = WindowProperties()
        if self.main_config["fullscreen"]:
            di = base.pipe.getDisplayInformation()
            for index in range(di.getTotalDisplayModes()):
                tmp_width = di.getDisplayModeWidth(index); tmp_height = di.getDisplayModeHeight(index)
                if (float(tmp_width)/tmp_height) > 1 and (float(tmp_width)/tmp_height) < 2:
                    wp.setSize(tmp_width,tmp_height); break
            wp.setFullscreen(True)
        elif not self.main_config["fullscreen"]: wp.setSize(950,700)
        base.openMainWindow(wp); base.setBackgroundColor(1,1,1)


app = ArcnsApp(); run()
