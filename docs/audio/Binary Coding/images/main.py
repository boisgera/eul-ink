#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import matplotlib as mpl
import matplotlib.pyplot as pp

#
# Matplotlib Configuration
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": [],      # use latex default serif font
    "font.sans-serif": [], # use a specific sans-serif font
    "legend.fontsize": 10, # "medium" make it 10 (equivalent)
    "axes.titlesize":  10,
    "axes.labelsize":  10,
    "xtick.labelsize": 10, # alt: "small",
    "ytick.labelsize": 10, # alt: "small",
}
mpl.rcParams.update(rc)

# Use PGF to render PDF with LaTeX fonts of the proper size.
from matplotlib.backends.backend_pgf import FigureCanvasPgf
mpl.backend_bases.register_backend("pdf", FigureCanvasPgf)

# The width of the standard LaTeX document is 345.0 pt.
width_in = 345.0 / 72.0

#
# Helper Functions
# ------------------------------------------------------------------------------
#
def save(name, dpi=None, prefix=""):
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    pp.savefig(prefix + name + ".pdf", **options)
    pp.savefig(prefix + name + ".png", **options)
    pp.savefig(prefix + name + ".pgf")
    pp.savefig(prefix + name + ".svg")


def set_ratio(ratio, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)


# Information Content
# ------------------------------------------------------------------------------

p = np.arange(0.001, 1.0, 0.001)
i = np.log2(1/p)

pp.plot(p, i, "k", linewidth=1.00)
pp.axis([0.0, 1.0, 0.0, 3.0])
pp.xticks([0.0, 0.25, 0.5, 0.75, 1.0])
#grid(True)
pp.xlabel(ur"probability $P(E)$")
#ylabel("information content")
pp.title("Shannon information content")
pp.gca().text(0.45, 2.0, ur"$I(E) = -\log_2 P(E)$")
pp.gcf().subplots_adjust(bottom=0.20)

set_ratio(1.618, bottom=0.15)
save("information_content")

# Brainfuck Binary Tree
#-------------------------------------------------------------------------------

def qtree(name, src):

    print "*** Generating " + name + " Tree ***"

    full_src = r"""
\documentclass{standalone}
\usepackage{qtree}
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amsfonts}
\setmonofont{Inconsolata}
\begin{document}
\begin{minipage}[c]{345pt}""" + src + \
r"""\end{minipage}
\end{document}"""

    file = open("/tmp/" + name + ".tex", "w")
    file.write(full_src)
    file.close()

    os.system("xelatex /tmp/" + name + ".tex")
    os.system("pdf2svg " + name + ".pdf " + name + ".svg")

qtree("brainfuck-tree",r"""
\Tree [ 
        [ 
          [  
            {\tt -}  
            [ 
              [ 
                {\tt [}
                [ 
                  {\tt .} 
                  [
                    {\tt ,}  
                    [ 
                      {\tt (*)} 
                      {\tt (!)}
                    ] 
                  ]
                ] 
              ] 
              {\tt ]} 
            ] 
          ] 
          [ {\tt >} {\tt <} ] 
        ]
        {\tt +} 
      ]
"""
)


qtree("huffmann-1", r"""
\Tree [ 
  {$\{3,4,\cdots\}, 0.125$} {$2, 0.125$}  {$1, 0.25$} {$0, 0.5$}
]
""")
qtree("huffmann-2", r"""
\Tree [ 
[.{$\{2,3,\cdots\}, 0.25$} {$\{3,4,\cdots\}, 0.125$} {$2, 0.125$} ] {$1, 0.25$} {$0, 0.5$} 
]
""")
qtree("huffmann-3", r"""
\Tree [.{$\mathbb{N}, 1.0$} 
  [.{$\{1,2,\cdots\}, 0.5$} 
    [.{$\{2,3,\cdots\}, 0.25$} {$\{3,4,\cdots\}, 0.125$} {$2, 0.125$} ] {$1, 0.25$} ] {$0, 0.5$} 
]
""")

