import modules as mod
from scipy.stats import qmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd


def example_2_13():
    """
    Corresponds to figure 3 in the paper.
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((7.0, 4.0), 0)
    c5 = mod.critical_val((0.0, 8.0), 0)
    c6 = mod.critical_val((7.0, 8.0), 0)
    c7 = mod.critical_val((0.0, 11.0), 0)
    c8 = mod.critical_val((7.0, 11.0), 0)

    d1 = mod.critical_val((0.0, 0.0), 1)
    d2 = mod.critical_val((7.0, 0.0), 1)
    d3 = mod.critical_val((0.0, 4.0), 1)
    d4 = mod.critical_val((7.0, 4.0), 1)
    d5 = mod.critical_val((0.0, 8.0), 1)
    d6 = mod.critical_val((7.0, 8.0), 1)
    d7 = mod.critical_val((0.0, 11.0), 1)
    d8 = mod.critical_val((7.0, 11.0), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]
    return CritPts


def small_socg_ex():
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((6.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 6.0), 0)

    d1 = mod.critical_val((4.0, 2.0), 1)
    d2 = mod.critical_val((4.0, 4.0), 1)
    d3 = mod.critical_val((8.0, 2.0), 1)

    d4 = mod.critical_val((1.0, 5.0), 1)
    d5 = mod.critical_val((1.0, 10.0), 1)
    d6 = mod.critical_val((2.0, 5.0), 1)

    critpts = [c1, c2, c3, d1, d2, d3, d4, d5, d6]
    return critpts


def example_2_11():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((7.0, 4.0), 0)
    c5 = mod.critical_val((0.0, 7.0), 0)
    c6 = mod.critical_val((7.0, 7.0), 0)
    c7 = mod.critical_val((0.0, 11.0), 0)
    c8 = mod.critical_val((7.0, 11.0), 0)

    d1 = mod.critical_val((0.0, 0.0), 1)
    d2 = mod.critical_val((7.0, 0.0), 1)
    d3 = mod.critical_val((0.0, 4.0), 1)
    d4 = mod.critical_val((7.0, 4.0), 1)
    d5 = mod.critical_val((0.0, 7.0), 1)
    d6 = mod.critical_val((7.0, 7.0), 1)
    d7 = mod.critical_val((0.0, 11.0), 1)
    d8 = mod.critical_val((7.0, 11.0), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]

    return CritPts


def example_1():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 8.0), 0)
    c4 = mod.critical_val((7.0, 8.0), 0)

    d1 = mod.critical_val((1.0, 1.0), 1)
    d2 = mod.critical_val((8.0, 1.0), 1)
    d3 = mod.critical_val((1.0, 9.0), 1)
    d4 = mod.critical_val((8.0, 9.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]
    return CritPts


def example_2():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((4.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((4.0, 4.0), 0)

    d1 = mod.critical_val((1.0, 0.0), 1)
    d2 = mod.critical_val((3.0, 0.0), 1)
    d3 = mod.critical_val((1.0, 4.0), 1)
    d4 = mod.critical_val((3.0, 4.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]
    return CritPts


def rectangle_example(numpts=4, display=False):
    # note: this goes in cw order, hopefully not an issue
    # parameters for rectangle shape and sampling density
    width = 8
    height = 4

    # calculate points on the boundary of the rectangle
    x1 = np.linspace(-width / 2, width / 2, num=numpts // 4 + 1)[:-1]
    y1 = np.full_like(x1, height / 2)

    x2 = np.full_like(y1, width / 2)
    y2 = np.linspace(height / 2, -height / 2, num=numpts // 4 + 1)[:-1]

    x3 = np.linspace(width / 2, -width / 2, num=numpts // 4 + 1)[:-1]
    y3 = np.full_like(x3, -height / 2)

    x4 = np.full_like(y3, -width / 2)
    y4 = np.linspace(-height / 2, height / 2, num=numpts // 4 + 1)[:-1]

    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])
    points = np.array(list(zip(x, y)))

    if display:
        # plot rectangle
        fig, ax1 = plt.subplots(figsize=(10, 4))
        ax1.set_xlim(-width / 2 - 1, width / 2 + 1)
        ax1.set_ylim(-height / 2 - 1, height / 2 + 1)
        ax1.set_aspect("equal")
        ax1.plot(x, y, "o", linewidth=2)
        plt.show()

    return points


def make_poisson(
    inputpts=rectangle_example(), llama=30, radius=0.000001, seed=0, display=False
):
    # inputpts should be column vec of x,y coords in 2D
    xMin = np.min(inputpts[:, 0])
    xMax = np.max(inputpts[:, 0])
    yMin = np.min(inputpts[:, 1])
    yMax = np.max(inputpts[:, 1])

    # rectangle dims
    xDelta = xMax - xMin
    yDelta = yMax - yMin
    areaTotal = xDelta * yDelta

    # note: llama/lambda is intensity (ie mean density)
    # of the Poisson pt process

    # this fixes a seed for reproducability (so it's not random)
    seed = 0
    g = np.random.default_rng(seed)
    numbPoints = g.poisson(llama * areaTotal)

    # Simulate a Poisson point process
    xx = xDelta * g.uniform(0, 1, numbPoints) + xMin
    yy = yDelta * g.uniform(0, 1, numbPoints) + yMin

    points = np.column_stack([xx.ravel(), yy.ravel()])
    # below is the tricksy blue noise thing
    scale = max(xDelta, yDelta)
    rng = g
    # radius = 1/(2*(math.sqrt(llama)))

    engine = qmc.PoissonDisk(d=2, radius=radius, seed=rng)
    # these are in [0,1]
    sample = engine.random(4 * llama)
    # print(radius, llama, sample.shape)
    scaledsample = sample * scale + np.array(
        [xMin + xDelta / 2 - scale / 2, yMin + yDelta / 2 - scale / 2]
    )
    # return points
    if display:
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.plot(scaledsample[:, 0], scaledsample[:, 1], "o", color="orange")
    return scaledsample


def make_rects(poisson_intensity, seed=0, dpi=150):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        inputpts=rectangle_example(),
        llama=poisson_intensity,
        radius=radius,
        seed=seed,
        display=False,
    )
    rectangle_lengths = []
    rectangle_widths = []

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    # np.random.seed(seed)
    rnd.seed(seed)
    critical_pts = []
    for x in range(len(poissonpts)):
        width = float(rnd.randint(2, 10))
        length = float(rnd.randint(2, 10))
        rectangle_lengths.append(length)
        rectangle_widths.append(width)
        # we only need the first four points for math,
        # but we need to repeat the initial point at the
        # end for plotting
        outpt_xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
        ]
        outpt_ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
        ]
        # added the init pt at the end for plotting
        xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
            poissonpts[x][0],
        ]
        ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
            poissonpts[x][1],
        ]

        color = rnd.randint(0, 1)
        if color == 0:
            ax.plot(xs, ys, "--", color="black")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="black", markersize=5)
        else:
            ax.plot(xs, ys, "--", color="orange")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="orange", markersize=5)
        for i in range(len(outpt_xs)):
            critpt = mod.critical_val((outpt_xs[i], outpt_ys[i]), color)
            critical_pts.append(critpt)

    black_patch = mpatches.Patch(color="black", label="M")
    orange_patch = mpatches.Patch(color="orange", label="N")
    ax.legend(
        handles=[black_patch, orange_patch],
        loc="upper right",
    )
    fig.dpi = dpi
    return critical_pts


def critvals_poisson(poisson_intensity, seed):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        llama=poisson_intensity, radius=radius, seed=seed, display=False
    )

    # turn poiss points into critvals
    critvals = []
    for p in poissonpts:
        c = mod.critical_val((p[0], p[1]), rnd.randint(0, 1))
        critvals.append(c)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    for c in critvals:
        if c.parent_module == 0:
            ax.plot(c.coords[0], c.coords[1], "o", color="red")
        else:
            ax.plot(c.coords[0], c.coords[1], "o", color="blue")
    return critvals


def bunny_into_critvals(bunnypoints, seed):
    rnd.seed(seed)
    critvals = []
    for row in bunnypoints:
        c = mod.critical_val((row[0], row[1]), rnd.randint(0, 1))
        critvals.append(c)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    for c in critvals:
        if c.parent_module == 0:
            ax.plot(c.coords[0], c.coords[1], "o", color="red")
        else:
            ax.plot(c.coords[0], c.coords[1], "o", color="blue")
    return critvals


def test_example():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)

    d1 = mod.critical_val((3.0, 2.0), 1)
    d2 = mod.critical_val((3.0, 6.0), 1)
    d3 = mod.critical_val((10.0, 2.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]

    return CritPts


def make_rects_balanced(poisson_intensity, seed=0, exact_num=2):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        inputpts=rectangle_example(),
        llama=poisson_intensity,
        radius=radius,
        seed=seed,
        display=False,
    )

    while len(poissonpts) < 2 * exact_num:
        print("not enought points try again")
        poisson_intensity = poisson_intensity + 1
        radius = 1 / (2 * (math.sqrt(poisson_intensity)))
        poissonpts = make_poisson(
            inputpts=rectangle_example(),
            llama=poisson_intensity,
            radius=radius,
            seed=seed,
            display=False,
        )

    if len(poissonpts) > 2 * exact_num:
        poissonpts = poissonpts[: 2 * exact_num]

    rectangle_lengths = []
    rectangle_widths = []
    colors = []
    for i in range(exact_num):
        color = 0
        colors.append(color)
    for i in range(exact_num, exact_num * 2):
        color = 1
        colors.append(color)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    # np.random.seed(seed)
    rnd.seed(seed)
    critical_pts = []
    for x in range(len(poissonpts)):
        width = float(rnd.randint(2, 10))
        length = float(rnd.randint(2, 10))
        rectangle_lengths.append(length)
        rectangle_widths.append(width)
        # we only need the first four points for math,
        # but we need to repeat the initial point at the
        # end for plotting
        outpt_xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
        ]
        outpt_ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
        ]
        # added the init pt at the end for plotting
        xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
            poissonpts[x][0],
        ]
        ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
            poissonpts[x][1],
        ]
        color = colors[x]

        if color == 0:
            ax.plot(xs, ys, "--", color="red")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="red", markersize=5)
        else:
            ax.plot(xs, ys, "--", color="blue")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="blue", markersize=5)
        for i in range(len(outpt_xs)):
            critpt = mod.critical_val((outpt_xs[i], outpt_ys[i]), color)
            critical_pts.append(critpt)

    return critical_pts
