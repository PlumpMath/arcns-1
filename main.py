# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties

import direct.directbase.DirectStart
import sys

class ArcnsApp(DirectObject):
    def __init__(self):
        #
        self.accept("escape",sys.exit,[0])
        #
        #wp = WindowProperties(); wp.setSize(200,200); base.win.requestProperties(wp)
        #
        OnscreenText(text="test1",pos=(0,0,0),fg=(0,0,0,1),bg=(1,1,1,0.8))
        print "good"
        try:
            from test1.firstClassTest import firstClassTest
            print "test inter"
            tst = firstClassTest()
        except Exception,e:
            print e

app = ArcnsApp()
run()
