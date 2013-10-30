# -*- coding: utf-8 -*-

mainscene_builder = {
    "statics":{
        "sol":{
            "mainscene/models/statics/dalle_grille_001":[
                [(0,0,0),(90,0,0)],[(0,1,0),(-90,0,0)],[(1,0,0),(90,0,0)],[(1,1,0),(-90,0,0)],
                [(-1,0,0),(90,0,0)],[(-1,1,0),(-90,0,0)]
            ],
            "mainscene/models/statics/socle_base":[]
        },
        "bords":{
            "nord":{
                "mainscene/models/statics/bord_basique_001":[]
            },
            "sud":{},
            "est":{},
            "ouest":{}
        },
        "murs":{
            "nord":{},
            "sud":{},
            "est":{},
            "ouest":{}
        },
        "decors":{
            "nord":{},
            "sud":{},
            "est":{},
            "ouest":{}
        }
    },
    "dynamics":{
        "spawners":{}
    },
    "lights":[[1,(0.6,0.6,0.6,1),(0,0,0),(0,-30,0),True,None,"dir_face"],[1,(0.5,0.5,0.5,1),(0,0,0),(0,200,0),True,None,"dir_top"],
        [0,(0.8,0.8,0.8,1),(-8,0,9),(6,-0.5,-1.5),True,None,"spot_aux_menu"]]
}
