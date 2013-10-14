# -*- coding: utf-8 -*-

from panda3d.core import Multifile, Filename

import os, py_compile

if not os.path.exists("arcns_mfs"): os.mkdir("arcns_mfs")

def crea_mf(name):
    if os.path.exists("arcns_mfs/"+name+".mf"):
        if os.stat(name).st_mtime <= os.stat("arcns_mfs/"+name+".mf").st_mtime: return
        else: os.unlink("arcns_mfs/"+name+".mf")
    mf = Multifile(); mf.openWrite("arcns_mfs/"+name+".mf")
    for root,dirs,files in os.walk(name):
        for f in files:
            if f[-1] == "~" or f[-3:] == "pyc" or f[-3:] == "pyo" or f[-3:] == "bam": pass
            elif f[-2:] == "py":
                if os.path.exists(f+"o") and os.stat(f).st_mtime <= os.stat(f+"o").st_mtime: pass
                else:
                    py_compile.compile(root+"/"+f); fln = Filename(root+"/"+f+"o"); fln.set_binary(); mf.addSubfile(root+"/"+f+"o",fln,6)
            elif f[-3:] == "egg":
                if os.path.exists(root+"/"+f[:-3]+"bam") and os.stat(root+"/"+f).st_mtime <= os.stat(root+"/"+f[:-3]+"bam").st_mtime: pass
                else:
                    if os.path.exists(root+"/"+f[:-3]+"bam"): os.unlink(root+"/"+f[:-3]+"bam")
                    os.system("egg2bam -o "+root+"/"+f[:-3]+"bam "+root+"/"+f)
                fln = Filename(root+"/"+f[:-3]+"bam"); fln.set_binary(); mf.addSubfile(root+"/"+f[:-3]+"bam",fln,6)
            elif f[-3:] == "wav":
                fln = Filename(root+"/"+f); fln.set_binary(); mf.addSubfile(root+"/"+f,fln,6)
            #
            # TODO : ajouter des formats
            #
    mf.close()

crea_mf("mainscene")
crea_mf("gamescene")
crea_mf("persoscene")
crea_mf("arcstools")

