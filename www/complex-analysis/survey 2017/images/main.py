#!/usr/bin/env python
# coding: utf-8
# Python 2.7 Directives
from __future__ import print_function
from __future__ import division

# Python 2.7 Standard Library
import csv
import json
import os
import re

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

# ------------------------------------------------------------------------------
csvfile = open("../Questionnaire Maths 3 (C1223 _ S1224).csv")

reader = csv.reader(csvfile, delimiter=",", quotechar='"')
test = []
hists = [(4, "niveau"), (5, "interet"), 
         (8, "format-cours"), (9, "encadrant-cours"), (10, "contenu-cours"),
         (14, "encadrant-PC"), (15, "contenu-PC"),
         (18, "encadrant-atelier"), (19, "contenu-atelier"),
         (21, "poly"), (22, "anglais"),
         (27, "satisfaction")
        ]

SESSIONS = [
  "Complex-Differentiability",
  "Line Integrals & Primitives",
  "Connected Sets",
  "Cauchy's Integral Theorem (Local Version)",
  "The Winding Number",
  "Cauchy's Integral Theorem (Global Version)",
  "Power Series",
  "Zeros & Poles",
  "Analytic Functions",
  "Integral Representations"
]

RESOURCES = [
  "Informations générales (agenda, préparation séjour, etc.)",
  "Cours en PDF (document électronique ou destiné à l'impression)",
  "Cours en HTML (version en ligne)",
  "Fichiers sources du cours (documents en markdown, programmes générant les images, etc.)",
  "Ressources mathématiques complémentaires (autres cours d'analyse complexe,  articles associés, etc.)",
  "Documents de la session 2016 (sujet d'examen corrigé, distribution des notes, résultats des questionnaires)",
]

def escape(s):
    return s.replace("&", "\&").replace("é", r"\'e").replace("à", r"\a").\
             replace("è", "\\`e")

S = 10 * [0.0]
R = 6 * [0.0]
data = {}
first = True
for i, row in enumerate(reader):
    if first:
       first = False
       continue
#    print(70*"-")
#    for i, item in enumerate(row):
#        print(i, item)
    for number, name in hists:
        #print(row)        
        item = row[number]
        if item:
            data.setdefault(number, []).append(int(item))
        else:
            data.setdefault(number, []).append(0)

    sessions = [s.strip() for s in row[11].split(";")]
    for session in sessions:
        if session:
            #print("*")
            S[SESSIONS.index(session)]+=1.0

    resources = [r.strip() for r in row[23].split(";")]
    for resource in resources:
        if resource:
            #print("*")
            R[RESOURCES.index(resource)]+=1.0

for number, name in hists:
  hist(data[number], name)


# ------------------------------------------------------------------------------




#i = 0
#reader = csv.reader(csvfile, delimiter=",", quotechar='"')
#for i, row in enumerate(reader):
#    if i != 0:

#        Arcs = not row[7].startswith("Lionel Rosier")

#        LE = row[7].decode("utf-8") or u"?"
#        AM.setdefault(LE, []).append((row[8], row[9], row[10]))

#        TA = row[13].decode("utf-8") or u"?"
#        PC.setdefault(TA, []).append((row[14], row[15]))

#        TA = row[17].decode("utf-8") or u"(?)"
#        name = re.search(r'\((.*?)\)', TA).group(1)
#        if name.startswith("Camille"):
#            if Arcs:
#                name = "Marin Boyet et Arnaud Larroche"
#            else:
#                name = "Camille Laurent"
#        AT.setdefault(name, []).append((row[18], row[19]))

#        sessions = [s.strip() for s in row[11].split(";")]
#        for session in sessions:
#            if session:
#                print("*")
#                S[SESSIONS.index(session)]+=1.0

N = i + 1

for k, v in enumerate(S):
    S[k] = S[k] / float(N) * 100.0

for i in range(10):
    print(SESSIONS[i] + ":", "{0:.1f}%".format(S[i]))

for k, v in enumerate(R):
    R[k] = R[k] / float(N) * 100.0

for i in range(6):
    print(RESOURCES[i] + ":", "{0:.1f}%".format(R[i]))

pp.clf()

# ------------------------------------------------------------------------------
m = 5
y_pos = m*(10 - np.arange(len(SESSIONS)))
pp.barh(y_pos, len(y_pos)*[100], height=3.0, align='center', color='white', edgecolor="k")
pp.barh(y_pos, S, height=3.0, align='center', color='#d3d3d3', edgecolor="k")
for i, label in enumerate(SESSIONS):
    print(escape(label))
    pp.text(95.0, y_pos[i]-0.5, escape(label), horizontalalignment="right",
            size=10)
set_ratio(0.80, left=0.10, bottom=0.15, top=0.15)
pp.axis([0.0, 100.0, 0.0, m*11])
#pp.gca().get_yaxis().set_visible(False)
pp.yticks(y_pos, range(1,11))
pp.xticks([00, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
pp.grid(True)
pp.gca().set_axisbelow(True)
pp.title("Sessions posant probl\`eme", size=12)
#pp.ylabel(ur"Session")
pp.xlabel(ur"Pourcentage de r\'eponses positives")
save("sessions")

# ------------------------------------------------------------------------------

pp.clf()
m = 5
y_pos = m*(6 - np.arange(len(RESOURCES)))
pp.barh(y_pos, len(y_pos)*[100], height=3.0, align='center', color='white', edgecolor="k")
pp.barh(y_pos, R, height=3.0, align='center', color='#d3d3d3', edgecolor="k")
for i, label in enumerate(RESOURCES):
    #print(escape(label))
    #print(repr(re.sub(r"\([^)]*\)", "", escape(label))))
    pp.text(95.0, y_pos[i]-0.4, re.sub(r"\([^)]*\)", "", escape(label)).strip(), horizontalalignment="right",
            size=10)
set_ratio(1.2, left=0.10, bottom=0.15, top=0.15)
pp.axis([0.0, 100.0, 0.0, m*7])
#pp.gca().get_yaxis().set_visible(False)
pp.yticks(y_pos, range(1,7))
pp.xticks([00, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
pp.grid(True)
pp.gca().set_axisbelow(True)
pp.title(r"Ressources utiles", size=12)
#pp.ylabel(ur"Session")
pp.xlabel(ur"Pourcentage de r\'eponses positives")
save("resources")


# ------------------------------------------------------------------------------

#data = json.load(open("../data.json"))

#pre = [d.get("prerequisite") or 0 for d in data]
#hist(pre, "prerequisite")

#hist([d.get("interest") or 0 for d in data], "interest")

#hist([d.get("lectures").get("content") or 0 for d in data], "amphi-content")
#hist([d.get("lectures").get("style") or 0 for d in data], "amphi-style")

#hist([d.get("tutorials").get("content") or 0 for d in data], "tuto-content")
#hist([d.get("tutorials").get("style") or 0 for d in data], "tuto-style")

#hist([d.get("workshops").get("keep") or 0 for d in data], "w-keep")
#hist([d.get("workshops").get("content") or 0 for d in data], "w-content")
#hist([d.get("workshops").get("style") or 0 for d in data], "w-style")

#hist([d.get("documents").get("lectures") or 0 for d in data], "doc-lectures")
#hist([d.get("documents").get("workshops") or 0 for d in data], "doc-workshops")

#hist([d.get("exam").get("rating") or 0 for d in data], "exam-rating")

#hist([d.get("rating") or 0 for d in data], "rating")

