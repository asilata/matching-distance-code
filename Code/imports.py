import gudhi
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib
import matplotlib.patches as mpatches
from matplotlib import rc
import math
from math import cos, sin, pi, atan     
import itertools
# from scipy.stats import qmc
import scipy.spatial
from scipy.optimize import linprog
import random as rnd
import sys 
if sys.version_info[0:3] != (3, 9, 6):
    raise Exception('!!! Requires python 3.9.6; please install it!!!')
# sys.path.append('../Code/')
import modules as mod
import examples as ex
import plot as ourplot
import csv
import bunny_smaller
import omega_pts as omega
import cleanup_helper_funcs as chf
import time
