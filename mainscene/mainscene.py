# -*- coding: utf-8 -*-

from direct.gui.OnscreenText import OnscreenText


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

"""
mainscene class
"""
class mainScene:
    def __init__(self,app):
        #
        self.app = app
        #
        #TODO : initialisation commands for the mainscene class
        #
        #
        #TEST
        print "mainscene start ..."
        #
        self.version = "v0.0"
        #
        self.app.arcLabel("test label",(0,0,0))
        #
        print "mainscene passed"
        #TEST
        #
        self.vers_txt = OnscreenText(text=self.version,font=self.app.arcFont,pos=(1.15,-0.95),fg=(0,0,0,1),bg=(1,1,1,0.8))
        #
