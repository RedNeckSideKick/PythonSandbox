# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:18:44 2020

@author: redne
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

# Minmums/maximums for the Mandelbrot Set
real_min = -0.84010
real_max = -0.84000
imag_min =  0.22425j
imag_max =  0.22435j

res = 999   # Resolution

# Make the starting complex domain array
domain_real = np.linspace(real_min, real_max, res)
domain_imag = np.linspace(imag_min, imag_max, res)

mesh_real, mesh_imag = np.meshgrid(domain_real, domain_imag)

domain_cmplx = mesh_real + mesh_imag

# Mandelbrot generator
def Mandelbrot(domain, iter_lim = 100):
    mandelbrot = np.zeros_like(domain)
    step = np.full_like(domain, -10, dtype=int)
    for i in trange(iter_lim):
        yield step, mandelbrot
        mandelbrot = (mandelbrot ** 2) + domain 
        step[(np.abs(mandelbrot) >= 2.0) & (step < 0)] = i

for step, mandelbrot in Mandelbrot(domain_cmplx, 250):
    pass

fig, ax = plt.subplots(1)
display = ax.imshow(step, cmap=plt.cm.inferno, origin='lower',\
                    extent=[real_min, real_max, imag_min.imag, imag_max.imag])
# plt.imsave(step, 'mandelbrot.png', cmap=plt.cm.inferno, origin='lower',\
#            extent=[real_min, real_max, imag_min.imag, imag_max.imag])