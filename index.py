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


app = Flask(__name__)

def getLinePoints():

    return [ [(0,6), (0,250)], [(0,0), (0,0)], [(0,0),(0,0)], [(0,0),(0,0)], [(0,1), (0,0)]]

def getCurvePoints():

    return [ [(0,0),(0,0)]]

@app.route('/')
def index():
    img = io.BytesIO()

    DefaultPx = 76713794182478803891528803692822015505111471502816304530189645921738551553824
    DefaultPy = 9989913769501776956673418849599695616596036032394306022682365229231505097463
    DefaultQx = 49396472789695839840842700318753929600130929079169291199003099305862335813206
    DefaultQy = 6721877582892931413141315114289651970823246064430791708367976298368088092295
    Rx, Ry = RValue( (DefaultPx, DefaultPy), (DefaultQx, DefaultQy) )

    DefaultGx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    DefaultGy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

    a = -1
    b = 1
    min = 0
    max =  1.2 *  10**78
    
    y,x = np.ogrid[ min:max:0.2 * 10**78, min:max:0.2 * 10**78 ]
    print("Ravel")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.contour(x.ravel(), y.ravel(), y**2 - x**3 - x * a -b, [0])
    plt.grid()
    
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
    ax.tick_params(axis='both', which='major', labelsize=6)

    #ax.set_xticks( np.arange(min,max, 1 * 10**77) )
    #ax.set_xticks( np.arange(min,max, 0.1 * 10**77), minor=True )
    #ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    #ax.yaxis.set_minor_locator(AutoMinorLocator(4))

     #Points Annotation
    plt.annotate("P", (DefaultPx, DefaultPy))
    plt.annotate("Q", (DefaultQx, DefaultQy))
    plt.annotate("R", (Rx, Ry))
    plt.annotate("G", (DefaultGx, DefaultGx))

    #Scatter Plot
    sx = [DefaultPx, DefaultQx, DefaultGx, Rx]
    sy = [DefaultPy, DefaultQy, DefaultGy, Ry]

    scolors = ['red', 'green', 'blue', 'purple']
    plt.scatter(DefaultPx, DefaultPy, color=scolors[0])
    plt.scatter(DefaultQx, DefaultQy, color=scolors[1])
    plt.scatter(DefaultGx, DefaultGy, color=scolors[2])
    plt.scatter(Rx, Ry, color=scolors[3])

    #Check if G intersects
    #is_on_curve(DefaultGx, DefaultGy)

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('modk-add.html', figure=plot_url)

def inverse_mod(k, p):
    #p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    if k == 0:
        raise ZeroDivisionError('division by zero')
    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
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

def RValue(P,Q):
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    Px,Py = P 
    Qx,Qy = Q
    if Px == Qx:
        Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
    else:
        Delta = (Py - Qy) * inverse_mod(Px - Qx, p)

    Rx = ( Delta * Delta - Px - Qx ) % p
    Ry = Py + Delta * (Rx - Px)
    Ry = -Ry % p
    return (Rx,Ry)


@app.route("/_mod_addition")
def mod_add():
    # Modulus

    img = io.BytesIO()

    #p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
    Px = int(request.args.get('px',0,int))
    Py = int(request.args.get('py',0,int))
    Qx = int(request.args.get('qx',0,int))
    Qy = int(request.args.get('qy',0,int))
    
    if Px == Qx:
        Delta = (3 *  Px * Px ) * inverse_mod(2 * Py, p)
    else:
        Delta = (Py - Qy) * inverse_mod(Px - Qx, p)

    Rx = ( Delta * Delta - Px - Qx ) % p
    Ry = Py + Delta * (Rx - Px)
    Ry = -Ry % p

    a = -1
    b = 1
    min = 0
    max =  1.2 *  10**78
    
    y,x = np.ogrid[ min:max:10**78, min:max:10**78 ]
    print("Ravel")
    #print(x.ravel())
    #print(y.ravel())

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.contour(x.ravel(), y.ravel(), y**2 - x**3 - x * a -b, [0])
    plt.grid()
    
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))

    plt.annotate("P", (Px, Py))
    plt.annotate("Q", (Qx, Qy))
    plt.annotate("R", (Rx, Ry))
    #plt.annotate("G", (DefaultGx, DefaultGx))

    sx = [Px, Qx, Rx]
    sy = [Py, Qy, Ry]

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return jsonify({'rx': str(Rx), 'ry': str(Ry), 'figure': plot_url  })

def is_on_curve(self, x, y):
    a = 0
    b = 7
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f 
    if x is None or y is None:
        return True
    return (y * y - x * x * x - a * x - b) % p == 0

def y_value(x):
    return sqrt(x**3 + 7)
    
if __name__ == '__main__':
    app.run(debug=True)