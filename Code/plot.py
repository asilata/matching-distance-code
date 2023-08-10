import matplotlib.pyplot as plt
import numpy as np


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
