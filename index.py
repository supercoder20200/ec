from flask import Flask, Response, render_template, request, jsonify
import pandas
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import matplotlib.ticker as mtick
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import json
import io
import random
import base64 
import matplotlib.lines as mlines
from matplotlib.ticker import MaxNLocator
import math

from hashlib import sha256, new
import binascii

P1x = 73310771008388540988256401357661415352304042095800324289366824950562794967684
P1y = 25612579043039068451963311536261134020656877051603969401472335406669199866075
Q1x = 48176182141707200397494489313819525051007048199980929464227639919183476022336
Q1y = 98296285486814584365400012414991623642713198288787606628925957970725125646703

P2x = 30666395314038636955251611877485727881264700062477752893228546022664438539836
P2y = 48756134551913896629494075854379340404881830235582095792160845931170832701583
Q2x = 45087122387471313123709619831609313851158046550223851204564586419255362513023
Q2y = 109339096676174093123610108599832585430504556221366403962193541220247390950753

P3x = 19529594405183429431769641698934855993594712781427083362133146204539138151596
P3y = 82775025087699545192812941522217722457926439501598540605610417946894027764418
Q3x = 111603070862711183124013446573783364289491092943582729801892522125682238345535
Q3y = 57515944028028858999360957506841015828304026625088010987126409447424932181677

P4x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
P4y = 83121579216557378445487899878180864668798711284981320763518679672151497189239
Q4x = 89565891926547004231252920425935692360644145829622209833684329913297188986597
Q4y = 12158399299693830322967808612713398636155367887041628176798871954788371653930

P5x = 49882918176856605183996093635109791033720065193759947705189250698360422403343
P5y = 87579154732488152196412440363928154660028982303670293471050882565505776325455
Q5x = 20492960541290307740821338613687217499731143618862861387631654218377231482582
Q5y = 67711064672408904786252786661545947703563490276329446296505645734325680519952

P6x = 52520157252336559685764725849242661731349909832028725108762837189691969715817
P6y = 35156572455267097799899517596807687333077141162180756329654631887468580805293
Q6x = 3956348602796439307740117187045434825700000342027208134063490177605197310844
Q6y = 78664996595258961789412901856290575890387424745742185933082277791245584623976

P7x = 23861131201851207810434022929743236790072622423728145265202521067677451190953
P7y = 56366276049751685336515781269824299647550048100380482333954076907946287728057
Q7x = 100309494246410138818135350310029905004028001819361899828781733221271966068009
Q7y = 115111448751665247878033032003033566886632067100284258391085181899257104406292

Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

nGx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
nGy = 83121579216557378445487899878180864668798711284981320763518679672151497189239

app = Flask(__name__)

k = 97
a = 0
b = 7

P= (2**256) - (2**32) - (2**9) - (2**8) - (2**7) - (2**6) - (2**4) - 1
PValue =              115792089237316195423570985008687907853269984665640564039457584007908834671663
PValue2 =             231584178474632390847141970017375815706539969331281128078915168015817669343326
closest_prime_to_2p = 231584178474632390847141970017375815706539969331281128078915168015817669343283
HValue =              115792089237316195423570985008687907852837564279074904382605163141518161494337
#0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f 
NValue =              0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
A=0
B=7

xMin = 0
xMax = 1.2 * (10 ** 77)
yMin = 0
yMax = 1.2 * (10 ** 77 )

def extended_euclidean_algorithm(a, b):
    if a == 0 :  
        return b,0,1
             
    gcd,x1,y1 = extended_euclidean_algorithm(b%a, a) 
     
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y

def inverse_of(n):
    if(n < 0):
        n += P
    gcd, x, y = extended_euclidean_algorithm(n, P)
    #assert (n * x + p * y) % p == gcd

    if gcd != 1:
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, P))
    else:
        return x % P

def inverseOf(n):
    n = ( +n ) % P

    if( n < 0 ):
        n = n + P

    for m in range(0, P-1,1):
        if( ( n * m ) % P == 1 ):
            return m

    raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))

class Point:
    def __init__(self, p, x=float('inf'), y=float('inf')):
        self.p = p
        self.x = x % p
        self.y = y % p
        
    def __repr__(self):
        return "Point(p={}, x={}, y={})".format(self.p, self.x, self.y)
    
    def __add__(self, other):
        assert type(other) is Point
        if self.x == other.x and self.y == other.y:
            return self.double()
        dx = other.x - self.x
        dy = other.y - self.y
        if dx == 0:
            return Point()
        slope = (dy * inverse_of(dx)) % self.p
        
        x = (slope ** 2) - self.x - other.x
        y = slope * x + (self.y - slope * self.x)
        x %= self.p
        y %= self.p
        return (x, -y)
        #return Point(self.p, x, -y)
    
    def double(self):
        slope = (3 * (self.x ** 2) + A) * inverse_of(2 * self.y)
        x = (slope ** 2) - (2 * self.x)
        y = slope * x + (self.y - slope * self.x)
        x %= self.p
        y %= self.p
        return Point(self.p, x, -y)
    
    def oppsite(self):
        return Point(self.p, self.x, -self.y)
    
    def np(self):
        return np.array([self.x, self.y])

def enumerate_points(p):
    for x in range(p):
        for y in range(p):
            if (y ** 2) % p == ((x ** 3) + A * x + B) % p:
                yield (x, y)

def plot_curve(p, a, b, ax, point_sizes, point_colors):
    points = list(enumerate_points(p))
    points = np.array(points)

    ax.scatter(
        points[:,0],
        points[:,1],
        list(map(lambda p: point_sizes.get(tuple(p), 10), points)),
        list(map(lambda p: point_colors.get(tuple(p), 'gray'), points)),
        zorder=5,
    )
    
    ax.set_axisbelow(True)
    ax.grid()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
   
    ax.set_ylim(top=yMax)
    ax.set_ylim(bottom=yMin)
    ax.set_xlim(left=xMin)
    ax.set_xlim(right=xMax )
    

def point_distance(p0, p1):
    return ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
 
def wrap_line_segments(p0, p1):
    
    p0x, p0y = p0
    p1x, p1y = p1
    
    dx = p1x - p0x
    dy = p1y - p0y
    slope = dy / dx
    
    # index of block where line touches axis
    x_axis_start_idx = math.ceil(p0y / P)
    x_axis_end_idx = math.floor(p1y / P)
    y_axis_start_idx = math.ceil(p0x / P)
    y_axis_end_idx = math.floor(p1x / P)
    
    # x value is increasing
    if dx >= 0:
        # The value we are using on the y axis edge for end and start
        y_edge = (P, 0)
        # The x values on y axis
        y_axis_stops = list(map(lambda x: x * P, range(y_axis_start_idx, y_axis_end_idx + 1)))
    # x value is decreasing
    else:
        # The value we are using on the y axis edge for end and start
        y_edge = (0, P)
        # The x values on y axis
        y_axis_stops = list(map(lambda x: x * P, range(y_axis_start_idx - 1, y_axis_end_idx, -1)))

    # y value is increasing
    if dy >= 0:
        # The value we are using on the x axis edge for end and start
        x_edge = (P, 0)
        # The x values on y axis
        x_axis_stops = list(map(lambda y: y * P, range(x_axis_start_idx, x_axis_end_idx + 1)))
    # y value is decreasing
    else:
        # The value we are using on the x axis edge for end and start
        x_edge = (0, P)
        # The x values on y axis
        x_axis_stops = list(map(lambda y: y * P, range(x_axis_start_idx - 1, x_axis_end_idx, -1)))
    
    # The points on x axis
    x_axis_stop_points = list(map(lambda y: (p0x + (y - p0y) / slope, y), x_axis_stops))
    # The points on y axis
    y_axis_stop_points = list(map(lambda x: (x, p0y + (x - p0x) * slope), y_axis_stops))
    
    last_point = p0
    
    while len(x_axis_stop_points) or len(y_axis_stop_points):
        x_axis_stop_point = None
        y_axis_stop_point = None
        if x_axis_stop_points: 
            x_axis_stop_point = x_axis_stop_points[0]
        if y_axis_stop_points:
            y_axis_stop_point = y_axis_stop_points[0]
        
        if x_axis_stop_point == y_axis_stop_point:
            pass

        if x_axis_stop_point is not None and y_axis_stop_point is not None:
            # Distance from point on x axis to starting point
            x_axis_distance = point_distance(x_axis_stop_point, p0)
            # Distance from point on y axis to starting point
            y_axis_distance = point_distance(y_axis_stop_point, p0)
        # No more points on x axis, just pick y axis point
        elif x_axis_stop_point is None:
            x_axis_distance = 1
            y_axis_distance = 0
        # No more points on y axis, just pick x axis point
        elif y_axis_stop_point is None:
            x_axis_distance = 0
            y_axis_distance = 1
        
        if x_axis_distance < y_axis_distance:
            x_axis_stop_points.pop(0)
            yield (last_point, (x_axis_stop_point[0] % P, x_edge[0]))
            last_point = (x_axis_stop_point[0] % P, x_edge[1])
        else:
            y_axis_stop_points.pop(0)
            yield (last_point, (y_edge[0], y_axis_stop_point[1] % P))
            last_point = (y_edge[1], y_axis_stop_point[1] % P)
    
    yield (last_point, (p1[0] % P, p1[1] % P))

def plot_distinct_point_curve(p0, p1, p0_annotation, p1_annotation, third_point_annotation, sum_point_annotation):
    #rpoint
   
    rvalue = RValue( (p0.x, p0.y), (p1.x, p1.y) )
    p2 = Point(P, rvalue[0], rvalue[1])
    #print("P2: {}".format(p2))
    #p2 = p0 + p1
   

    fig, ax = plt.subplots()

    plot_curve(
        P, A, B, ax,
        {(p0.x, p0.y): 30, (p1.x, p1.y): 30, (p2.x, p2.y): 30},
        {(p0.x, p0.y): 'b', (p1.x, p1.y): 'b', (p2.x, p2.y): 'orange'},
    )

    dx = p1.x - p0.x
    dy = p1.y - p0.y

    
    dx_dy_gcd = math.gcd(dx, dy)
    dx = int(dx / dx_dy_gcd)
    dy = int(dy / dx_dy_gcd)

    current_increasing_x = p0.x
    current_increasing_y = p0.y
    current_decreasing_x = p1.x
    current_decreasing_y = p1.y
    p2_flip = -p2.y % P


    while True:
        current_increasing_x += dx
        current_increasing_y += dy
       
        if (current_increasing_x % P) == p2.x and (current_increasing_y % P) == p2_flip:
            line_stop = (current_increasing_x, current_increasing_y)
            line_start = (p0.x, p0.y)
            break
        current_decreasing_x -= dx
        current_decreasing_y -= dy
     
        if (current_decreasing_x % P) == p2.x and (current_decreasing_y % P) == p2_flip:
            line_stop = (current_decreasing_x, current_decreasing_y)
            line_start = (p1.x, p1.y)
            break
    
    line_points = list(wrap_line_segments(line_start, line_stop))
    for line_point0, line_point1 in line_points:
        ax.add_line(mlines.Line2D(
            [line_point0[0], line_point1[0]],
            [line_point0[1], line_point1[1]],
            color='r',
            zorder=1,
        ))

    ax.annotate(p0_annotation, xy=p0.np(), xytext=(-5, 5), textcoords='offset points', zorder=10)
    ax.annotate(p1_annotation, xy=p1.np(), xytext=(-5, 5), textcoords='offset points', zorder=10)
    ax.annotate(sum_point_annotation, xy=p2.np(), xytext=(-5, 5), textcoords='offset points', zorder=10)

    ax.add_line(mlines.Line2D(
        [p2.x, p2.x],
        [p2.y, p2_flip],
        color='g',
        zorder=1,
    ))
    
    #plt.show()

def is_on_linepoint(p0,p1):
    #rpoint
    rvalue = RValue( (p0.x, p0.y), (p1.x, p1.y) )
    p2 = Point(P, rvalue[0], rvalue[1])
    #p2 = p0 + p1

    dx = p1.x - p0.x
    dy = p1.y - p0.y
    
    dx_dy_gcd = math.gcd(dx, dy)
    dx = int(dx / dx_dy_gcd)
    dy = int(dy / dx_dy_gcd)
    
    current_increasing_x = p0.x
    current_increasing_y = p0.y
    current_decreasing_x = p1.x
    current_decreasing_y = p1.y
    p2_flip = -p2.y % P

    while True:
        current_increasing_x += dx
        current_increasing_y += dy
        if (current_increasing_x % P) == p2.x and (current_increasing_y % P) == p2_flip:
            line_stop = (current_increasing_x, current_increasing_y)
            line_start = (p0.x, p0.y)
            break
        current_decreasing_x -= dx
        current_decreasing_y -= dy
        if (current_decreasing_x % P) == p2.x and (current_decreasing_y % P) == p2_flip:
            line_stop = (current_decreasing_x, current_decreasing_y)
            line_start = (p1.x, p1.y)
            break
    
    line_points = list(wrap_line_segments(line_start, line_stop))
    
    for line_point0, line_point1 in line_points:
        x1,y1 = line_point0
        x2,y2 = line_point1
        #print("Line Points: {} {} {} {}".format(x1, y1, x2, y2))
        #print("G is on line points : {}".format(is_on_line(x1, y1, x2, y2, Gx, Gy)))

def is_on_line(x1, y1, x2, y2, x3, y3):
    slope = (y2 - y1) / (x2 - x1)
    return y3 - y1 == slope * (x3 - x1)

def is_on_curve(x, y):
    if x is None or y is None:
        return True
    return (y * y - x * x * x - a * x - b) % P == 0

#print (is_on_curve( () ) )

def slope(P,Q):
    Px, Py = P 
    Qx, Qy = Q
    return Qy - Py / Qx - Px

#returns uncompressed public key
def point_to_key(coord):
    x,y = coord
    hx = hex(x).split('x')[-1]
    hy = hex(y).split('x')[-1]
    key = '04' + hx + hy
    return key

#Get compressed public key
def get_compressed_key(coord):
    x,y = coord
    hx = hex(x).split('x')[-1]
    if y%2 == 0:
        return '02' + hx 
    else:
        return '03' + hx


def RValue1(P,Q):
    p = PValue
    Px, Py = P 
    Qx, Qy = Q
    '''
        6C6AF962D1CC0529C6D689174D22DCF68307205BBF0C277408FE6E93B2677FAB
        x = 20131979211061389967751131264678527958175244405833067093780319892079931982003
        y = 97739400561097470892304758517697903219823751918482384097704428900997592914452

        +

        F1A3CDF824F686F93F5836073536C55833A53135250EA0A9F04E5114AC4BF3B5
        x = 3110312095956218672199054275855287122563277688985124808786333320921364917406
        y = 37876912097499250873068094917849140669589073080654473765979021074106692303005
    '''
    #Test2
    #Px = 20131979211061389967751131264678527958175244405833067093780319892079931982003
    #Py = 97739400561097470892304758517697903219823751918482384097704428900997592914452
    #Qx = 3110312095956218672199054275855287122563277688985124808786333320921364917406
    #Qy = 37876912097499250873068094917849140669589073080654473765979021074106692303005

    if Px == Qx:
        #Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
        Delta = (3 *  Px * Px )
        print("Delta-0 = {}".format(Delta))

        inv = inverse_mod(2 * Py, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-1 = {}".format(Delta))
    else:
        #Delta = (Py - Qy) * inverse_mod(Px - Qx, p)
        Delta = (Py - Qy) 
        print("Delta-2 = {}".format(Delta))

        inv = inverse_mod(Px - Qx, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-3 = {}".format(Delta))

    Rx = ( Delta * Delta - Px - Qx ) % p
    print("Rx = {}".format(Rx))

    Ry = Py + Delta * (Rx - Px)
    print("Ry-1 = {}".format(Ry))
   
    Ry = -Ry % p
    print("Ry-2 = {}".format(Ry))

    return (Rx,Ry)

def RValue1_mod2p(P,Q):
    p = 2 * PValue
    
    Px, Py = P 
    Qx, Qy = Q
    
    '''
        Test 3
        1543E189FDF4328DE0D381C168FC24A4157B323618A8B848954F08D69184ADE3
        x = 90659819201786086632712812093525439922787265278409960745653921851223632181874
        y = 76236105781602925710363989762560393482863261107195715651091640076383975965140

        +

        565D1DC3988EE41586553FE46EE6F175A7C0A22314A1E864DB0332BBA083B042
        x = 96325344453420136853251529731187724497408795511788904895294093459244939918654
        y = 26404976397782792208654192950566734405099242558120540310248048648562637353326
    '''
    #Test3
    #Px = 90659819201786086632712812093525439922787265278409960745653921851223632181874
    #Py = 76236105781602925710363989762560393482863261107195715651091640076383975965140
    #Qx = 96325344453420136853251529731187724497408795511788904895294093459244939918654
    #Qy = 26404976397782792208654192950566734405099242558120540310248048648562637353326

    if Px == Qx:
        #Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
        Delta = (3 *  Px * Px )
        print("Delta-0 = {}".format(Delta))

        inv = inverse_mod(2 * Py, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-1 = {}".format(Delta))
    else:
        #Delta = (Py - Qy) * inverse_mod(Px - Qx, p)
        Delta = (Py - Qy) 
        print("Delta-2 = {}".format(Delta))

        inv = inverse_mod(Px - Qx, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-3 = {}".format(Delta))

    Rx = ( Delta * Delta - Px - Qx ) % p
    print("Rx = {}".format(Rx))

    Ry = Py + Delta * (Rx - Px)
    print("Ry-1 = {}".format(Ry))
   
    Ry = -Ry % p
    print("Ry-2 = {}".format(Ry))

    return (Rx,Ry)

def RValue1_no_modp(P,Q):
    p = PValue
    
    Px, Py = P 
    Qx, Qy = Q
    
    '''
        Test 3
        1543E189FDF4328DE0D381C168FC24A4157B323618A8B848954F08D69184ADE3
        x = 90659819201786086632712812093525439922787265278409960745653921851223632181874
        y = 76236105781602925710363989762560393482863261107195715651091640076383975965140

        +

        565D1DC3988EE41586553FE46EE6F175A7C0A22314A1E864DB0332BBA083B042
        x = 96325344453420136853251529731187724497408795511788904895294093459244939918654
        y = 26404976397782792208654192950566734405099242558120540310248048648562637353326
    '''
    #Test3
    #Px = 90659819201786086632712812093525439922787265278409960745653921851223632181874
    #Py = 76236105781602925710363989762560393482863261107195715651091640076383975965140
    #Qx = 96325344453420136853251529731187724497408795511788904895294093459244939918654
    #Qy = 26404976397782792208654192950566734405099242558120540310248048648562637353326

    if Px == Qx:
        #Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
        Delta = (3 *  Px * Px )
        print("Delta-0 = {}".format(Delta))

        inv = inverse_mod(2 * Py, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-1 = {}".format(Delta))
    else:
        #Delta = (Py - Qy) * inverse_mod(Px - Qx, p)
        Delta = (Py - Qy) 
        print("Delta-2 = {}".format(Delta))

        inv = inverse_mod(Px - Qx, p)
        print("inv: {}".format(inv))

        Delta *= inv
        print("Delta-3 = {}".format(Delta))

    Rx = ( Delta * Delta - Px - Qx )
    print("Rx = {}".format(Rx))

    Ry = Py + Delta * (Rx - Px)
    print("Ry-1 = {}".format(Ry))
   
    Ry = -Ry
    print("Ry-2 = {}".format(Ry))

    return (Rx,Ry)


def RValue(P, Q):
    Px, Py = P
    Qx, Qy = Q

    p1 = Point(PValue, Px, Py)
    p2 = Point(PValue, Qx, Qy)

    (x,y) = p1 + p2

    return (x % PValue, y % PValue )

def RValue_mod2p(P,Q):
    Px, Py = P
    Qx, Qy = Q

    p1 = Point(2 * PValue, Px, Py)
    p2 = Point(2 * PValue, Qx, Qy)

    (x,y) = p1 + p2

    return (x % PValue , y % PValue )
    
def RValue_nomodp(P,Q):
    Px, Py = P
    Qx, Qy = Q
    p = 1

    if Px == Qx:
        Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
    else:
        Delta = (Py - Qy) * inverse_mod(Px - Qx, p)

    Rx = ( Delta * Delta - Px - Qx )
    Ry = Py + Delta * (Rx - Px)
    Ry = -Ry

    return (Rx,Ry)

def atZero(P,Q):
    rVal = RValue_mod2p(P,Q)
    Rx, Ry = rVal 

    T1 = 54471083016396624140318862818537878273881801691469295999863093677033270108678
    T2 = 80478451357263941651379549121933213189533405107104786161611916381943362666422
    if Rx > HValue or Ry > HValue:
        return True
    else:
        return False


@app.route('/')
def index():
    
    img = io.BytesIO()
    
    DefaultPx = 76713794182478803891528803692822015505111471502816304530189645921738551553824
    DefaultPy = 9989913769501776956673418849599695616596036032394306022682365229231505097463
    DefaultQx = 49396472789695839840842700318753929600130929079169291199003099305862335813206
    DefaultQy = 67218775828929314131413151142896519708232460644307917083679762983680880922954
    
    DefaultGx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    DefaultGy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

    rz = atZero( (DefaultPx, DefaultPy), (DefaultQx, DefaultQy) )

    Rx_modp, Ry_modp = RValue( (DefaultPx, DefaultPy), (DefaultQx, DefaultQy) )
    Rx_mod2p, Ry_mod2p = RValue_mod2p( (DefaultPx, DefaultPy), (DefaultQx, DefaultQy) )

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.grid()

    return render_template('modk-add.html', rz=rz, line_through_g=rz, Rx_modp=Rx_modp, Ry_modp=Ry_modp, Rx_mod2p=Rx_mod2p, Ry_mod2p=Ry_mod2p)

def inverse_mod(k, p):
   
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    if k == 0:
        raise ZeroDivisionError('division by zero')
    if k < 0:
        return p - inverse_mod(-k, p)
    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    return x % p


def double(P):
    Px, Py = P
    slope = (( (3 * (Px ** 2)) * inverse_mod(2 * Py, PValue) )) % PValue
    x = ( (slope ** 2) - (2 * Px)) % PValue
    y = (slope * (Px - x) - Py ) % PValue
    return (x,y)

def multiply(k,point=(Gx, Gy)):
    current = point 
    b = bin(k)
    binary = b[2:]
    for char in binary:
        current = double(current)
        if char == "1":
            current = RValue(current, point)
    return None


@app.route("/_mod_addition")
def mod_add():
    # Modulus
    img = io.BytesIO()

    Px = int(request.args.get('px',0,int))
    Py = int(request.args.get('py',0,int))
    Qx = int(request.args.get('qx',0,int))
    Qy = int(request.args.get('qy',0,int))

    Rx_modp, Ry_modp = RValue( (Px, Py), (Qx, Qy) )
    Rx_mod2p, Ry_mod2p = RValue_mod2p( (Px, Py), (Qx, Qy) )

    sx = [Px, Qx, Rx_modp]
    sy = [Py, Qy, Ry_modp]

    rz = atZero( (Px, Py), (Qx, Qy) )
    
    return jsonify({'rz': rz, 
                    'line_through_g': rz, 
                    'a': str(Ry_modp),
                    'rx_modp': str(Rx_modp), 
                    'ry_modp': str(Ry_modp),
                    'rx_mod2p': str(Rx_mod2p),
                    'ry_mod2p': str(Ry_mod2p)
                  })

    
def hash_256_from_hex_string_like_bytes(hexstring: str):
    return sha256(bytes.fromhex(hexstring)).hexdigest()

def ripemd160_from_hex_string_like_bytes(hexstring: str):
    return new('ripemd160', bytes.fromhex(hexstring)).hexdigest()

def sha_ripe_digest(hex_string_to_checksum):
    hashc1 = hash_256_from_hex_string_like_bytes(hex_string_to_checksum)
    hashc2 = ripemd160_from_hex_string_like_bytes(hashc1)
    return hashc2.upper()

def sha256_get_checksum(hex_string_to_checksum):
    hasha1 = hash_256_from_hex_string_like_bytes(hex_string_to_checksum)
    # print("HashA1", hasha1)
    hasha2 = hash_256_from_hex_string_like_bytes(hasha1)
    # print("HashA2", hasha2)
    return hasha2[:8].upper()

def b58encode(hex_string, expected_length=None):
    v = binascii.unhexlify(hex_string)
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    lev, number = 1, 0
    for char in reversed(v):
        number += lev * char
        lev = lev << 8  # 2^8
    string = ""
    while number:
        number, modulo = divmod(number, 58)
        string = alphabet[modulo] + string
    if not expected_length:
        return string
    elif len(string) != expected_length:
        raise Exception(f"b58encode: Expected length={expected_length} obtained length={len(string)}")
    else:
        return string

def hex_public_to_public_addresses(hex_publics):
    uncompressed = hex_publics
    public_key_hashC_uncompressed = "00" + sha_ripe_digest(uncompressed)
    checksum = sha256_get_checksum(public_key_hashC_uncompressed)
    PublicKeyChecksumC = public_key_hashC_uncompressed + checksum
    public_address_uncompressed = "1" + b58encode(PublicKeyChecksumC, 33)
    #print("Public address uncompressed:\t", public_address_uncompressed)
    return public_address_uncompressed

if __name__ == '__main__':

    #Test 2
    px2 = 20131979211061389967751131264678527958175244405833067093780319892079931982003
    py2 = 97739400561097470892304758517697903219823751918482384097704428900997592914452
 
    qx2 = 3110312095956218672199054275855287122563277688985124808786333320921364917406
    qy2 = 37876912097499250873068094917849140669589073080654473765979021074106692303005

    #Test 5
    px5 = 111386653702928498438210543587694059852557464044625577365950565957075797233859
    py5 = 11627437750286147394364244714515275317324809791379124524916276925749558022274

    qx5 = 18987839139458821171764383611033286003599317517728450167230613632453532645617
    qy5 = 74957358265573496758837787484033884875007782526873647488473254115707719229729
    
    #Test6
    px6 = 57950323574031113507242725402012892184835813891210007786510734268948311896155
    py6 = 80417912802329255677878571421122691638026994009162974239972935647548500727785

    qx6 = 23356342954826335616876035065214442486893957595758241080908971145135527322432
    qy6 = 104849726249746422487891434741829100644994550713215136641463619492046526925720
    
    iRV2 =       RValue1( (px2,py2),(qx2,qy2) )
    iRV2_mod2p = RValue1_mod2p( (px2,py2),(qx2,qy2))
    iRV2_nomod = RValue1_no_modp( (px2,py2),(qx2,qy2) )
    
    RV2 =       RValue1((qx2,qy2), (px2,py2))
    RV2_mod2p = RValue1_mod2p( (qx2,qy2), (px2,py2) )
    RV2_nomod = RValue1_no_modp( (qx2,qy2), (px2,py2) )
    
    '''print("-------------------------R2----------------------------------------------------")
    print("RValue: {}".format(iRV2))
    print("RValue Mod2p: {}".format(iRV2_mod2p))
    print("RValue NoMod: {}".format(iRV2_nomod))'''
    
    '''print("-------------------------R2 INVERSE----------------------------------------------------")
    print("RValue: {}".format(RV2))
    print("RValue Mod2p: {}".format(RV2_mod2p))
    print("RValue NoMod: {}".format(RV2_nomod))'''
    
    iRV5 =       RValue1((px5,py5),(qx5,qy5))
    iRV5_mod2p = RValue1_mod2p( (px5,py5), (qx5,qy5) )
    iRV5_nomod = RValue1_no_modp( (px5,py5), (qx5,qy5) )
    
    RV5 =       RValue1((qx5,qy5),(px5,py5))
    RV5_mod2p = RValue1_mod2p( (qx5,qy5), (px5,py5) )
    RV5_nomod = RValue1_no_modp( (qx5,qy5), (px5,py5) )
    
   
    '''print("----------------------------R5-------------------------------------------------- ")
    print("RValue: {}".format(iRV5))
    print("RValue Mod2p: {}".format(iRV5_mod2p))
    print("RValue NoMod: {}".format(iRV5_nomod))'''
   
    '''print("----------------------------R5 INVERSE---------------------------------------------------------------------------------------------------- ")
    print("RValue: {}".format(RV5))
    print("RValue Mod2p: {}".format(RV5_mod2p))
    print("RValue NoMod: {}".format(RV5_nomod))'''
    
    iRV6 =       RValue1((px6,py6),(qx6,qy6))
    iRV6_mod2p = RValue1_mod2p( (px6,py6),(qx6,qy6) )
    iRV6_nomod = RValue1_no_modp( (px6,py6),(qx6,qy6) )
    
    RV6 =       RValue1((qx6,qy6), (px6,py6))
    RV6_mod2p = RValue1_mod2p( (qx6,qy6), (px6,py6) )
    RV6_nomod = RValue1_no_modp( (qx6,qy6), (px6,py6) )
    
    '''print("----------------------------R6-------------------------------------------------- ")
    print("RValue: {}".format(iRV6))
    print("RValue Mod2p: {}".format(iRV6_mod2p))
    print("RValue NoMod: {}".format(iRV6_nomod))'''
    
    print("----------------------------R6 INVERSE-------------------------------------------------- ")
    print("RValue: {}".format(RV6))
    print("RValue Mod2p: {}".format(RV6_mod2p))
    print("RValue NoMod: {}".format(RV6_nomod))
    

    '''
    print("-------------------------modp----------------------------------")
    RValue1()
    print("-------------------------mod2p----------------------------------")
    RValue1_mod2p()
    print("-------------------------without mod----------------------------------")
    RValue1_no_modp()
    '''

    app.run(debug=True, threaded=True)