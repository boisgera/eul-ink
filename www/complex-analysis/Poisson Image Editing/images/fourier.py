#!/usr/bin/env python

# Future
from __future__ import absolute_import, division, print_function

# Python 2.7 Standard Library
pass

# Third-Party Packages
import numpy as np
import PIL.Image

# ------------------------------------------------------------------------------
N = 1024
R, R_1, R_2 = 0.75, 0.85, 0.95

# ------------------------------------------------------------------------------
def xy(i, j, N=N):
    x = -1 + 2 / N * (    j + 0.5)
    y = -1 + 2 / N * (N - i - 0.5)
    return x, y

def save(array, filename):
    uint8s = (255 * array).astype(np.uint8)
    PIL.Image.fromarray(uint8s).save(filename)

def dirichlet(n, N=N):
    i = np.r_[0:N]
    j = np.r_[0:N]
    I, J = np.meshgrid(i, j, indexing="ij")
    X, Y = xy(I, J, N)
    Z = X + 1j * Y

    image = (1 + np.cos(n * np.angle(Z))) / 2
    save(image, "dirichlet-original-{0}.png".format(n))

    uniform = 0.95 * np.ones_like(image)
    save(np.c_[image, uniform], "dirichlet-original-and-source-{0}.png".format(n))

    circ = (abs(Z) > R_1) * (abs(Z) < R_2)
    boundary = image * circ
    save(boundary, "dirichlet-boundary-values-{0}.png".format(n))

    disk = abs(Z) < R
    circ = (abs(Z) > R_1) * (abs(Z) < R_2)
    image_2 = image.copy() * circ
    image_2[disk] = (0.5  + ((abs(Z) / R) ** n) * 0.5 * np.cos(n * np.angle(Z)))[disk]
    save(image_2, "dirichlet-solution-{0}.png".format(n))

    image[disk] = image_2[disk]
    save(image, "dirichlet-healed-{0}.png".format(n))

    save(np.c_[image_2, image], "dirichlet-solution-and-healed-{0}.png".format(n))

def analytic(n=9, N=N):
    i = np.r_[0:N]
    j = np.r_[0:N]
    I, J = np.meshgrid(i, j, indexing="ij")
    X, Y = xy(I, J, N)
    Z = X + 1j * Y

    image = 0.25 * (1 + 3 / (5 - 4 * np.cos(np.angle(Z))))
    save(image, "dirichlet-analytic.png")

    images = []
    disk = abs(Z) < R
    image[disk] = 0
    for i in range(n+1):
        image[disk] += (2**(-i-1) * ((np.abs(Z) / R) ** i) * np.cos(i * np.angle(Z)))[disk]
        images.append(image.copy())
        save(image, "dirichlet-analytic-healed-{0}.png".format(i))
    image = np.r_[
              np.c_[images[0], images[1], images[2]],
              np.c_[images[3], images[4], images[5]],
#              np.c_[images[6], images[7], images[8]],
            ]    
    save(image, "dirichlet-analytic-all.png")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    for n in range(12):
        dirichlet(n=n)
      


