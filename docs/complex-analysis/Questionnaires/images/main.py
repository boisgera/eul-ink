#!/usr/bin/env python
# coding: utf-8
# Python 2.7 Directives
from __future__ import print_function
from __future__ import division

# Python 2.7 Standard Library
import json
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp

#
# Matplotlib Configuration & Helper Functions
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
    "font.family": "serif",
    "font.serif": [],
    "font.sans-serif": [],
    "legend.fontsize": 10, 
    "axes.titlesize":  10,
    "axes.labelsize":  10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
}
mpl.rcParams.update(rc)

# Use PGF to render PDF with LaTeX fonts of the proper size.
from matplotlib.backends.backend_pgf import FigureCanvasPgf
mpl.backend_bases.register_backend("pdf", FigureCanvasPgf)

# The width of the standard LaTeX document is 345.0 pt.
width_in = 345.0 / 72.0

def save(name, dpi=None):
    options = {}
    if dpi:
        options["dpi"] = dpi
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf")
    pp.savefig(name + ".svg")
    os.chdir(cwd)

def set_ratio(ratio, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)

def count(list):
    result = {}
    for item in list:
      result[item] = result.get(item, 0) + 1
    return result

def hist(answers, filename=None):
  pp.clf()
  n, bins, patches = pp.hist(answers, 5, range=(-0.5, 4.5), normed=True, rwidth=0.5)
  pp.grid(True)
  pp.gca().set_axisbelow(True)
  set_ratio(5.0, bottom=0.18, top=0.20)
  pp.axis([-0.5, 4.5, 0.0, 1.0])
  xlabels = ["N/A", "Non (1.0)", "Plut\^ot Non", "Plut\^ot Oui", "Oui (4.0)"]
  pp.xticks([0, 1, 2, 3, 4], xlabels)
  pp.yticks([0.0, 0.25, 0.5, 0.75, 1.0], ["0\%", "25\%", "50\%", "75\%", "100\%"])
  pp.setp(patches, 'facecolor', '#d3d3d3', 'edgecolor', 'k')
  mean_ = np.mean([a for a in answers if a!=0])
  pp.plot([mean_, mean_], [0.0, 1.0], "k-", linewidth=1.0)
  pp.text(mean_-0.12, 1.05, "{0:.2f}".format(mean_), size="8")
  pp.show()
  if filename:
    save(filename, dpi=600)

data = json.load(open("../data.json"))

pre = [d.get("prerequisite") or 0 for d in data]
hist(pre, "prerequisite")

hist([d.get("interest") or 0 for d in data], "interest")

hist([d.get("lectures").get("content") or 0 for d in data], "amphi-content")
hist([d.get("lectures").get("style") or 0 for d in data], "amphi-style")

hist([d.get("tutorials").get("content") or 0 for d in data], "tuto-content")
hist([d.get("tutorials").get("style") or 0 for d in data], "tuto-style")

hist([d.get("workshops").get("keep") or 0 for d in data], "w-keep")
hist([d.get("workshops").get("content") or 0 for d in data], "w-content")
hist([d.get("workshops").get("style") or 0 for d in data], "w-style")

hist([d.get("documents").get("lectures") or 0 for d in data], "doc-lectures")
hist([d.get("documents").get("workshops") or 0 for d in data], "doc-workshops")

hist([d.get("exam").get("rating") or 0 for d in data], "exam-rating")

hist([d.get("rating") or 0 for d in data], "rating")

