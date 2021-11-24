import numpy as np
import matplotlib.pyplot as plt

def main():
    a = -1
    b = 1

    y,x = np.ogrid[-5*10^76:5:100j, -5:5:100j]
    plt.contour(x.ravel(), y.ravel(), y**2 - x**3 -x*a - b, [0])
    plt.grid()
    plt.show()

def add():
    a = 7671379418247880389152880369282015505111471502816304530189645921738551553824
    b = 49396472789695839840842700318753929600130929079169291199003099305862335813206
    c = a + b
    print(c)
    #return a + b

if __name__ == '__main__':
    add()