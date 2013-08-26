# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters
from direct.stdpy.file import *
from panda3d.core import Vec4, TextNode, CardMaker, NodePath, PandaNode, AmbientLight, LightRampAttrib
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32
from panda3d.core import WindowProperties
from pandac.PandaModules import TransparencyAttrib

import direct.directbase.DirectStart
import sys, json

class ArcnsApp(DirectObject):
    def __init__(self):
        self.accept("escape",sys.exit,[0]); base.setBackgroundColor(1,1,1)
        self.arcFont = base.loader.loadFont("firstv2.ttf")
        cm = CardMaker("cursor"); cm.setFrame(0,0.1,-0.13,0); self.cust_mouse = render.attachNewNode(cm.generate())
        self.cust_mouse_tex = {}
        self.cust_mouse_tex["blank"] = loader.loadTexture("cursors/blank_cursor.png")
        self.cust_mouse_tex["main"] = loader.loadTexture("cursors/main_cursor.png")
        self.change_cursor("blank"); self.cust_mouse.setTransparency(TransparencyAttrib.MAlpha)
        self.cust_mouse.reparentTo(render2d); self.cust_mouse.setBin("gui-popup",100)
        base.mouseWatcherNode.setGeometry(self.cust_mouse.node())
        self.curdir = base.appRunner.p3dFilename.getDirname()
        if exists(self.curdir+"/config.json"):
            self.main_config = json.loads("".join([line.rstrip().lstrip() for line in file(self.curdir+"/config.json","rb")]))
        else:
            #
            self.main_config = {
                "size":["640x480","800x600","1024x768","1152x864","1280x960","1280x1024","1440x900"],
                "lang":[["fr","Français"],["en","English"]],"fullscreen":False,
                "lang_chx":0,"size_chx":1}
            #
            #TODO : vérifier s'il n'y a pas quelque chose à rajouter
            #
            try: mcf = open(self.curdir+"/config.json","w"); mcf.write(json.dumps(self.main_config)); mcf.close()
            except Exception,e: print e
        self.rampnode = NodePath(PandaNode("ramp node"))
        self.rampnode.setAttrib(LightRampAttrib.makeSingleThreshold(0.1,0.7))
        self.rampnode.setShaderAuto()
        base.cam.node().setInitialState(self.rampnode.getState())
        self.filters = CommonFilters(base.win,base.cam)
        self.filterok = self.filters.setCartoonInk(separation=1)
        self.alghtnode = AmbientLight("ambient light"); self.alghtnode.setColor(Vec4(0.4,0.4,0.4,1))
        self.alght = render.attachNewNode(self.alghtnode); render.setLight(self.alght)
        #
        #
        self.voile = {}; self.voile["frame"] = DirectFrame(frameSize=(-2,2,-2,2),frameColor=(0,0,0,0.8))
        self.voile["frame"].setBin("gui-popup",1); self.voile["frame"].hide()
        self.voile["lab1"] = self.arcLabel("",(0,0,0.3),txtalgn=TextNode.ACenter)
        self.voile["lab1"].setBin("gui-popup",1); self.voile["lab1"].reparentTo(self.voile["frame"])
        self.voile["lab2"] = self.arcLabel("",(0,0,0.17),txtalgn=TextNode.ACenter)
        self.voile["lab2"].setBin("gui-popup",1); self.voile["lab2"].reparentTo(self.voile["frame"])
        self.voile["btn_g"] = self.arcButton("",(-0.3,0,0),None,txtalgn=TextNode.ACenter)
        self.voile["btn_g"].setBin("gui-popup",1); self.voile["btn_g"].reparentTo(self.voile["frame"])
        self.voile["btn_d"] = self.arcButton("",(0.3,0,0),None,txtalgn=TextNode.ACenter)
        self.voile["btn_d"].setBin("gui-popup",1); self.voile["btn_d"].reparentTo(self.voile["frame"])
        #
        #
        self.mouse_trav = CollisionTraverser(); self.mouse_hand = CollisionHandlerQueue()
        self.pickerNode = CollisionNode("mouseRay"); self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1)); self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay); self.mouse_trav.addCollider(self.pickerNP,self.mouse_hand)
        self.pickly_node = render.attachNewNode("pickly_node")
        #
        from mainscene.mainscene import mainScene
        #
        from cinematic.cinescene import cineScene
        #
        from gamescene.gamescene import gameScene
        #
        #TEST
        #
        print base
        #
        di = base.pipe.getDisplayInformation()
        #
        print "max window width : "+str(di.getMaximumWindowWidth())
        print "max window height : "+str(di.getMaximumWindowHeight())
        #
        for index in range(di.getTotalDisplayModes()):
            #
            print str(di.getDisplayModeWidth(index))+" : "+str(di.getDisplayModeHeight(index))
            #
            #sizes += (di.getDisplayModeWidth(index), di.getDisplayModeHeight(index))
        #
        print di.getDisplayState()
        #
        self.fullscreen = False
        self.accept("w",self.changefullscreen)
        #TEST
        #
        #
        #
        self.scene = mainScene(self)
    #TEST
    def changefullscreen(self):
        #
        di = base.pipe.getDisplayInformation()
        #
        print "changefullscreen"
        #
        self.fullscreen = (False if self.fullscreen else True)
        #
        wp = WindowProperties()
        #
        wp.setSize(di.getDisplayModeWidth(0),di.getDisplayModeHeight(0))
        #
        wp.setFullscreen(self.fullscreen)
        #
        base.win.requestProperties(wp)
        #
    #TEST
    def change_cursor(self,chx):
        self.cust_mouse.setTexture(self.cust_mouse_tex[chx])
    def arcButton(self,txt,pos,cmd,scale=0.08,txtalgn=TextNode.ALeft,extraArgs=[]): #override button
        ndp = DirectButton(text=txt,scale=scale,text_font=self.arcFont,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_align=txtalgn,
            command=cmd,extraArgs=extraArgs)
        ndp._DirectGuiBase__componentInfo["text2"][0].setFg((0.03,0.3,0.8,1))
        ndp._DirectGuiBase__componentInfo["text3"][0].setFg((0.3,0.3,0.3,1))
        return ndp
    def arcLabel(self,txt,pos,scale=0.08,txtalgn=TextNode.ALeft): #override label
        ndp = DirectLabel(text=txt,scale=scale,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_font=self.arcFont,text_align=txtalgn)
        return ndp
    def arcOptMenu(self,txt,pos,items,init=0,cmd=None,scale=0.08,change=1,txtalgn=TextNode.ALeft,extraArgs=[]):
        ndp = DirectOptionMenu(text=txt,scale=scale,pos=pos,items=items,initialitem=init,textMayChange=change,text_font=self.arcFont,
            text_align=txtalgn,text_bg=(1,1,1,0.8),relief=None,highlightColor=(0.03,0.3,0.8,1),popupMarker_relief=None,
            popupMarker_pos=(0,0,0),popupMarkerBorder=(0,0),item_text_font=self.arcFont,command=cmd,extraArgs=extraArgs)
        return ndp
    def arcRadioButton(self,lst_rad,parent,gui,scale=0.08,txtalgn=TextNode.ALeft): #override radio button
        lst_radio = []
        for elt in lst_rad:
            ndp = DirectRadioButton(text=elt[0],variable=elt[1],value=elt[2],command=elt[3],extraArgs=elt[4],
                text_align=txtalgn,scale=scale,pos=elt[5],text_font=self.arcFont,text_bg=(1,1,1,0.8),relief=None)
            lst_radio.append(ndp)
        for elt in lst_radio:
            elt.setOthers(lst_radio); elt.reparentTo(parent); gui.append(elt)
    def arcEntry(self,pos,txt="",cmd=None,scale=0.08,nlines=1): #override entry
        ndp = DirectEntry(pos=pos,text=txt,command=cmd,scale=scale,numLines=nlines,entryFont=self.arcFont,frameColor=(1,1,1,0.8),relief=DGG.RIDGE)
        return ndp
    def change_screen(self):
        wp = WindowProperties()
        #
        wp.setSize(200,200)
        #
        base.win.requestProperties(wp)


app = ArcnsApp(); run()
