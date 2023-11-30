import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from matplotlib import rc

# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=True)


def plotmod(CritPts, Pts):
    fig = plt.figure()
    ax = fig.gca()

    for pt in Pts:
        plt.scatter(pt[0], pt[1], c="C1")
    for crit in CritPts:
        plt.scatter(crit.coords[0], crit.coords[1], c="C2")

    ax.set_xticks(np.arange(-7, 10, 1))
    ax.set_yticks(np.arange(-4, 10, 1))

    # plot line of equation y = 10/7 x +1
    x = np.linspace(-7, 10, 100)
    y = 10 / 7 * x + 1
    plt.plot(x, y, "-r", label="y=10/7x+1")

    # plot linr of slope 1 thrrough (7,11)
    x = np.linspace(-7, 10, 100)
    y = x + 4
    plt.plot(x, y, "-r", label="y=x+4")

    plt.grid(axis="both", color="0.95")
    return None


def plot_both_c_o(critpts, omegapts, title, dpi, alg):
    fig, ax = plt.subplots()
    fig.set_dpi(dpi)
    fig.set_size_inches(5, 5)
    ax.set_aspect("equal")
    for c in critpts:
        ax.plot(c.coords[0], c.coords[1], "o", color="black", label="black")
    for o in omegapts:
        ax.plot(o[0], o[1], "o", color="red", label="red")
    plt.title(alg + " Algorithm for " + title)

    red_patch = mpatches.Patch(color="red", label="omega points")
    black_patch = mpatches.Patch(color="black", label="critical points")
    plt.legend(handles=[red_patch, black_patch])
    plt.show()
