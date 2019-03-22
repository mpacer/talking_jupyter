

```python
import json
import math
import os
import glob

import numpy as np

import cairosvg

from uuid import uuid4

from vdom.svg import circle, path, rect, svg, g as group, animate, text, clipPath

from IPython.display import display_png, Image
```


```python
with open('heart_quads.json') as fp:
    data =json.load(fp)
quads = data['quad_points']
initial_point = data['initial_point']
```


```python
def gen_id():
    return f"{uuid4()}".replace("-","")

def gen_heart(myid=None, stroke="red"):
    if myid is None:
        myid = gen_id()
    d = f'M{initial_point[0]},{initial_point[1]} {" ".join("Q"+",".join(map(str, (q for q in quad[0])))+" "+",".join(map(str, (q for q in quad[1]))) for quad in quads)} Z'
    my_heart = path(id=f"{myid}",
                    fill="none", 
                    stroke=stroke,
                    d=d,
                    transform = "scale(1.25 -1.25)",
                    **{"stroke-width": ".5"}
        )    
    return my_heart

```


```python
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
                     **kwargs)
    
    def _repr_mimebundle_(self, include=None, exclude=None):
        viewer = svg(self.flag(), viewBox="-25 -25 50 50", 
                     version="1.1", baseProfile="full", width="300", height="200", 
                     xmlns="http://www.w3.org/2000/svg", 
                     x="0px", y="0px",
                     **{"xmlns:xlink":"http://www.w3.org/1999/xlink", 
                        "xml:space":"preserve"})
        return {**viewer._repr_mimebundle_(None, None),
                
                "text/html": viewer._repr_html_(),
                "text/svg+xml": viewer._repr_html_()
               }
    
    def encode(self, **kwargs):
        myflag = svg(self.flag(**kwargs), viewBox="-25 -25 50 50")
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
                   viewBox="-25 -25 50 50")

    
def encode_heart(flag_def, **kwargs):
    heart_shape = Clip(gen_heart(), clipid="uniquid")
    heart = svg(heart_shape.clipper(),
                heart_shape.clip(Flag(**flag_def).flag()),
                viewBox="-25 -25 50 50") 

    return heart.to_html().encode('utf-8')

def encode_flag(flag_def, **kwargs):
    return Flag(**flag_def).encode()

def write_pngs(flag_defs, base_dir=None, suffix="heart", encoder=None):
    if encoder is None:
        encoder = encode_heart
    if base_dir is None:
        base_dir = os.path.join("images", "pngs")

    for flag in flag_defs:
        with open(f"{os.path.join(base_dir,flag['name'])}-{suffix}.png", 'wb') as fp:
            fp.write(cairosvg.svg2png(encoder(flag), dpi=300, parent_width=400, parent_height=400))

```


```python
import IPython.display

```


```python
IPython.display.SVG
```


```python
heart_coords = [
    {'x': "60", "y":"0"},
    {'x': "180", "y":"0"},
    {'x': "345", "y":"0"},
    {'x': "465", "y":"0"},
    {'x': "0", "y":"120"},
    {'x': "130", "y":"120"},
    {'x': "260", "y":"120"},
    {'x': "390", "y":"120"},
    {'x': "520", "y":"120"},
    {'x': "40", "y":"240"},
    {'x': "185", "y":"240"},
    {'x': "335", "y":"240"},
    {'x': "480", "y":"240"},
    {'x': "170", "y":"360"},
    {'x': "355", "y":"360"},
    {'x': "260", "y":"480"},
]
```


```python
# %%writefile flag_spec.py
trans = {"colors":['lightskyblue', 'lightpink', 'white',  'lightpink', 'lightskyblue'],
         "name":"trans",}

intersex = {"colors":["gold"],
            "name": "intersex",}
intersex['symbol'] = circle(cx="0", cy="2", r="5", fill="transparent", 
                            stroke="purple", **{"stroke-width":"2.5"})

genderqueer = {"colors":['purple', 'white', 'forestgreen'],
               "name": "genderqueer",}

pride = {"colors":['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black'], 
         "name": "pride",}

agender = {"colors":['black', 'lightgrey', 'white', 'chartreuse', 'white', 'lightgrey', 'black'],
           "name": "agender",}

ace = {"colors":['black','lightgrey','white', 'purple'], 
       "name": "asexual", }

bi = {"colors":['deeppink', 'deeppink', 'mediumpurple', 'blue','blue'],
      "name": "bi",}

enby = {"colors":['#ffef00', 'white', '#9C59D1', 'black'], 
        "name": "enby",}

genderfluid = {"colors":['#ff75a2', "white","#be18d6", 'black', 'mediumblue'],
               "name": "genderfluid",}

pansexual = {"colors":['deeppink', "gold", "deepskyblue"],
             "name": "pansexual",}

polysexual = {"colors":["#f61cb9", "#07d569", 'dodgerblue'],
              "name": "polysexual",}

aromantic = {"colors":["#3da542", "#a7d379", "white", "lightgrey", "black"],
             "name": "aromantic",}

lipstick = {"colors":["#A60061", "#B95393", "#D260A7", "#EDEDEB", "#E5ABD0", "#C74D52", "#8C1D00"], 
            "name": "lipstick",}



polyamory = {"colors":["blue", "red", "black"],
             "name": "polyamory",}

bear = {"colors": ["#623804", "chocolate", "#fedd63", "moccasin", "white", "dimgray", "black"], 
        "name": "bear",}

lesbian = {"colors":["purple"],
           "name": "lesbian",}

polyamory['symbol'] = text("π", y="4.5", fill="yellow", 
                           **{'text-anchor': "middle", "font-family": "Minion Pro", "font-size":"15"})
bear['symbol'] = path(d="M98.9 24.4c-5.7 0-11.5 1.3-16.3 4.4C61.2 42.6 91.1 48.3 96 51.1c4.7 2.7 22.4 22.9 29.7-8.4 2.2-9.7-12.2-18.3-26.8-18.3m45.4 11.2c-17.7 1.9-.8 43 23.6 44.4 16.5.9 28.9-39.3-23.6-44.4m-94.4 8.9C34.2 44 43.7 73.3 69 83.6c5.1 2.1 14.2-4.7 14.4-16 .1-4.2-7.1-22.2-33.5-23.1m61 17.7c-7.1-.1-14.6 3-22.8 11.5-28.9 30.3 13.8 35.5 10.6 51.9-9.7 48.5-.9 52.5 8.3 55.6 11.7 3.9 33.8-33.4 43.1-40.4 12.4-9.4 77.9-42.2 62.4-58.8-22.3-23.8-27 7.3-57.7-1-14.6-3.9-28.3-18.8-43.9-18.8M54.4 96.5c-2.8-.1-5.5.4-8.1 1.6-11.5 5.2 10.8 36.5 20.9 37.4 12.4 1.1 17.4-8.9 17.6-14.7.3-7.6-15.4-24-30.4-24.3m4 46.7c-4.5.1-8 1.2-9.6 3.3-4.1 6.2 21.6 30.4 28.7 32 6.5 1.5 12.6-13 11.4-18.7-2.2-10.4-19.2-16.7-30.5-16.6",
                      transform = "scale(.08 .08) translate(-120,-80) ") 
lesbian['symbol'] = group(path(d="M500 550L211.325 50h577.35z", fill="black"),
                          path(d="M479.667 132.374a162.687 162.687 0 0 1-108.732-62.373 162.687 162.687 0 0 0 0 198.075 162.687 162.687 0 0 1 108.732-62.373zm40.672 73.329a162.687 162.687 0 0 1 108.732 62.373 162.687 162.687 0 0 0 0-198.075 162.687 162.687 0 0 1-108.732 62.373zm-4.067-91.571a16.269 8.134 0 0 0-32.538 0v347.743a16.269 8.134 0 0 0 32.538 0z", 
                               fill="white"), 
                          transform = "scale(.04, .04) translate(-500 -150)")

demigirl = {"colors":["darkgrey", "lightgrey", "lightpink","white", "lightpink", "lightgrey", "darkgrey"], "name": "demigirl"}
demiboy = {"colors":["darkgrey", "lightgrey", "lightblue","white", "lightblue", "lightgrey", "darkgrey"], "name": "demiboy"}

flag_defs = [demigirl, demiboy, lesbian, bear, agender, ace, bi, pride, enby, genderfluid, pansexual, polysexual, aromantic, lipstick, genderqueer, intersex, polyamory]
```


```python
heart = Clip(gen_heart(), clipid="newid")
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
            height="100",
            viewBox="-25 -25 50 50",
            style={"overflow":"visible"}
        )
    )    
svg(*flag_list, width=f"{90*8}", viewBox="250 0 675 675")

```




<svg viewBox="250 0 675 675" width="720"><clipPath id="newid"><path d="M0.0,5.0 Q2.26480878769362e-09,5.01935203545116 0.00240468499265089,5.05784209373124 Q0.00617678614768245,5.11821945317385 0.0144892681784808,5.19071052417724 Q0.0249796452381706,5.28219447150715 0.0416669391001586,5.38322902221801 Q0.0625689845764014,5.50978212250472 0.0921242540272451,5.64469196933818 Q0.129325564905271,5.81450341906648 0.178888071354544,5.99135494886849 Q0.227032997926876,6.16314819595208 0.285852572783466,6.33796304924934 Q0.345659522697073,6.51571243286517 0.415701700411068,6.69417844133358 Q0.487743067528425,6.87773834271958 0.569888188951648,7.06019887319993 Q0.692043825721294,7.33153065651206 0.834806300015498,7.59665683949396 Q0.918421740467044,7.75194024064588 1.00862101667763,7.90415568501767 Q1.12167926629051,8.09494670272544 1.24449884261148,8.27994312284276 Q1.44189780344349,8.57727439675439 1.66250874377508,8.85670281234556 Q1.80054060640138,9.03153559541965 1.94694688614682,9.19842404729501 Q2.08999423977703,9.36148366081515 2.24054566891579,9.51639833059041 Q2.48490085256662,9.76783534981824 2.74741879975013,9.99621086079807 Q3.01662696842382,10.2304064795754 3.30291999709097,10.4385942042024 Q3.46972317871875,10.5598908176942 3.64179542494331,10.6719572214367 Q3.79857226878001,10.7740621074039 3.95941554482475,10.8683033405894 Q4.13334243392154,10.9702105195257 4.31166833497306,11.0627149706127 Q4.47604708828145,11.1479845038409 4.64386151028959,11.2251070150907 Q4.80544594869858,11.299366411392 4.96995032351617,11.3659501831024 Q5.16725965014621,11.4458118838945 5.36835311845226,11.5144650549576 Q5.56561833961004,11.5818112650908 5.7660857806164,11.6382214352365 Q5.93594304380552,11.6860181101922 6.10780540394526,11.7258795037075 Q6.3802811445957,11.7890769525997 6.65689783599178,11.8321328272072 Q6.88756600251257,11.8680367330906 7.12039035026157,11.8898178268749 Q7.33575429714658,11.9099654719568 7.5524023719199,11.9179755377665 Q7.78903411552322,11.9267244539104 8.02650188595541,11.9209696911957 Q8.31148267851657,11.9140635041521 8.59647282523938,11.8863060110558 Q8.84172783653293,11.8624186438571 9.08605624824551,11.8231757557194 Q9.29602775102361,11.7894511138005 9.5047004646898,11.7444820539865 Q9.73546771599974,11.6947516117789 9.96389320433066,11.631434414029 Q10.2137994798527,11.5621629628359 10.4598847954114,11.4769149350853 Q10.7426952738113,11.3789447028671 11.0189146985215,11.2604175545564 Q11.2783606307036,11.14908799649 11.5305552606758,11.0202359184706 Q11.8305962880828,10.8669380077389 12.1182124982183,10.6899608334626 Q12.3086605446971,10.5727735681955 12.4928101128895,10.4457122376404 Q12.7138340887796,10.2932079405257 12.9247407405014,10.1272078034175 Q13.1164494580624,9.97631795172166 13.2989309836935,9.81495653041487 Q13.4993501715355,9.63773352169933 13.6876496499027,9.44875874377583 Q13.8259025844505,9.31000999189398 13.9571663998683,9.16537567684822 Q14.0895559130142,9.01950100078341 14.2144709921875,8.86804150073268 Q14.3647042289743,8.68588374135466 14.50359102542,8.496302620215 Q14.6242491373507,8.33160373796121 14.7359701511584,8.16180777241553 Q14.8556947497797,7.9798477889744 14.9647911861361,7.79259020255814 Q15.0815966885041,7.5921004598673 15.1858302302757,7.38620717426887 Q15.2838990649354,7.19249108020058 15.3705462405702,6.99456656547992 Q15.4710479022511,6.76499482847765 15.555848418953,6.53053381443338 Q15.6293410875024,6.32733734508333 15.6908398354807,6.12101489646327 Q15.7582996840502,5.89469352248478 15.811151998362,5.66520400901477 Q15.858001700426,5.46177837907041 15.8932743283624,5.25628456535619 Q15.9234569772515,5.08044431780161 15.9451194504346,4.90333416558016 Q15.9730560934491,4.67492704627213 15.9867773968648,4.44479362169134 Q16.0034165941822,4.16572133934909 15.9991176647554,3.88472444785707 Q15.9950908430473,3.62151371089842 15.9726972179107,3.35708697651958 Q15.9526619394994,3.12050789606779 15.9179459679384,2.88322942110747 Q15.882312030686,2.63967678789829 15.83124032874,2.39559405324708 Q15.7875158480249,2.1866252815493 15.7324953373768,1.97736550244011 Q15.6648912559291,1.72024656653811 15.5802540161198,1.46276838245011 Q15.4968741501039,1.20911530326591 15.3969639315714,0.955118442554341 Q15.3045821236361,0.720260691795003 15.1980404233408,0.485042552463534 Q15.0759331774567,0.215459477516022 14.935136668034,-0.0547900505028633 Q14.7784251600096,-0.355587358989756 14.5983261379963,-0.657651595836769 Q14.4326365303214,-0.935548190367364 14.2468180712942,-1.21507534194023 Q13.9287667177733,-1.69352075241799 13.5495204141351,-2.17993676735823 Q13.228806301099,-2.59128021171493 12.8611063340419,-3.0124517446707 Q12.1591087582907,-3.81653502342836 11.2483797084418,-4.69658759121086 Q10.4733210891135,-5.44553957449827 9.42454171069957,-6.36494199823616 Q8.84072932123853,-6.87673555265406 7.788610883906,-7.77268471082305 Q6.43199730758967,-8.92793182800395 5.86781215340663,-9.42143310902599 Q4.99911290579133,-10.1812974697638 4.33114177564245,-10.8099404645036 Q3.70609091742599,-11.3981902041088 3.18523060681885,-11.9373159451196 Q2.65398052055043,-12.4871958084704 2.2119638126538,-13.0054355175612 Q1.84652002656313,-13.4338977860892 1.53818480616621,-13.8451114872961 Q1.35658899707246,-14.0872981719213 1.19468144267213,-14.3236430665681 Q1.01229440141544,-14.5898829354267 0.855250034700979,-14.8481696259238 Q0.710327112506176,-15.0865204992088 0.587635439099838,-15.317016364333 Q0.482522452421447,-15.5144878644567 0.394395445017321,-15.7049318068687 Q0.31840843950407,-15.869141001397 0.255658210448299,-16.0268054813404 Q0.189432844334108,-16.1932014939857 0.138853346014398,-16.3499815211115 Q0.0926197731189966,-16.4932905900716 0.0605744460923479,-16.625013082467 Q0.0353801389730772,-16.7285744199802 0.0199590858880895,-16.820733667613 Q0.00867700999654953,-16.8881575731122 0.00346592649802561,-16.9441272743669 Q0.000399281055259889,-16.9770646144295 2.49345880547808e-05,-16.9979165809901 Q0.000120167169769384,-16.9926119052863 -0.00120639179482519,-16.9723446290242 Q-0.00426775812446953,-16.9255728240776 -0.0129503651544767,-16.86557788734 Q-0.0227183511665687,-16.7980832165775 -0.0385454062196693,-16.7222898015959 Q-0.06004549711036,-16.6193290609179 -0.0915669504606278,-16.5067117118991 Q-0.132286979305915,-16.3612304217578 -0.188273154562518,-16.204902779091 Q-0.258831712369531,-16.0078853375281 -0.351810097949509,-15.7987840090959 Q-0.440000005976105,-15.6004516030464 -0.547194072845051,-15.3939437422104 Q-0.651340977758142,-15.193306195987 -0.772699085783482,-14.9863772240217 Q-0.910246809839973,-14.7518431694101 -1.0692413762151,-14.5103646821128 Q-1.22417112561029,-14.2750597759499 -1.39908931791318,-14.0337431312646 Q-1.76797104341055,-13.5248349433239 -2.22583196061482,-12.9891937151164 Q-2.65281454964278,-12.4896763511826 -3.16250584273345,-11.960865339223 Q-3.75455354091074,-11.3466085397729 -4.48484292020919,-10.6660006846297 Q-5.15417223354364,-10.0422057873649 -6.03462845747207,-9.27588577364818 Q-6.5518613566613,-8.82570334364281 -7.72688839874177,-7.82524124839609 Q-9.00011940672614,-6.74116461325269 -9.66659027493077,-6.1518575057301 Q-10.6800142168527,-5.25576742827941 -11.4416925502921,-4.5083632999628 Q-11.9256928826451,-4.03343335824615 -12.3453337586718,-3.58350021932445 Q-12.8421226311087,-3.05085006647637 -13.2630306985554,-2.53794032909005 Q-13.5888635034756,-2.14088731127246 -13.8734126595931,-1.7506997108797 Q-14.1158142868982,-1.41830684568896 -14.3296155195759,-1.08906603538983 Q-14.6222670714185,-0.638400560466284 -14.8629035091692,-0.191196762642277 Q-14.9849831812171,0.035678657752151 -15.093879517273,0.262018849814471 Q-15.1989501677438,0.48040738398381 -15.2918143665365,0.698434979814885 Q-15.4099383650006,0.975767813457227 -15.5083731080758,1.25265889367945 Q-15.596037025423,1.49925228146578 -15.6680979222918,1.74552862415746 Q-15.7452025309944,2.00904242791343 -15.8044279558644,2.27213565719569 Q-15.8673099421169,2.55147218982739 -15.9099982659839,2.83015436556823 Q-15.9467996846554,3.07040505935725 -15.9685614040832,3.30996314026493 Q-15.9881495049069,3.52559352082962 -15.9955342067788,3.74046434121497 Q-16.0051232678424,4.01947484877545 -15.9941254637899,4.2967472393645 Q-15.9844330208493,4.54110936947305 -15.958768035937,4.78366431573383 Q-15.9275621653641,5.07858513044192 -15.8728386332033,5.37000215623899 Q-15.8278093231867,5.60979493058336 -15.7669750538715,5.84656658453498 Q-15.721016172269,6.02544208568407 -15.6661182996239,6.20226632422338 Q-15.6208315317082,6.34813351117917 -15.5695193619767,6.49241673134215 Q-15.4613890101118,6.79646537021361 -15.3269801205853,7.09222815454625 Q-15.2212449367798,7.32489529787583 -15.0996951958763,7.55142914467109 Q-14.9588348202878,7.81395247467492 -14.7974725228564,8.0668861942751 Q-14.6745800019696,8.25951894005113 -14.5402766384116,8.44582208248948 Q-14.3933701098356,8.64960810238759 -14.2334198263091,8.84498132868387 Q-14.0945594532161,9.01459402644063 -13.9463689488664,9.17725000648766 Q-13.7735280755873,9.36696257787514 -13.588753931665,9.54638613301087 Q-13.4189681105967,9.71125538896335 -13.23982095404,9.86674014639278 Q-13.0625216805617,10.0206210957701 -12.8767644199624,10.1646925661538 Q-12.6944389535778,10.3061023713246 -12.5046728111778,10.4375123135825 Q-12.3142699757146,10.5693631553476 -12.1171076375409,10.6906405650386 Q-11.9213331232265,10.811064304174 -11.7196291899761,10.9206103014377 Q-11.509884893371,11.0345230436026 -11.2945462865961,11.1362305693748 Q-11.0736106685721,11.2405816441808 -10.8476757705343,11.3316650627413 Q-10.6451233054253,11.4133220848312 -10.4392342246826,11.4840381672923 Q-10.2480502354789,11.5497035376801 -10.0545178054937,11.605752174849 Q-9.87842747053587,11.6567494330024 -9.70078839955957,11.699669661687 Q-9.51646003889087,11.7442061217657 -9.33086927650686,11.7799481442673 Q-9.13248730736292,11.8181535630821 -8.933139388093,11.846219406851 Q-8.71465712197788,11.8769791417381 -8.49561748097842,11.8954757888015 Q-8.29291726492743,11.9125926647188 -8.09024399409492,11.9191639457214 Q-7.78610008904026,11.9290252118723 -7.4833331334596,11.915111810162 Q-7.17318452623145,11.9008591908364 -6.86609005385436,11.8617329844013 Q-6.59503326929163,11.8271982575912 -6.32749985800465,11.7734249707618 Q-6.065591016902,11.7207822030116 -5.80803820752765,11.6498970887622 Q-5.55929013948285,11.5814352643096 -5.31546652781383,11.4961928265364 Q-5.10668790644988,11.4232023621669 -4.90208243255889,11.3381020157274 Q-4.65361227556304,11.2347572906909 -4.41212777878246,11.1139056578479 Q-4.19936350048537,11.0074271435513 -3.99268182769649,10.8876853593409 Q-3.75270580423463,10.7486543711102 -3.52182577913573,10.5922682144105 Q-3.32874675879168,10.4614864981576 -3.14265200973488,10.3189846901617 Q-2.96546888319985,10.183306945327 -2.79512566366148,10.0373935236474 Q-2.59954871236449,9.869865269557 -2.41370491741605,9.68946420864727 Q-2.19513433610818,9.47729481788262 -1.99121915187079,9.24849308724242 Q-1.80560573104341,9.04022673339448 -1.63321108031305,8.8193835024801 Q-1.48460042648279,8.62900835568098 -1.34656919353414,8.43025073001946 Q-1.22862003028138,8.26041021540489 -1.11890397474925,8.08517660112203 Q-0.95801857573265,7.82821758251459 -0.816175270753006,7.56186513162384 Q-0.660837400706088,7.27017267275816 -0.530605965747761,6.97155652900988 Q-0.428580116785493,6.73761481140916 -0.343519030901754,6.5029591230879 Q-0.261963346200934,6.27797368901832 -0.197516475528564,6.05656345647983 Q-0.136184858928778,5.84585582472599 -0.0920712402436369,5.64444995400555 Q-0.0534506179297929,5.46812299882186 -0.0298383755424187,5.30751615628668 Q-0.0115789781484796,5.18331854244193 -0.00400653952455051,5.08123174112462 Z" fill="none" id="9ebcf82df7a7408788b32c7d0c69327f" stroke="red" stroke-width=".5" transform="scale(1.25 -1.25)"></path></clipPath><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="60" y="50"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">demigirl</text><g style="clip-path: url(#newid)"><g><rect fill="darkgrey" height="10.428571428571429%" stroke="darkgrey" width="50" x="-25" y="-31.5%"></rect><rect fill="lightgrey" height="10.428571428571429%" stroke="lightgrey" width="50" x="-25" y="-21.07142857142857%"></rect><rect fill="lightpink" height="10.428571428571429%" stroke="lightpink" width="50" x="-25" y="-10.642857142857142%"></rect><rect fill="white" height="10.428571428571429%" stroke="white" width="50" x="-25" y="-0.2142857142857153%"></rect><rect fill="lightpink" height="10.428571428571429%" stroke="lightpink" width="50" x="-25" y="10.214285714285715%"></rect><rect fill="lightgrey" height="10.428571428571429%" stroke="lightgrey" width="50" x="-25" y="20.642857142857146%"></rect><rect fill="darkgrey" height="10.428571428571429%" stroke="darkgrey" width="50" x="-25" y="31.07142857142857%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="180" y="50"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">lesbian</text><g style="clip-path: url(#newid)"><g><rect fill="purple" height="73.0%" stroke="purple" width="50" x="-25" y="-31.5%"></rect><g transform="scale(.04, .04) translate(-500 -150)"><path d="M500 550L211.325 50h577.35z" fill="black"></path><path d="M479.667 132.374a162.687 162.687 0 0 1-108.732-62.373 162.687 162.687 0 0 0 0 198.075 162.687 162.687 0 0 1 108.732-62.373zm40.672 73.329a162.687 162.687 0 0 1 108.732 62.373 162.687 162.687 0 0 0 0-198.075 162.687 162.687 0 0 1-108.732 62.373zm-4.067-91.571a16.269 8.134 0 0 0-32.538 0v347.743a16.269 8.134 0 0 0 32.538 0z" fill="white"></path></g></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="345" y="50"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">bear</text><g style="clip-path: url(#newid)"><g><rect fill="#623804" height="10.428571428571429%" stroke="#623804" width="50" x="-25" y="-31.5%"></rect><rect fill="chocolate" height="10.428571428571429%" stroke="chocolate" width="50" x="-25" y="-21.07142857142857%"></rect><rect fill="#fedd63" height="10.428571428571429%" stroke="#fedd63" width="50" x="-25" y="-10.642857142857142%"></rect><rect fill="moccasin" height="10.428571428571429%" stroke="moccasin" width="50" x="-25" y="-0.2142857142857153%"></rect><rect fill="white" height="10.428571428571429%" stroke="white" width="50" x="-25" y="10.214285714285715%"></rect><rect fill="dimgray" height="10.428571428571429%" stroke="dimgray" width="50" x="-25" y="20.642857142857146%"></rect><rect fill="black" height="10.428571428571429%" stroke="black" width="50" x="-25" y="31.07142857142857%"></rect><path d="M98.9 24.4c-5.7 0-11.5 1.3-16.3 4.4C61.2 42.6 91.1 48.3 96 51.1c4.7 2.7 22.4 22.9 29.7-8.4 2.2-9.7-12.2-18.3-26.8-18.3m45.4 11.2c-17.7 1.9-.8 43 23.6 44.4 16.5.9 28.9-39.3-23.6-44.4m-94.4 8.9C34.2 44 43.7 73.3 69 83.6c5.1 2.1 14.2-4.7 14.4-16 .1-4.2-7.1-22.2-33.5-23.1m61 17.7c-7.1-.1-14.6 3-22.8 11.5-28.9 30.3 13.8 35.5 10.6 51.9-9.7 48.5-.9 52.5 8.3 55.6 11.7 3.9 33.8-33.4 43.1-40.4 12.4-9.4 77.9-42.2 62.4-58.8-22.3-23.8-27 7.3-57.7-1-14.6-3.9-28.3-18.8-43.9-18.8M54.4 96.5c-2.8-.1-5.5.4-8.1 1.6-11.5 5.2 10.8 36.5 20.9 37.4 12.4 1.1 17.4-8.9 17.6-14.7.3-7.6-15.4-24-30.4-24.3m4 46.7c-4.5.1-8 1.2-9.6 3.3-4.1 6.2 21.6 30.4 28.7 32 6.5 1.5 12.6-13 11.4-18.7-2.2-10.4-19.2-16.7-30.5-16.6" transform="scale(.08 .08) translate(-120,-80) "></path></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="465" y="50"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">agender</text><g style="clip-path: url(#newid)"><g><rect fill="black" height="10.428571428571429%" stroke="black" width="50" x="-25" y="-31.5%"></rect><rect fill="lightgrey" height="10.428571428571429%" stroke="lightgrey" width="50" x="-25" y="-21.07142857142857%"></rect><rect fill="white" height="10.428571428571429%" stroke="white" width="50" x="-25" y="-10.642857142857142%"></rect><rect fill="chartreuse" height="10.428571428571429%" stroke="chartreuse" width="50" x="-25" y="-0.2142857142857153%"></rect><rect fill="white" height="10.428571428571429%" stroke="white" width="50" x="-25" y="10.214285714285715%"></rect><rect fill="lightgrey" height="10.428571428571429%" stroke="lightgrey" width="50" x="-25" y="20.642857142857146%"></rect><rect fill="black" height="10.428571428571429%" stroke="black" width="50" x="-25" y="31.07142857142857%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="0" y="170"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">asexual</text><g style="clip-path: url(#newid)"><g><rect fill="black" height="18.25%" stroke="black" width="50" x="-25" y="-31.5%"></rect><rect fill="lightgrey" height="18.25%" stroke="lightgrey" width="50" x="-25" y="-13.25%"></rect><rect fill="white" height="18.25%" stroke="white" width="50" x="-25" y="5.0%"></rect><rect fill="purple" height="18.25%" stroke="purple" width="50" x="-25" y="23.25%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="130" y="170"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">bi</text><g style="clip-path: url(#newid)"><g><rect fill="deeppink" height="14.6%" stroke="deeppink" width="50" x="-25" y="-31.5%"></rect><rect fill="deeppink" height="14.6%" stroke="deeppink" width="50" x="-25" y="-16.9%"></rect><rect fill="mediumpurple" height="14.6%" stroke="mediumpurple" width="50" x="-25" y="-2.3000000000000007%"></rect><rect fill="blue" height="14.6%" stroke="blue" width="50" x="-25" y="12.299999999999997%"></rect><rect fill="blue" height="14.6%" stroke="blue" width="50" x="-25" y="26.9%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="260" y="170"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">pride</text><g style="clip-path: url(#newid)"><g><rect fill="red" height="9.125%" stroke="red" width="50" x="-25" y="-31.5%"></rect><rect fill="orange" height="9.125%" stroke="orange" width="50" x="-25" y="-22.375%"></rect><rect fill="yellow" height="9.125%" stroke="yellow" width="50" x="-25" y="-13.25%"></rect><rect fill="green" height="9.125%" stroke="green" width="50" x="-25" y="-4.125%"></rect><rect fill="blue" height="9.125%" stroke="blue" width="50" x="-25" y="5.0%"></rect><rect fill="purple" height="9.125%" stroke="purple" width="50" x="-25" y="14.125%"></rect><rect fill="brown" height="9.125%" stroke="brown" width="50" x="-25" y="23.25%"></rect><rect fill="black" height="9.125%" stroke="black" width="50" x="-25" y="32.375%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="390" y="170"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">enby</text><g style="clip-path: url(#newid)"><g><rect fill="#ffef00" height="18.25%" stroke="#ffef00" width="50" x="-25" y="-31.5%"></rect><rect fill="white" height="18.25%" stroke="white" width="50" x="-25" y="-13.25%"></rect><rect fill="#9C59D1" height="18.25%" stroke="#9C59D1" width="50" x="-25" y="5.0%"></rect><rect fill="black" height="18.25%" stroke="black" width="50" x="-25" y="23.25%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="520" y="170"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">genderfluid</text><g style="clip-path: url(#newid)"><g><rect fill="#ff75a2" height="14.6%" stroke="#ff75a2" width="50" x="-25" y="-31.5%"></rect><rect fill="white" height="14.6%" stroke="white" width="50" x="-25" y="-16.9%"></rect><rect fill="#be18d6" height="14.6%" stroke="#be18d6" width="50" x="-25" y="-2.3000000000000007%"></rect><rect fill="black" height="14.6%" stroke="black" width="50" x="-25" y="12.299999999999997%"></rect><rect fill="mediumblue" height="14.6%" stroke="mediumblue" width="50" x="-25" y="26.9%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="40" y="290"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">pansexual</text><g style="clip-path: url(#newid)"><g><rect fill="deeppink" height="24.333333333333332%" stroke="deeppink" width="50" x="-25" y="-31.5%"></rect><rect fill="gold" height="24.333333333333332%" stroke="gold" width="50" x="-25" y="-7.166666666666668%"></rect><rect fill="deepskyblue" height="24.333333333333332%" stroke="deepskyblue" width="50" x="-25" y="17.166666666666664%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="185" y="290"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">polysexual</text><g style="clip-path: url(#newid)"><g><rect fill="#f61cb9" height="24.333333333333332%" stroke="#f61cb9" width="50" x="-25" y="-31.5%"></rect><rect fill="#07d569" height="24.333333333333332%" stroke="#07d569" width="50" x="-25" y="-7.166666666666668%"></rect><rect fill="dodgerblue" height="24.333333333333332%" stroke="dodgerblue" width="50" x="-25" y="17.166666666666664%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="335" y="290"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">aromantic</text><g style="clip-path: url(#newid)"><g><rect fill="#3da542" height="14.6%" stroke="#3da542" width="50" x="-25" y="-31.5%"></rect><rect fill="#a7d379" height="14.6%" stroke="#a7d379" width="50" x="-25" y="-16.9%"></rect><rect fill="white" height="14.6%" stroke="white" width="50" x="-25" y="-2.3000000000000007%"></rect><rect fill="lightgrey" height="14.6%" stroke="lightgrey" width="50" x="-25" y="12.299999999999997%"></rect><rect fill="black" height="14.6%" stroke="black" width="50" x="-25" y="26.9%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="480" y="290"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">lipstick</text><g style="clip-path: url(#newid)"><g><rect fill="#A60061" height="10.428571428571429%" stroke="#A60061" width="50" x="-25" y="-31.5%"></rect><rect fill="#B95393" height="10.428571428571429%" stroke="#B95393" width="50" x="-25" y="-21.07142857142857%"></rect><rect fill="#D260A7" height="10.428571428571429%" stroke="#D260A7" width="50" x="-25" y="-10.642857142857142%"></rect><rect fill="#EDEDEB" height="10.428571428571429%" stroke="#EDEDEB" width="50" x="-25" y="-0.2142857142857153%"></rect><rect fill="#E5ABD0" height="10.428571428571429%" stroke="#E5ABD0" width="50" x="-25" y="10.214285714285715%"></rect><rect fill="#C74D52" height="10.428571428571429%" stroke="#C74D52" width="50" x="-25" y="20.642857142857146%"></rect><rect fill="#8C1D00" height="10.428571428571429%" stroke="#8C1D00" width="50" x="-25" y="31.07142857142857%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="170" y="410"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">genderqueer</text><g style="clip-path: url(#newid)"><g><rect fill="purple" height="24.333333333333332%" stroke="purple" width="50" x="-25" y="-31.5%"></rect><rect fill="white" height="24.333333333333332%" stroke="white" width="50" x="-25" y="-7.166666666666668%"></rect><rect fill="forestgreen" height="24.333333333333332%" stroke="forestgreen" width="50" x="-25" y="17.166666666666664%"></rect></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="355" y="410"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">intersex</text><g style="clip-path: url(#newid)"><g><rect fill="gold" height="73.0%" stroke="gold" width="50" x="-25" y="-31.5%"></rect><circle cx="0" cy="2" fill="transparent" r="5" stroke="purple" stroke-width="2.5"></circle></g></g></svg><svg style="overflow: visible" height="100" viewBox="-25 -25 50 50" x="260" y="530"><text font-family="Minion Pro" font-size="15" text-anchor="middle" y="-20">polyamory</text><g style="clip-path: url(#newid)"><g><rect fill="blue" height="24.333333333333332%" stroke="blue" width="50" x="-25" y="-31.5%"></rect><rect fill="red" height="24.333333333333332%" stroke="red" width="50" x="-25" y="-7.166666666666668%"></rect><rect fill="black" height="24.333333333333332%" stroke="black" width="50" x="-25" y="17.166666666666664%"></rect><text fill="yellow" font-family="Minion Pro" font-size="15" text-anchor="middle" y="4.5">π</text></g></g></svg></svg>




```python
for idx, flag_def in enumerate(flag_defs):
    flag = Flag(**flag_def)
    display(IPython.display.SVG(flag._repr_mimebundle_(None,None)['text/html']), metadata={"filename": flag_def['name']})

```


![svg](Tearing%20my%20Hearts%20out_files/demigirl.svg)



![svg](Tearing%20my%20Hearts%20out_files/demiboy.svg)



![svg](Tearing%20my%20Hearts%20out_files/lesbian.svg)



![svg](Tearing%20my%20Hearts%20out_files/bear.svg)



![svg](Tearing%20my%20Hearts%20out_files/agender.svg)



![svg](Tearing%20my%20Hearts%20out_files/asexual.svg)



![svg](Tearing%20my%20Hearts%20out_files/bi.svg)



![svg](Tearing%20my%20Hearts%20out_files/pride.svg)



![svg](Tearing%20my%20Hearts%20out_files/enby.svg)



![svg](Tearing%20my%20Hearts%20out_files/genderfluid.svg)



![svg](Tearing%20my%20Hearts%20out_files/pansexual.svg)



![svg](Tearing%20my%20Hearts%20out_files/polysexual.svg)



![svg](Tearing%20my%20Hearts%20out_files/aromantic.svg)



![svg](Tearing%20my%20Hearts%20out_files/lipstick.svg)



![svg](Tearing%20my%20Hearts%20out_files/genderqueer.svg)



![svg](Tearing%20my%20Hearts%20out_files/intersex.svg)



![svg](Tearing%20my%20Hearts%20out_files/polyamory.svg)



```python

```


```python

```


```python

```


```python
%load flag_spec.py

```


```python
# %%writefile flag_spec.py
trans = {"colors":['lightskyblue', 'lightpink', 'white',  'lightpink', 'lightskyblue'],
         "name":"trans",}

intersex = {"colors":["gold"],
            "name": "intersex",}
intersex['symbol'] = circle(cx="0", cy="2", r="5", fill="transparent", 
                            stroke="purple", **{"stroke-width":"2.5"})

genderqueer = {"colors":['purple', 'white', 'forestgreen'],
               "name": "genderqueer",}

pride = {"colors":['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black'], 
         "name": "pride",}

agender = {"colors":['black', 'lightgrey', 'white', 'chartreuse', 'white', 'lightgrey', 'black'],
           "name": "agender",}

ace = {"colors":['black','lightgrey','white', 'purple'], 
       "name": "asexual", }

bi = {"colors":['deeppink', 'deeppink', 'mediumpurple', 'blue','blue'],
      "name": "bi",}

enby = {"colors":['#ffef00', 'white', '#9C59D1', 'black'], 
        "name": "enby",}

genderfluid = {"colors":['#ff75a2', "white","#be18d6", 'black', 'mediumblue'],
               "name": "genderfluid",}

pansexual = {"colors":['deeppink', "gold", "deepskyblue"],
             "name": "pansexual",}

polysexual = {"colors":["#f61cb9", "#07d569", 'dodgerblue'],
              "name": "polysexual",}

aromantic = {"colors":["#3da542", "#a7d379", "white", "lightgrey", "black"],
             "name": "aromantic",}

lipstick = {"colors":["#A60061", "#B95393", "#D260A7", "#EDEDEB", "#E5ABD0", "#C74D52", "#8C1D00"], 
            "name": "lipstick",}



polyamory = {"colors":["blue", "red", "black"],
             "name": "polyamory",}

bear = {"colors": ["#623804", "chocolate", "#fedd63", "moccasin", "white", "dimgray", "black"], 
        "name": "bear",}

lesbian = {"colors":["purple"],
           "name": "lesbian",}

polyamory['symbol'] = text("π", y="4.5", fill="yellow", 
                           **{'text-anchor': "middle", "font-family": "Minion Pro", "font-size":"15"})
bear['symbol'] = path(d="M98.9 24.4c-5.7 0-11.5 1.3-16.3 4.4C61.2 42.6 91.1 48.3 96 51.1c4.7 2.7 22.4 22.9 29.7-8.4 2.2-9.7-12.2-18.3-26.8-18.3m45.4 11.2c-17.7 1.9-.8 43 23.6 44.4 16.5.9 28.9-39.3-23.6-44.4m-94.4 8.9C34.2 44 43.7 73.3 69 83.6c5.1 2.1 14.2-4.7 14.4-16 .1-4.2-7.1-22.2-33.5-23.1m61 17.7c-7.1-.1-14.6 3-22.8 11.5-28.9 30.3 13.8 35.5 10.6 51.9-9.7 48.5-.9 52.5 8.3 55.6 11.7 3.9 33.8-33.4 43.1-40.4 12.4-9.4 77.9-42.2 62.4-58.8-22.3-23.8-27 7.3-57.7-1-14.6-3.9-28.3-18.8-43.9-18.8M54.4 96.5c-2.8-.1-5.5.4-8.1 1.6-11.5 5.2 10.8 36.5 20.9 37.4 12.4 1.1 17.4-8.9 17.6-14.7.3-7.6-15.4-24-30.4-24.3m4 46.7c-4.5.1-8 1.2-9.6 3.3-4.1 6.2 21.6 30.4 28.7 32 6.5 1.5 12.6-13 11.4-18.7-2.2-10.4-19.2-16.7-30.5-16.6",
                      transform = "scale(.08 .08) translate(-120,-80) ") 
lesbian['symbol'] = group(path(d="M500 550L211.325 50h577.35z", fill="black"),
                          path(d="M479.667 132.374a162.687 162.687 0 0 1-108.732-62.373 162.687 162.687 0 0 0 0 198.075 162.687 162.687 0 0 1 108.732-62.373zm40.672 73.329a162.687 162.687 0 0 1 108.732 62.373 162.687 162.687 0 0 0 0-198.075 162.687 162.687 0 0 1-108.732 62.373zm-4.067-91.571a16.269 8.134 0 0 0-32.538 0v347.743a16.269 8.134 0 0 0 32.538 0z", 
                               fill="white"), 
                          transform = "scale(.04, .04) translate(-500 -150)")

flag_defs = [, trans, lesbian, bear, agender, ace, bi, pride, enby, genderfluid, pansexual, polysexual, aromantic, lipstick, genderqueer, intersex, polyamory]
```


```python

```


```python

```


```python
!rm images/pngs/*
```


```python
write_pngs(flag_defs, suffix="flag", encoder=lambda x: Flag(**x).encode())
write_pngs(flag_defs, suffix="heart")
```


```python
ls images/pngs
```


```python
for f in sorted(glob.glob(os.path.join("..",'hearts_full_of_pride', "images", "pngs","*"))):
    display(Image(filename=f), f)
```


```python

```


```python

```


```python

```


```python

```


```python

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
fade_out =  animate(id="animation1",
             attributeName="opacity",
                dur="3s",
                begin="6s",
                fill="freeze",
             **{"from":"1", "to":"0" })


def animated_heart():
    return group(gen_heart("blargh", stroke="white"),anim_style)

heart = Clip(gen_heart())
```


```python
svg(heart.clipper(), 
    heart.clip(
        Flag(**rainbow).flag()
    ),
    group(Flag(**rainbow).flag(**{"id": "myflag"}), 
          animated_heart(),
          fade_out),
    viewBox="-25 -25 50 50",
    height = "450"
   )

```


```python

```