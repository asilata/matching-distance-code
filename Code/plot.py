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
    ax.set_xlim(-5, 35)
    ax.set_ylim(-5, 20)
    for c in critpts:
        if c.parent_module == 0:
            ax.plot(c.coords[0], c.coords[1], "o", color="black", label="black")
        else:
            ax.plot(c.coords[0], c.coords[1], "o", color="orange", label="orange")

    for o in omegapts:
        # apparently sometimes at the end of omegapts we spit out the number of points too,
        # so it can be an int. We might want to fix.
        ax.plot(o[0], o[1], "o", color="red", label="red", alpha=0.8)
        # if type(o) is not int:
        #     ax.plot(o[0], o[1], "o", color="red", label="red", alpha=1.0)
    plt.title(alg + " Algorithm for " + title)

    red_patch = mpatches.Patch(color="red", label="omega points")
    black_patch = mpatches.Patch(color="black", label="critical points from M")
    orange_patch = mpatches.Patch(color="orange", label="critical points from N")

    plt.legend(handles=[red_patch, black_patch, orange_patch], loc="best")
    plt.show()


def plot_c_o_with_inf(critpts, orderedomegas, is_inf, title, dpi, alg):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    fig.set_dpi(dpi)
    # fig.set_size_inches(5, 5)
    fig.tight_layout
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    # ax1.set_xlim(-5, 20)
    # ax1.set_ylim(-5, 10)

    ## draw quarter circle
    theta = np.linspace(0, np.pi / 2, 100)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax2.plot(x, y, "--", color="black")

    for c in critpts:
        if c.parent_module == 0:
            ax1.plot(c.coords[0], c.coords[1], "o", color="black", label="black")
        else:
            ax1.plot(c.coords[0], c.coords[1], "o", color="orange", label="orange")
    for o in orderedomegas:
        # the first entry is a string
        if orderedomegas.index(o) == 0:
            continue
        # apparently sometimes at the end of omegapts we spit out the number of points too,
        # so it can be an int. We might want to fix.
        if is_inf[orderedomegas.index(o)] == None:
            ax1.plot(o[0], o[1], "o", color="red", label="red", alpha=1.0)
        else:
            print("infty point:", is_inf[orderedomegas.index(o)])
            # ax2.plot(o[0], o[1], "o", color="red", label="red", alpha=1.0)
            slope = is_inf[orderedomegas.index(o)]
            # maybe draw intersection
            # Calculate the coordinates of the intersection point
            x_intersection = radius / np.sqrt(1 + slope**2)
            y_intersection = slope * x_intersection

            # Plot the line through (0,0) with slope m
            x_line = np.linspace(0, x_intersection, 100)
            y_line = slope * x_line
            ax2.plot(x_line, y_line, color="red", label=f"Line with slope {slope}")
            # Plot the intersection point
            ax2.scatter(
                x_intersection,
                y_intersection,
                color="red",
                label="Intersection Point",
            )

    fig.suptitle(alg + " Algorithm for " + title)

    red_patch = mpatches.Patch(color="red", label="omega points")
    black_patch = mpatches.Patch(color="black", label="critical points from M")
    orange_patch = mpatches.Patch(color="orange", label="critical points from N")
    ax1.legend(
        handles=[red_patch, black_patch, orange_patch], bbox_to_anchor=(0.8, 1.5)
    )
    plt.show()
