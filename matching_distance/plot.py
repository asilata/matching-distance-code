import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from matplotlib import rc

from . import settings

rc("font", **{"family": "serif", "serif": ["Times"]})
rc("text", usetex=settings.use_tex)


def plot_both_c_o(crits_no_lub, omegapts, title, dpi, alg, out_path=None):
    """Plot proper candidate switch points (red) with the critical values of M (black) and N (orange)."""
    fig, ax = plt.subplots()
    fig.set_dpi(dpi)
    fig.set_size_inches(6, 5)
    ax.set_aspect("equal")
    for o in omegapts:
        ax.plot(o[0], o[1], "o", color="red", label="red", alpha=0.8, markersize=4)

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

    red_patch = mpatches.Patch(color="red", label="candidate switch points")
    black_patch = mpatches.Patch(color="black", label="critical values from M")
    orange_patch = mpatches.Patch(color="orange", label="critical values from N")

    plt.legend(handles=[red_patch, black_patch, orange_patch], loc="best")
    if out_path:
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()


def plot_c_o_with_inf(crits_no_lub, orderedomegas, is_inf, title, dpi, alg, out_path=None):
    """Plot proper candidates (left) and points at infinity as directions on the unit quarter circle (right).

    orderedomegas and is_inf are parallel lists that start with a header entry; is_inf
    holds the slope of a point at infinity and None for a proper point.
    """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    fig.set_dpi(dpi)
    fig.set_size_inches(6, 5)
    ax1.set_aspect("equal")
    ax2.set_aspect("equal")

    # quarter circle
    theta = np.linspace(0, np.pi / 2, 100)
    radius = 1
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax2.plot(x, y, "--", color="black")

    for o, slope in zip(orderedomegas[1:], is_inf[1:]):  # skip the header entries
        if slope is None:
            ax1.plot(o[0], o[1], "o", color="red", label="red", alpha=1.0, markersize=4)
        else:
            # where the direction of slope meets the quarter circle
            x_intersection = radius / np.sqrt(1 + slope**2)
            y_intersection = slope * x_intersection

            # the segment from the origin to the quarter circle
            x_line = np.linspace(0, x_intersection, 100)
            y_line = slope * x_line
            ax2.plot(x_line, y_line, color="red", label=f"Line with slope {slope}")
            ax2.scatter(
                x_intersection,
                y_intersection,
                color="red",
                label="Intersection Point",
            )
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

    red_patch = mpatches.Patch(color="red", label="candidate switch points or slopes")
    black_patch = mpatches.Patch(color="black", label="critical values from M")
    orange_patch = mpatches.Patch(color="orange", label="critical values from N")
    ax1.legend(
        handles=[red_patch, black_patch, orange_patch],
        bbox_to_anchor=(0.64, 1.31),
        loc="upper left",
    )
    if out_path:
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
