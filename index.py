from flask import Flask, render_template, request, jsonify
import pandas
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import json

app = Flask(__name__)


def create_plot(args):
    xScale = [args.px, args.qx, args.rx]
    yScale = [args.py, args.qy, args.ry]

    trace = go.Scatter(xScale, yScale)
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('', graphJSON=graphJSON)

@app.route('/')
def index():
    return render_template('modk-add.html')

def inverse_mod(k, p):
    p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
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

@app.route("/_mod_addition")
def mod_add():
    p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    Px = int(request.args.get('px',0,int))
    Py = int(request.args.get('py',0,int))
    Qx = int(request.args.get('qx',0,int))
    Qy = int(request.args.get('qy',0,int))
    
    Delta = ( (Py - Qy) * inverse_mod( (Px - Qx), p) ) 
    Rx = ( Delta ** 2 - Px - Qx ) % p
    Ry = ( Delta * (Px - Rx) - Qy ) % p
    
    return jsonify({'rx': str(Rx), 'ry': str(Ry) })

def y_value(x):
    return sqrt(x**3 + 7)
    
if __name__ == '__main__':
    app.run(debug=True)