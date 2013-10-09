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
from arcstools.arcstools import arcsTools

import direct.directbase.DirectStart

class ArcnsApp(DirectObject):
    def __init__(self):
    	base.disableMouse(); base.setBackgroundColor(1,1,1)
    	self.arcFont = base.loader.loadFont(("" if base.appRunner else "misc/")+"firstv2.ttf")
        self.cust_mouse_tex = {}
        self.cust_mouse_tex["blank"] = loader.loadTexture(("" if base.appRunner else "models/")+"cursors/blank_cursor.png")
        self.cust_mouse_tex["main"] = loader.loadTexture(("" if base.appRunner else "models/")+"cursors/main_cursor.png")
        self.alghtnode = AmbientLight("ambient light"); self.alghtnode.setColor(Vec4(0.4,0.4,0.4,1))
        self.voile = DirectFrame(frameSize=(-2,2,-2,2),frameColor=(1,1,1,0.7)); self.voile.setBin("gui-popup",1); self.voile.hide()
        cust_path = ("" if base.appRunner else "mainscene/models/")
        self.arrow_mod = loader.loadModel(cust_path+"statics/arrow")
        self.card_arrow = CardMaker("arrow_hide"); self.card_arrow.setFrame(-1.1,1,-0.8,0.8); self.card_arrow.setColor(1,0,0,1)
        self.mouse_trav = CollisionTraverser(); self.mouse_hand = CollisionHandlerQueue()
        self.pickerNode = CollisionNode("mouseRay"); self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1)); self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay); self.mouse_trav.addCollider(self.pickerNP,self.mouse_hand)
        self.curdir = (base.appRunner.p3dFilename.getDirname() if base.appRunner else ".")
        self.tools = arcsTools(); self.initScreen(); self.change_cursor("blank"); self.transit = None
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
    def arcButton(self,txt,pos,cmd,scale=0.08,txtalgn=TextNode.ALeft,extraArgs=[],sound=None): #override button
        ndp = DirectButton(text=txt,scale=scale,text_font=self.arcFont,pos=pos,text_shadow=(0,0.5,1,0.8),
            relief=None,text_align=txtalgn,extraArgs=extraArgs,text_shadowOffset=(0.07,0.07),clickSound=sound)
        ndp._DirectGuiBase__componentInfo["text2"][0].setFg((0.03,0.3,0.8,1))
        ndp._DirectGuiBase__componentInfo["text3"][0].setFg((0.3,0.3,0.3,1))
        ndp["command"] = cmd; return ndp
    def arcLabel(self,txt,pos,scale=0.08,txtalgn=TextNode.ALeft): #override label
        ndp = DirectLabel(text=txt,scale=scale,pos=pos,relief=None,text_font=self.arcFont,text_align=txtalgn,
            text_shadow=(0,0.5,1,0.8),text_shadowOffset=(0.07,0.07))
        return ndp
    def arcOptMenu(self,txt,pos,items,init=0,cmd=None,scale=0.08,change=1,txtalgn=TextNode.ALeft,extraArgs=[]): # override options menu
        ndp = DirectOptionMenu(text=txt,scale=scale,pos=pos,items=items,initialitem=init,textMayChange=change,text_font=self.arcFont,
            text_align=txtalgn,text_shadow=(0,0.5,1,0.8),text_shadowOffset=(0.07,0.07),popupMarker_scale=1.4,popupMarker_frameColor=(1,1,1,1),
            relief=None,highlightColor=(0.02,0.5,1,0.8),popupMarker_relief=DGG.RIDGE,item_frameColor=(1,1,1,0.7),item_relief=DGG.RIDGE,
            popupMarker_pos=(0,0,0),popupMarkerBorder=(0.5,0.5),item_text_font=self.arcFont,extraArgs=extraArgs)
        ndp["command"] = cmd; return ndp
    def arcRadioButton(self,lst_rad,parent,gui,scale=0.08,txtalgn=TextNode.ALeft): #override radio button
        lst_radio = []
        for elt in lst_rad:
            ndp = DirectRadioButton(text=elt[0],variable=elt[1],value=elt[2],extraArgs=elt[4],text_shadowOffset=(0.07,0.07),
                boxImageColor=(1,1,1,0.8),text_align=txtalgn,scale=scale,boxBorder=0.2,
                pos=elt[5],text_font=self.arcFont,text_shadow=(0,0.5,1,0.8),relief=None)
            ndp["command"] = elt[3]; ndp.reparentTo(parent); gui[elt[6]] = ndp; lst_radio.append(ndp)
        for elt in lst_radio: elt.setOthers(lst_radio)
    def arcCheckButton(self,txt,pos,cmd,scale=0.08,boxplct="left",txtalgn=TextNode.ALeft,extraArgs=[]): #override check button
        ndp = DirectCheckButton(text=txt,scale=scale,pos=pos,text_font=self.arcFont,text_align=txtalgn,relief=None,
            boxRelief=DGG.RIDGE,text_shadow=(0,0.5,1,0.8),text_shadowOffset=(0.07,0.07),boxPlacement=boxplct,extraArgs=extraArgs)
        ndp["command"] = cmd; return ndp
    def arcEntry(self,pos,txt="",cmd=None,scale=0.08,nlines=1): #override entry
        ndp = DirectEntry(pos=pos,initialText=txt,scale=scale,numLines=nlines,entryFont=self.arcFont,frameColor=(1,1,1,0.8),relief=DGG.RIDGE)
        ndp["command"] = cmd; return ndp
    def arcSlider(self,pos,scale=1,inter=(0,100),initVal=50,pas=1,cmd=None,orient=DGG.HORIZONTAL): #override slider
        calc_size = None; calc_text = None; calc_pos = None
        if orient == DGG.HORIZONTAL:
            calc_size = (scale*-0.5,scale*0.5,scale*0.1,scale*-0.1); calc_text = "|"; calc_pos = (0,scale*-0.033-0.0035)
        elif orient == DGG.VERTICAL:
            calc_size = (scale*-0.1,scale*0.1,scale*0.5,scale*-0.5); calc_text = "_"; calc_pos = (-0.01*scale,0)
        ndp = DirectSlider(pos=pos,range=inter, value=initVal, pageSize=pas,orientation=orient,frameColor=(0,0.5,1,1),
            frameSize=calc_size,thumb_relief=DGG.RIDGE,thumb_text=calc_text,thumb_text_scale=scale*0.12,
            thumb_text_fg=(1,1,1,1),thumb_borderWidth=(0.01,0.01),thumb_text_pos=calc_pos,thumb_frameColor=(1,1,1,1))
    	ndp["command"] = cmd; return ndp
    def arcScrollBar(self,pos,scale=1,inter=(0,1),val=0.5,pas=0.1,cmd=None,orient=DGG.HORIZONTAL): #override scrollbar
        ndp = DirectScrollBar(pos=pos,range=inter,value=val,pageSize=pas,orientation=orient,frameColor=(0,0.5,1,1),
            thumb_relief=DGG.RIDGE,thumb_borderWidth=(0.01,0.01),decButton_relief=DGG.RIDGE,incButton_relief=DGG.RIDGE,
            thumb_frameColor=(1,1,1,1),decButton_frameColor=(1,1,1,1),incButton_frameColor=(1,1,1,1),
            decButton_borderWidth=(0.01,0.01),incButton_borderWidth=(0.01,0.01),decButton_text="-",incButton_text="+",
            decButton_text_scale=scale*0.12,incButton_text_scale=scale*0.12,scale=scale,
            decButton_text_pos=(-0.005*scale,-0.025*scale),incButton_text_pos=(-0.005*scale,-0.02*scale))
        ndp["command"] = cmd; return ndp
    def arcWaitBar(self,pos,scale=1,range=100,val=50,text=""):
        ndp = DirectWaitBar(pos=pos,text=text,range=range,value=val,scale=scale,text_font=self.arcFont,
            text_shadow=(1,1,1,0.8),text_shadowOffset=(0.07,0.07),relief=DGG.RIDGE,barRelief=DGG.RIDGE,
            barBorderWidth=(0.01,0.01),borderWidth=(0.01,0.01),frameColor=(1,1,1,1),barColor=(0,0.5,1,1))
        return ndp
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
    def crea_persoscene(self):
        return persoScene()

app = ArcnsApp(); run()
