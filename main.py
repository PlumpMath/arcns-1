# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import Point3, Vec4, Vec3, BitMask32, NodePath, PandaNode, TextNode
from panda3d.core import WindowProperties

"""
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.filter.CommonFilters import CommonFilters
from direct.stdpy.file import *
from panda3d.core import PointLight, DirectionalLight, Spotlight, AmbientLight, PerspectiveLens
from panda3d.core import LightRampAttrib, WindowProperties, Filename, CardMaker
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay
from panda3d.core import Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomPrimitive, GeomTriangles
from pandac.PandaModules import TransparencyAttrib

import direct.directbase.DirectStart
import math, os, sys, json, time
"""

import direct.directbase.DirectStart
import sys

"""
override functions
"""
def arcButton(txt,pos,cmd,scale=0.08,txtalgn=TextNode.ALeft,extraArgs=[]): #override button
    ndp = DirectButton(text=txt,scale=scale,text_font=arcFont,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_align=txtalgn,
        command=cmd,extraArgs=extraArgs)
    ndp._DirectGuiBase__componentInfo["text2"][0].setFg((0.03,0.3,0.8,1))
    ndp._DirectGuiBase__componentInfo["text3"][0].setFg((0.3,0.3,0.3,1))
    return ndp

def arcLabel(txt,pos,scale=0.08,txtalgn=TextNode.ALeft): #override label
    ndp = DirectLabel(text=txt,scale=scale,pos=pos,text_bg=(1,1,1,0.8),relief=None,text_font=arcFont,text_align=txtalgn)
    return ndp

def arcOptMenu(txt,pos,items,init=0,cmd=None,scale=0.08,change=1,txtalgn=TextNode.ALeft,extraArgs=[]):
    ndp = DirectOptionMenu(text=txt,scale=scale,pos=pos,items=items,initialitem=init,textMayChange=change,text_font=arcFont,
        text_align=txtalgn,text_bg=(1,1,1,0.8),relief=None,highlightColor=(0.03,0.3,0.8,1),popupMarker_relief=None,
        popupMarker_pos=(0,0,0),popupMarkerBorder=(0,0),item_text_font=arcFont,command=cmd,extraArgs=extraArgs)
    return ndp

def arcRadioButton(lst_rad,parent,gui,scale=0.08,txtalgn=TextNode.ALeft): #override radio button
    lst_radio = []
    for elt in lst_rad:
        ndp = DirectRadioButton(text=elt[0],variable=elt[1],value=elt[2],command=elt[3],extraArgs=elt[4],
            text_align=txtalgn,scale=scale,pos=elt[5],text_font=arcFont,text_bg=(1,1,1,0.8),relief=None)
        lst_radio.append(ndp)
    for elt in lst_radio:
        elt.setOthers(lst_radio); elt.reparentTo(parent); gui.append(elt)

def arcEntry(pos,txt="",cmd=None,scale=0.08,nlines=1): #override entry
    ndp = DirectEntry(pos=pos,text=txt,command=cmd,scale=scale,numLines=nlines,entryFont=arcFont,frameColor=(1,1,1,0.8),relief=DGG.RIDGE)
    return ndp

"""
main class
"""
class ArcnsApp(DirectObject):
    def __init__(self):
        #
        #TEST
        self.accept("escape",sys.exit,[0])
        #
        #wp = WindowProperties(); wp.setSize(200,200); base.win.requestProperties(wp)
        #
        OnscreenText(text="test1",pos=(0,0,0),fg=(0,0,0,1),bg=(1,1,1,0.8))
        print "good"
        #
        #from direct.p3d.PackageInfo import PackageInfo
        #
        #
        #
        #TEST
        #

app = ArcnsApp()
run()
