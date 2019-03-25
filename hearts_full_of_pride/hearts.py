#!/usr/bin/env python
# coding: utf-8

# In[47]:


import json
import math
import os
import glob

import numpy as np

import cairosvg

from uuid import uuid4

from vdom import VDOM, style
from vdom.svg import circle, path, rect, svg, g as group, animate, text, clipPath

from IPython.display import display_png, Image, SVG


# In[48]:

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
FLAG_JSON_FILENAME = os.path.join(BASE_DIR, "flag_spec.json")
HEART_ARRAY_JSON_FILENAME = os.path.join(BASE_DIR, "heart_coords.json")

def gen_id():
    return f"{uuid4()}".replace("-","")

def gen_heart(myid=None, stroke="red"):
    if myid is None:
        myid = gen_id()
    with open('heart_quads.json') as fp:
        data =json.load(fp)
    quads = data['quad_points']
    initial_point = data['initial_point']
    
    d = f'M{initial_point[0]},{initial_point[1]} {" ".join("Q"+",".join(map(str, (q for q in quad[0])))+" "+",".join(map(str, (q for q in quad[1]))) for quad in quads)} Z'
    my_heart = path(id=f"{myid}",
                    fill="none", 
                    stroke=stroke,
                    d=d,
                    transform = "scale(1.25 -1.25)",
                    **{"stroke-width": ".5"}
        )    
    return my_heart


# In[49]:


class Flag:
    def __init__(self, name, colors, symbol=None):
        self.name = name
        self.colors = colors
        self.symbol = symbol
        self.num = len(colors)
        
    def flag(self, height_perc=73, shift=5, **kwargs):
        height_perc = height_perc
        shift = shift
        div_heights = np.linspace(-height_perc/2+shift,
                                  height_perc/2+shift, 
                                  self.num, 
                                  endpoint=False)
        internal = [rect(x="-25", y=f"{this_h}%", 
                         width="50", height=f"{height_perc/self.num}%", 
                         fill=self.colors[i],
                         stroke=self.colors[i]
                        ) 
                    for i, this_h in enumerate(div_heights)]
        if self.symbol:
            internal.append(self.symbol)
        return group(*internal, 
                     **kwargs, )
    
    def _repr_mimebundle_(self, include=None, exclude=None):
        viewer = svg(self.flag(), viewBox="-25 -25 50 50", 
                     version="1.1", baseProfile="full", width="300px", height="200px", 
                     xmlns="http://www.w3.org/2000/svg", 
                     x="0px", y="0px",
                     **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
                        "xml:space":"preserve"})
        return {**viewer._repr_mimebundle_(None, None),
                "text/html": viewer._repr_html_(),
                "image/svg+xml": viewer._repr_html_()
               }
    
    def encode(self, **kwargs):
        myflag = svg(self.flag(**kwargs),
                     viewBox="-25 -25 50 50",
                     version="1.1",
                     baseProfile="full",
                     xmlns="http://www.w3.org/2000/svg",
                     **{"xmlns:xlink": "http://www.w3.org/1999/xlink",
                        "xml:space": "preserve"})
        return myflag.to_html().encode('utf-8')
    
        
    
class Clip:

    def __init__(self, *shapes, clipid="clipid", **kwargs):
        self.clipid = clipid
        self.shapes = shapes
        self.kwargs = kwargs
    
    def clipper(self):
        return clipPath(*self.shapes, 
                        **{"id":self.clipid}, **self.kwargs)
    
    def clip(self, *targets, **kwargs):
        return group(*targets, style={"clip-path":f"url(#{self.clipid})"})
    
    def show_clip(self, *targets, edge=False, clip=True, style = None, **kwargs):
        if style is not None:
            style = {}

        outline = self.shapes if edge else [""]
        to_display = [self.clip(*targets, **kwargs)] if clip else targets
        
        return svg(*to_display,
                   *outline,
                   viewBox="-25 -25 50 50", version="1.1",
            baseProfile="full", 
            xmlns="http://www.w3.org/2000/svg", 
            **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
               "xml:space":"preserve"})

    
def encode_heart(flag_def, **kwargs):
    heart_shape = Clip(gen_heart(), clipid="uniquid")
    heart = svg(heart_shape.clipper(),
                heart_shape.clip(Flag(**flag_def).flag()),
                viewBox="-25 -25 50 50", 
                version="1.1",
            baseProfile="full", 
            xmlns="http://www.w3.org/2000/svg", 
            **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
               "xml:space":"preserve"}) 

    return heart.to_html().encode('utf-8')

def encode_flag(flag_def, **kwargs):
    return Flag(**flag_def).encode()


def gen_heart_array(flag_defs):
    heart = Clip(gen_heart(), clipid="newid")
    heart_coords = load_heart_coords()
    flag_list = [heart.clipper()]
    coord_list = []

    for idx, flag_def in enumerate(flag_defs):
        x = f"{heart_coords[idx]['x']}"
        y = f"{int(heart_coords[idx]['y'])+50}"
        flag = Flag(**flag_def)
        flag_list.append(
            svg(
                text(flag.name, y=f"{-20}", **{'text-anchor': "middle", "font-family": "Minion Pro", "font-size":"15"}),
                heart.clip(
                    flag.flag(),
                ), 
                x = x,
                y = y,
                height="100px",
                viewBox="-25 -25 50 50",
                style={"overflow":"visible"},
                version="1.1",
                baseProfile="full", 
                xmlns="http://www.w3.org/2000/svg", 
                **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
                   "xml:space":"preserve"}
            )
        )    
    heart_array = svg(*flag_list, width=f"{90*8}", viewBox="250 0 675 675", 
                      version="1.1", baseProfile="full", 
                      xmlns="http://www.w3.org/2000/svg", 
                      **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
                            "xml:space":"preserve"})
    return heart_array

def write_pngs(flag_defs, base_dir=None, suffix="heart", encoder=None):
    if encoder is None:
        encoder = encode_heart
    if base_dir is None:
        base_dir = os.path.join("images", "pngs")

    for flag in flag_defs:
        with open(f"{os.path.join(base_dir,flag['name'])}-{suffix}.png", 'wb') as fp:
            fp.write(cairosvg.svg2png(encoder(flag), dpi=300, parent_width=400, parent_height=400))




def load_heart_coords():
    with open(HEART_ARRAY_JSON_FILENAME, "r") as fp:
        heart_coords_json = json.load(fp)
        return heart_coords_json['heart_coords']



# In[53]:


# %%writefile flag_spec.py
# trans = {"colors":['lightskyblue', 'lightpink', 'white',  'lightpink', 'lightskyblue'],
#          "name":"trans",}

# intersex = {"colors":["gold"],
#             "name": "intersex",}
# intersex['symbol'] = circle(cx="0", cy="2", r="5", fill="transparent", 
#                             stroke="purple", **{"stroke-width":"2.5"})

# genderqueer = {"colors":['purple', 'white', 'forestgreen'],
#                "name": "genderqueer",}

# pride = {"colors":['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black'], 
#          "name": "pride",}

# agender = {"colors":['black', 'lightgrey', 'white', 'chartreuse', 'white', 'lightgrey', 'black'],
#            "name": "agender",}

# ace = {"colors":['black','lightgrey','white', 'purple'], 
#        "name": "asexual", }

# bi = {"colors":['deeppink', 'deeppink', 'mediumpurple', 'blue','blue'],
#       "name": "bi",}

# enby = {"colors":['#ffef00', 'white', '#9C59D1', 'black'], 
#         "name": "enby",}

# genderfluid = {"colors":['#ff75a2', "white","#be18d6", 'black', 'mediumblue'],
#                "name": "genderfluid",}

# pansexual = {"colors":['deeppink', "gold", "deepskyblue"],
#              "name": "pansexual",}

# polysexual = {"colors":["#f61cb9", "#07d569", 'dodgerblue'],
#               "name": "polysexual",}

# aromantic = {"colors":["#3da542", "#a7d379", "white", "lightgrey", "black"],
#              "name": "aromantic",}

# lipstick = {"colors":["#A60061", "#B95393", "#D260A7", "#EDEDEB", "#E5ABD0", "#C74D52", "#8C1D00"], 
#             "name": "lipstick",}

# polyamory = {"colors":["blue", "red", "black"],
#              "name": "polyamory",}

# bear = {"colors": ["#623804", "chocolate", "#fedd63", "moccasin", "white", "dimgray", "black"], 
#         "name": "bear",}

# lesbian = {"colors":["purple"],
#            "name": "lesbian",}

# polyamory['symbol'] = text("π", y="4.5", fill="yellow", 
#                            **{'text-anchor': "middle", "font-family": "Minion Pro", "font-size":"15"})
# bear['symbol'] = path(d="M98.9 24.4c-5.7 0-11.5 1.3-16.3 4.4C61.2 42.6 91.1 48.3 96 51.1c4.7 2.7 22.4 22.9 29.7-8.4 2.2-9.7-12.2-18.3-26.8-18.3m45.4 11.2c-17.7 1.9-.8 43 23.6 44.4 16.5.9 28.9-39.3-23.6-44.4m-94.4 8.9C34.2 44 43.7 73.3 69 83.6c5.1 2.1 14.2-4.7 14.4-16 .1-4.2-7.1-22.2-33.5-23.1m61 17.7c-7.1-.1-14.6 3-22.8 11.5-28.9 30.3 13.8 35.5 10.6 51.9-9.7 48.5-.9 52.5 8.3 55.6 11.7 3.9 33.8-33.4 43.1-40.4 12.4-9.4 77.9-42.2 62.4-58.8-22.3-23.8-27 7.3-57.7-1-14.6-3.9-28.3-18.8-43.9-18.8M54.4 96.5c-2.8-.1-5.5.4-8.1 1.6-11.5 5.2 10.8 36.5 20.9 37.4 12.4 1.1 17.4-8.9 17.6-14.7.3-7.6-15.4-24-30.4-24.3m4 46.7c-4.5.1-8 1.2-9.6 3.3-4.1 6.2 21.6 30.4 28.7 32 6.5 1.5 12.6-13 11.4-18.7-2.2-10.4-19.2-16.7-30.5-16.6",
#                       transform = "scale(.08 .08) translate(-120,-80) ") 
# lesbian['symbol'] = group(path(d="M500 550L211.325 50h577.35z", fill="black"),
#                           path(d="M479.667 132.374a162.687 162.687 0 0 1-108.732-62.373 162.687 162.687 0 0 0 0 198.075 162.687 162.687 0 0 1 108.732-62.373zm40.672 73.329a162.687 162.687 0 0 1 108.732 62.373 162.687 162.687 0 0 0 0-198.075 162.687 162.687 0 0 1-108.732 62.373zm-4.067-91.571a16.269 8.134 0 0 0-32.538 0v347.743a16.269 8.134 0 0 0 32.538 0z", 
#                                fill="white"), 
#                           transform = "scale(.04, .04) translate(-500 -150)")

# demigirl = {"colors":["darkgrey", "lightgrey", "lightpink","white", "lightpink", "lightgrey", "darkgrey"], "name": "demigirl"}
# demiboy = {"colors":["darkgrey", "lightgrey", "lightblue","white", "lightblue", "lightgrey", "darkgrey"], "name": "demiboy"}

# flag_json = {entry['name']: entry.to_json() for entry in flag_spec.flag_defs}


def write_flags(flag_defs, flag_json_filename=FLAG_JSON_FILENAME):
    flag_json = {}
    for entry in flag_defs:
        temp_entry = {}
        for key, value in entry.items():
            temp_entry[key] = value.to_json() if isinstance(value, VDOM) else value
        flag_json[entry['name']] = temp_entry
    with open(flag_json_filename, 'w') as fp:
        json.dump(flag_json, fp)


def load_flags_iter(flag_json_filename=FLAG_JSON_FILENAME):
    with open(flag_json_filename, 'r') as fp:
        loaded_json = json.load(fp)
    for name, flag in loaded_json.items():
        for key, value in flag.items():
            if key == "symbol":
                flag[key] = VDOM.from_dict(json.loads(value))
        yield name, flag


def load_flag_list(flag_json_filename=FLAG_JSON_FILENAME):
    return list(flag[1] for flag in load_flags_iter(flag_json_filename))


def load_flag_dict(flag_json_filename=FLAG_JSON_FILENAME):
    return dict(load_flags_iter(flag_json_filename))


def gen_animation_style():
    anim_style = style("""#blargh {
        stroke-dasharray: 400;
        stroke-dashoffset: 400;
        animation: dash 10s linear forwards;
        animation-delay: 2s
        }
        @keyframes dash {
          to {
            stroke-dashoffset: 100;
          }
        }
    """)

    start_anim = animate(attributeName="startOffset", 
                         dur=f"2s", 
                         repeatCount="indefinite",
                         begin="0s",
                         **{"from": "0%",
                            "to": "100%"}
                         ) 
    return {"anim_style": anim_style, "start_anim": start_anim}


def gen_fade_out():
    fade_out = animate(id="animation1",
                       attributeName="opacity",
                       dur="3s",
                       begin="6s",
                       fill="freeze",
                       **{"from": "1", "to": "0"}
                       )
    return fade_out


def animated_heart(stroke_color="white"):
    anim_styles = gen_animation_style()
    
    return group(gen_heart("blargh", stroke=stroke_color), anim_styles['anim_style'])



def animated_flag_heart(this_flag, stroke_color="grey"):
    # this_flag = flag_dict[this_flag_name]
    heart = Clip(gen_heart())
    fade_out = gen_fade_out()
    anim_flag_heart = svg(heart.clipper(),
                          heart.clip(Flag(**this_flag).flag()),
                          group(Flag(**this_flag).flag(**{"id": "myflag"}),
                          animated_heart(stroke_color=stroke_color),
                          fade_out),
                          viewBox="-25 -25 50 50",
                          height="450"
                          )
    return anim_flag_heart


# In[59]:


# animated_flag_heart("trans")


# In[ ]:
