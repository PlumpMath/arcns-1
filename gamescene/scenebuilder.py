# -*- coding: utf-8 -*-

gamescene_builder = {}

gamescene_builder["firstbase"] = {
    "statics":{
        "sol":{
            "mainscene/models/statics/socle_base":[
                [(0,0,0),(0,0,0)],[(1,0,0),(0,0,0)],[(0,1,0),(0,0,0)],[(-1,0,0),(0,0,0)],[(0,-1,0),(0,0,0)]
            ]
        },
        "bords":{
            "nord":{},
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
    "lights":[
        [1,(0,0,0),(0,-10,0),True,camera,"gates_light"]
        #[(0,0,0),0,0,0]
    ]
}
