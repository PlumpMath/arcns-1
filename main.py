# -*- coding: utf-8 -*-

from panda3d.core import loadPrcFile

loadPrcFile("config.prc")

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import Vec4, TextNode, CardMaker, NodePath, PandaNode, AmbientLight, WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32
from pandac.PandaModules import TransparencyAttrib

from mainscene.mainscene import mainScene
from persoscene.persoscene import persoScene
from gamescene.gamescene import gameScene

import direct.directbase.DirectStart

class ArcnsApp(DirectObject):
    def __init__(self):
    	base.disableMouse(); base.setBackgroundColor(1,1,1)
    	self.arcFont = base.loader.loadFont(("" if base.appRunner else "misc/")+"firstv2.ttf")
        self.cust_mouse_tex = {}
        self.cust_mouse_tex["blank"] = loader.loadTexture(("" if base.appRunner else "models/")+"cursors/blank_cursor.png")
        self.cust_mouse_tex["main"] = loader.loadTexture(("" if base.appRunner else "models/")+"cursors/main_cursor.png")
        self.alghtnode = AmbientLight("ambient light"); self.alghtnode.setColor(Vec4(0.4,0.4,0.4,1))
        self.voile = DirectFrame(frameSize=(-2,2,-2,2),frameColor=(0,0,0,0.8)); self.voile.setBin("gui-popup",1); self.voile.hide()
        cust_path = ("" if base.appRunner else "mainscene/models/")
        self.arrow_mod = loader.loadModel(cust_path+"statics/arrow")
        self.card_arrow = CardMaker("arrow_hide"); self.card_arrow.setFrame(-1,1,-0.8,0.6)
        self.mouse_trav = CollisionTraverser(); self.mouse_hand = CollisionHandlerQueue()
        self.pickerNode = CollisionNode("mouseRay"); self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1)); self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay); self.mouse_trav.addCollider(self.pickerNP,self.mouse_hand)
        self.curdir = (base.appRunner.p3dFilename.getDirname() if base.appRunner else ".")
        self.initScreen(); self.change_cursor("blank"); self.transit = None
        self.main_config = None; self.speak = None; self.scene = mainScene(self); self.scene.request("Init")
    	base.mouseWatcherNode.setGeometry(self.cust_mouse.node())
    def clearScreen(self):
        self.cust_mouse.removeNode(); render.clearLight(self.alght); self.alght.removeNode(); self.pickly_node.removeNode()
    def initScreen(self,x=640,y=480):
    	x = (640.0/x) * 0.1; y = (480.0/y) * -0.13
        cm = CardMaker("cursor"); cm.setFrame(0,x,y,0); self.cust_mouse = render.attachNewNode(cm.generate())
        self.cust_mouse.setTransparency(TransparencyAttrib.MAlpha)
        self.cust_mouse.reparentTo(render2d); self.cust_mouse.setBin("gui-popup",100)
        self.alght = render.attachNewNode(self.alghtnode); render.setLight(self.alght)
        self.pickly_node = render.attachNewNode("pickly_node")
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
    def main_screen(self):
        self.scene.close(); self.scene = None; self.clearScreen()
        wp = WindowProperties()
        if self.main_config["fullscreen"]: wp.setFullscreen(False)
        wp.setSize(640,480); base.openMainWindow(wp,makeCamera=False,keepCamera=True)
        self.initScreen(); self.change_cursor("blank"); self.scene = mainScene(self); self.scene.request("Init")
        base.mouseWatcherNode.setGeometry(self.cust_mouse.node())
    def game_screen(self):
        self.scene.close(); self.scene = None; self.clearScreen();
        x = 950; y = 700; wp = WindowProperties()
        if self.main_config["fullscreen"]:
            di = base.pipe.getDisplayInformation()
            for index in range(di.getTotalDisplayModes()):
                tmp_width = di.getDisplayModeWidth(index); tmp_height = di.getDisplayModeHeight(index)
                if (float(tmp_width)/tmp_height) > 1 and (float(tmp_width)/tmp_height) < 2:
                    wp.setSize(tmp_width,tmp_height); x = tmp_width; y = tmp_height; break
            wp.setFullscreen(True)
        elif not self.main_config["fullscreen"]: wp.setSize(950,700)
        base.openMainWindow(wp,makeCamera=False,keepCamera=True)
        self.initScreen(x,y); self.change_cursor("main"); self.scene = gameScene(self); self.scene.request("Init")
        base.mouseWatcherNode.setGeometry(self.cust_mouse.node())

app = ArcnsApp(); run()
