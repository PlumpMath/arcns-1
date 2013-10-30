# -*- coding: utf-8 -*-

from arcstools.arcstools import arcsTools
import sys
import direct.directbase.DirectStart

scene = None
if sys.argv[1] == "main":
    from mainscene import scenebuilder; scene = scenebuilder.mainscene_builder
elif sys.argv[1] == "game":
    #
    print "game"
    #
    sys.exit(0)
    #

builder = arcsTools()
builder.parse_scene(scene)

run()
