#!/usr/bin/env python3

import graphics as gr
import os

window = gr.GraphWin("fractal", 600, 600)
alpha = 0.03

def fractal_rectangle(a, b, c, d, deep=10):
    if deep < 1:
        return
    for i, j in (a, b), (b, c), (c, d), (d, a):
        gr.Line(gr.Point(*i), gr.Point(*j)).draw(window)
    
    a1 = (a[0] * (1 - alpha) + b[0] * alpha, a[1] * (1 - alpha) + b[1] * alpha)
    b1 = (b[0] * (1 - alpha) + c[0] * alpha, b[1] * (1 - alpha) + c[1] * alpha)
    c1 = (c[0] * (1 - alpha) + d[0] * alpha, c[1] * (1 - alpha) + d[1] * alpha)
    d1 = (d[0] * (1 - alpha) + a[0] * alpha, d[1] * (1 - alpha) + a[1] * alpha)
    fractal_rectangle(a1, b1, c1, d1, deep - 1)

fractal_rectangle((100, 100), (500, 100), (500, 500), (100, 500), 200)
os.system("pause")
