from flask import Flask, Response, render_template, request, jsonify
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
import io
import random

app = Flask(__name__)

@app.route('/')
def index():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    x_points = range(50)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)

    return render_template('modk-add.html', output=output.getvalue())

# Test Image Plot
@app.route('/plot_png')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    x_points = range(50)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


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

@app.route("/_mod_addition")
def mod_add():
    # Modulus
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

    #Slope = (3x^2 + a) / 2y
    #Delta = ( (Py - Qy) * inverse_mod( (Px - Qx), p) ) 
    Rx = ( Delta * Delta - Px - Qx ) % p
    Ry = Py + Delta * (Rx - Px)
    Ry = -Ry % p
    
    return jsonify({'rx': str(Rx), 'ry': str(Ry) })

def y_value(x):
    return sqrt(x**3 + 7)
    
if __name__ == '__main__':
    app.run(debug=True)