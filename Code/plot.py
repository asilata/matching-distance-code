import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from matplotlib import rc

# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=True)


def plot_both_c_o(crits_no_lub, omegapts, title, dpi, alg):
    sanitycount = 0
    fig, ax = plt.subplots()
    fig.set_dpi(dpi)
    fig.set_size_inches(6, 5)
    ax.set_aspect("equal")
    # ax.set_xlim(-5, 35)
    # ax.set_ylim(-5, 20)
    for o in omegapts:
        # apparently sometimes at the end of omegapts we spit out the number of points too,
        # so it can be an int. We might want to fix.
        ax.plot(o[0], o[1], "o", color="red", label="red", alpha=0.8, markersize=4)
        sanitycount += 1
    print("for sanity, num omegas:", sanitycount)

    for c in crits_no_lub:
        if c[1] == 0:
            ax.plot(
                c[0][0],
                c[0][1],
                "o",
                color="black",
                label="black",
                markersize=4,
            )
        else:
            ax.plot(
                c[0][0],
                c[0][1],
                "o",
                color="black",
                markersize=4,
            )

            ax.plot(
                c[0][0],
                c[0][1],
                "o",
                color="orange",
                label="orange",
                markersize=3,
            )

    plt.title(alg + " Algorithm for " + title)

    red_patch = mpatches.Patch(color="red", label="switch points")
    black_patch = mpatches.Patch(color="black", label="critical values from M")
    orange_patch = mpatches.Patch(color="orange", label="critical values from N")

    plt.legend(handles=[red_patch, black_patch, orange_patch], loc="best")
    plt.show()


def plot_c_o_with_inf(crits_no_lub, orderedomegas, is_inf, title, dpi, alg):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    fig.set_dpi(dpi)
    fig.set_size_inches(6, 5)
    fig.tight_layout
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    # ax1.set_xlim(-5, 20)
    # ax1.set_ylim(-5, 10)
    sanitycount = -1  # because the first one is a string

    ## draw quarter circle
    theta = np.linspace(0, np.pi / 2, 100)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax2.plot(x, y, "--", color="black")

    for o in orderedomegas:
        sanitycount += 1
        # the first entry is a string
        if orderedomegas.index(o) == 0:
            continue
        # apparently sometimes at the end of omegapts we spit out the number of points too,
        # so it can be an int. We might want to fix.
        if is_inf[orderedomegas.index(o)] == None:
            ax1.plot(o[0], o[1], "o", color="red", label="red", alpha=1.0, markersize=4)
        else:
            # print("infty point:", is_inf[orderedomegas.index(o)])
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
    print("for sanity, num omegas: ", sanitycount)
    for c in crits_no_lub:
        if c[1] == 0:
            ax1.plot(
                c[0][0],
                c[0][1],
                "o",
                color="black",
                label="black",
                markersize=4,
            )
        else:
            ax1.plot(
                c[0][0],
                c[0][1],
                "o",
                color="black",
                markersize=4,
            )

            ax1.plot(
                c[0][0],
                c[0][1],
                "o",
                color="orange",
                label="orange",
                markersize=3,
            )

    fig.suptitle(alg + " Algorithm for " + title)

    red_patch = mpatches.Patch(color="red", label="switch points or slopes")
    black_patch = mpatches.Patch(color="black", label="critical values from M")
    orange_patch = mpatches.Patch(color="orange", label="critical values from N")
    ax1.legend(
        handles=[red_patch, black_patch, orange_patch],
        bbox_to_anchor=(0.64, 1.31),
        loc="upper left",
    )
    plt.show()
