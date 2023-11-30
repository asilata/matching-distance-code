import gudhi
from math import cos, sin, pi
import numpy as np

import modules as mod
import numpy.linalg

## for checking if in convex hull
import scipy.spatial
from scipy.optimize import linprog
from itertools import combinations

import modules as mod

import csv


###### Convex hull functions ####


def in_hull(points, x):
    """Checks if x is in the convex hull of points
    points = array of pts in R^2
    """

    ## Maybe we need to double check the linearr programing part

    n_points = len(points)
    c = np.zeros(n_points)
    A = np.r_[points.T, np.ones((1, n_points))]
    b = np.r_[x, np.ones(1)]
    lp = linprog(
        c,
        A_eq=A,
        b_eq=b,
    )
    return lp.success


def sort_bottom_and_right(u, v, w):
    """return the rightmost and bottommost points of u,v,w"""
    ## C: This seems correct to me
    rm = u
    if v[0] > rm[0]:
        rm = v
    if w[0] > rm[0]:
        rm = w

    bm = u
    if v[1] < bm[1]:
        bm = v
    if w[1] < bm[1]:
        bm = w

    return bm, rm


def sort_top_and_left(u, v, w):
    """return the leftmost and topmost points of u,v,w"""
    ## C: This seems correct to me
    lm = u
    if v[0] < lm[0]:
        lm = v
    if w[0] < lm[0]:
        lm = w

    tm = u
    if v[1] > tm[1]:
        tm = v
    if w[1] > tm[1]:
        tm = w

    return tm, lm


def check_in_quadrant_tl(x, p, q):
    """ "assume p is the bottommost pt of u,v,w
    assume q is the rightmost of u,v,w
    return True if x is in the top left quadrant
    """
    ## C: looks fine to me
    if x[0] <= q[0] and p[1] <= x[1]:
        return True
    else:
        return False


def check_x_push_up(
    x, u, v, w
):  ## Check-point-A and Check-point-B like in the overleaf
    """Check if the points x,u,v,w are admissible for:
        - x pushing up (i.e. x is below the line)
        - u,v,w pushing right
    returns True if they are an admissible quadruple
    and False if they are not admissible or would create superfluous omegapoints
    """
    ## C: looks fine to me

    p, q = sort_bottom_and_right(
        u, v, w
    )  ## p is the bottommost pt, q is the rightmost pt
    a = (q[0], p[1])

    ## First check if x is in the upper left quadrant:
    if check_in_quadrant_tl(x, p, q):
        ## Check if x is in convex hull
        if in_hull(np.array([u, v, w]), x):
            return False

        elif in_hull(np.array([u, v, w, a]), x):
            return True

        else:
            return False

    else:
        return True


def check_in_quadrant_br(x, p, q):
    """ "assume p is the topmost pt of u,v,w
    assume q is the leftmost of u,v,w
    return True if x is in the bottom right quadrant(including the boundary)
    """
    ## C: looks fine to me
    if q[0] <= x[0] and x[1] <= p[1]:
        return True
    else:
        return False


def check_x_push_right(x, u, v, w):
    """Check if the points x,u,v,w are admissible for:
        - x pushing right
        - u,v,w pushing up
    returns True if they are an admissible quadruple
    and False if they are not admissible or would create superfluous omegapoints
    """
    ## C: looks fine to me
    p, q = sort_top_and_left(u, v, w)
    a = (q[0], p[1])

    ## First check if x is in the upper left quadrant:
    if check_in_quadrant_br(x, p, q):
        ## Check if x is in convex hull
        if in_hull(np.array([u, v, w]), x):
            return False

        elif in_hull(np.array([u, v, w, a]), x):
            return True
        else:
            return False
    else:
        return True


###


def check_3distinct(C):
    # this function checks that 3 out of 4 things in a set are distinct
    assert len(C) == 4, "C is not of length 4 "
    if (len(C) - len(set(C))) > 1:
        return False
    else:
        return True


def check_4distinct(C):
    # this function checks that all things in a set (of 4) are distinct
    assert len(C) == 4, "C is not of length 4 "
    if (len(C) - len(set(C))) > 0:
        # print("beepbeep", C)
        return False
    else:
        return True


def check_c_distinct(c, C):
    """this function checks that c, assumed to be in C, is not repeated in C"""
    C_new = C.copy()
    C_new.remove(c)
    val = True
    for (
        d
    ) in (
        C_new
    ):  ## can we do without a for loop here? (for further optimization if we ever want to do that )
        if c.coords == d.coords:
            val = False

    return val


####
def check_omega_x_below(u, v, w, x, omega):
    """Here we assume we are in the case where x pushes up and u,v,w push right, i.e. x is below a line separating u,v,w from x
    We check if the omegapoint is valid
    """
    ## check below vs x push up
    """ Function to be implemented later to check if the computed omegapoint is valid"""
    if omega[1] <= x.coords[1]:  ### We reject omega if it is below x , Double check
        return False
    # elif check_x_push_up(u.coords,v.coords, w.coords, omega): ## UUuugh shouldn't this be:  check_x_push_up(omega, u.coords,v.coords, w.coords): ??
    elif check_x_push_up(omega, u.coords, v.coords, w.coords):
        return True
    else:
        return False


def check_omega_x_above(u, v, w, x, omega):
    """Function to be implemented later to check if the computed omegapoint is valid"""
    if (
        omega[0] <= x.coords[0]
    ):  ### We reject omega if it is to the left of x, DOUBLE CHECK
        return False
    # elif check_x_push_right(u.coords, v.coords, w.coords,omega):## UUuugh shouldn't this be:  check_x_push_right(omega, u.coords,v.coords, w.coords): ??
    elif check_x_push_right(omega, u.coords, v.coords, w.coords):
        return True
    else:
        return False


#### 2 vs 2 paired version  ####


def check_pts_2v2_paired(
    x, w, u, v
):  ### corresponds the the function CheckPts2 in the paper
    """Implement later"""
    if x.coords[0] == w.coords[0]:
        m1 = np.inf
    else:
        m1 = (w.coords[1] - x.coords[1]) / (
            w.coords[0] - x.coords[0]
        )  ## slope of the line through x and w

    if u.coords[0] == v.coords[0]:
        m2 = np.inf
    else:
        m2 = (u.coords[1] - v.coords[1]) / (
            u.coords[0] - v.coords[0]
        )  ## slope of the line through u and v

    # R has a triangle cut out of it

    # sort the topmost of x and w and the leftmost of x and w
    lm = x.coords  ## TODO check if this is correct
    if w.coords[0] < lm[0]:
        lm = w.coords
    tm = x.coords
    if w.coords[1] > tm[1]:
        tm = w.coords

    corner_R = (lm[0], tm[1])  ## corner of the quandrant R

    # sort the bottommost of u and v and the rightmost of u and v
    rm = u.coords
    if v.coords[0] > rm[0]:  ## TODO check if this is correct
        rm = v.coords
    bm = u.coords
    if v.coords[1] < bm[1]:
        bm = v.coords
    corner_Q = (rm[0], bm[1])  ## corner of the quandrant Q

    if check_in_quadrant_br(u.coords, tm, lm) or check_in_quadrant_br(v.coords, tm, lm):
        # check if u or v are in the quandrant containing R
        if m1 > 0:
            if in_hull(np.array([x.coords, w.coords, corner_R]), u.coords) or in_hull(
                np.array([x.coords, w.coords, corner_R]), v.coords
            ):
                # check if u or v are in the triangle cut out of R
                return True
            else:
                return False

        else:  # R is a quandrant
            return False

    elif check_in_quadrant_tl(x.coords, bm, rm) or check_in_quadrant_tl(
        w.coords, bm, rm
    ):
        # check if x or w are in the quandrant containing Q

        if m2 > 0:
            if in_hull(np.array([u.coords, v.coords, corner_Q]), x.coords) or in_hull(
                np.array([u.coords, v.coords, corner_Q]), w.coords
            ):
                # check if x or w are in the triangle cut out of Q
                return True
            else:
                return False

        else:
            return False
    else:
        return True

        # check if u or v are in the quandrant containing R
        # if yes,check if u or v is in the triangle cut out of R --> return True
        # if not in the tirangle but in quadrant return False
        # if not in the quandrant return False

        # side note: we can check if u or v are in the triangle cut out of R by checking if they are in the convex hull of the other two points and the corner of the quandrant

    # else: #R is a quandrant
    # check if u or v are in the quandrant R
    # if yes return False
    # if no return True

    # if m2 >0: #Q has a triangle cut out of it
    # check if x or w are in the quandrant containing Q
    # if yes, check if x or w is in the triangle cut out of Q --> return True
    # if not in the tirangle but in quadrant return False
    # if not in the quandrant return False

    # else: #Q is a quandrant
    # check if x or w are in the quandrant Q
    # if yes return False
    # if no return True


def algo_2v2_paired(CritPts):
    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_4distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []  ## will contain just the valid omega points that were computed
    info_list = (
        []
    )  ## contains the omega points and the additional info from which critical pts it came from
    for c, d in combinations(CritPts, 2):
        x = c
        w = d
        if w.coords[0] < x.coords[0]:
            temp_x = x
            x = w
            w = temp_x
        elif w.coords[0] == x.coords[0]:
            continue

        CritPts_no_x_w = CritPts.copy()
        CritPts_no_x_w.remove(w)  # .remove(x) ## can we do this in one line?
        CritPts_no_x_w.remove(x)
        u = CritPts_no_x_w[0]
        v = CritPts_no_x_w[1]
        if u.coords[1] < v.coords[1]:
            temp_u = u
            u = v
            v = temp_u
        elif u.coords[1] == v.coords[1]:
            continue

        if x.parent_module == w.parent_module:
            eta = 2
        else:
            eta = 1
        if u.parent_module == v.parent_module:
            delta = 2
        else:
            delta = 1

        if check_pts_2v2_paired(x, w, u, v):
            omega = (
                0,
                delta * (w.coords[0] - x.coords[0]),
                eta * (u.coords[1] - v.coords[1]),
            )  ## How tf are we going to deal with projective coordinates here?
            if u.coords[1] == v.coords[1]:
                m = np.inf
            else:
                m = (eta * (u.coords[1] - v.coords[1])) / (
                    delta * (w.coords[0] - x.coords[0])
                )

            if max(x.coords[1] - m * x.coords[0], w.coords[1] - m * w.coords[0]) < min(
                u.coords[1] - m * u.coords[0], v.coords[1] - m * v.coords[0]
            ):
                Omega_pts.append(omega)
                info_list.append(
                    [omega, x.coords, u.coords, v.coords, w.coords, eta, delta, m]
                )

    return Omega_pts, info_list


def output_alg_2_2_paired(CritPts, name):
    Pts = []
    Total_info_list = [["omega_pts", "x", "u", "v", "w", "eta", "delta", "m"]]
    set_of_points = set({})
    length = len(CritPts)

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_4distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, info_list = algo_2v2_paired(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]]
                        )
                        Pts += pts
                        # a first attempt to get rid of duplicates
                        # this should be moved to the omega file
                        for p in range(len(pts)):
                            if pts[p] not in set_of_points:
                                set_of_points.add(pts[p])
                                Total_info_list += [info_list[p]]

    print("**********")
    num_duplicates = len(Pts)
    print("Computed {} points (with duplicates)".format(num_duplicates))

    # # checking a weird number discrep; uncomment later
    Pts = list(set(Pts))
    print("Without duplicates {}".format(len(Pts)))

    # Dict_pts.sort()
    # new_pts= list(k for k,_ in itertools.groupby(k))
    is_inf = []
    for t in range(len(Total_info_list)):
        is_inf.append(Total_info_list[t][-1])
    print(is_inf)
    # w+ option overwrites file each time (good thing)
    with open("../output/" + name + "_2v2_paired.csv", "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(Total_info_list)

    return Pts, num_duplicates, len(Pts), is_inf


#####  3 vs 1 new version
# corresponds to Algorithm 3 in the paper as of July 13, 2023


def output_alg_3_1(CritPts, name):
    Pts = []
    Dict_pts = [["omega_pts", "x", "u", "v", "w", "eta", "delta"]]
    set_of_points = set({})
    length = len(CritPts)

    all_critptscoords = []
    for x in CritPts:
        all_critptscoords.append(x.coords)

    closure = closure_lub(CritPts)
    for key in closure.keys():
        all_critptscoords += closure[
            key
        ]  ## add the closure under lub to the list of all critical points

    all_critptscoords = list(set(all_critptscoords))  ## remove duplicates

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_3distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, dict_pts = algo_3vs1(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]],
                            all_critptscoords,
                        )
                        Pts += pts
                        # a first attempt to get rid of duplicates
                        # this should be moved to the omega file
                        for p in range(len(pts)):
                            if pts[p] not in set_of_points:
                                set_of_points.add(pts[p])
                                Dict_pts += [dict_pts[p]]

    print("**********")
    num_duplicates = len(Pts)
    print("Computed {} points (with duplicates)".format(num_duplicates))

    # # checking a weird number discrep; uncomment later
    Pts = list(set(Pts))
    print("Without duplicates {}".format(len(Pts)))

    # Dict_pts.sort()
    # new_pts= list(k for k,_ in itertools.groupby(k))
    # w+ option overwrites file each time (good thing)
    with open("../output/" + name + "_3v1.csv", "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(Dict_pts)

    return Pts, num_duplicates, len(Pts)


# def almost_equal(x, y, tol=1e-3):
#    return abs(x[0] - y[0]) < tol and abs(x[1] - y[1]) < tol

# def check_in_list(x, list_pts):
#    for pt in list_pts:
#        if almost_equal(x, pt):
#           return True
#    else:
#       return False


def algo_3vs1(CritPts, all_CritPts):
    """discards the omega points that are not valid"""
    ## input: 4 critical points from C_M and C_N

    # don't we already do this in the if statement that contains this function?
    ## Check that we have at least three distinct points, otherwise stop
    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_3distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []
    dict_omega_pts = []

    for c in CritPts:
        # Trying to find x (of the points x,w,u,v in the paper)
        if check_c_distinct(
            c, CritPts
        ):  ## want a critical point x that is distinct from u,v,w
            x = c
        else:
            continue  ### Skips the rest of the loop if c appears multiple times in C

        CritPts_no_x = CritPts.copy()
        CritPts_no_x.remove(x)

        for d in CritPts_no_x:
            w = d
            CritPts_no_x_no_w = CritPts_no_x.copy()
            CritPts_no_x_no_w.remove(
                w
            )  ## lol (with a french accent), list with two elements only

            if CritPts_no_x_no_w[0].coords == CritPts_no_x_no_w[1].coords:
                continue

            u = CritPts_no_x_no_w[0]
            v = CritPts_no_x_no_w[1]

            ## Assign the value of the denominator eta and delta according to the parent module
            ## of the pairs (x,w) and (u,v)
            if x.parent_module == w.parent_module:
                eta = 2
            else:
                eta = 1

            if u.parent_module == v.parent_module:
                delta = 2
            else:
                delta = 1

            ## Is indentation correct? yes same as paper
            if check_x_push_up(x.coords, u.coords, v.coords, w.coords):
                # adding this to include claudia's comment about matching having null cost
                if u.coords[1] == v.coords[1]:
                    continue

                if (
                    u.coords[1] < v.coords[1]
                ):  ## at some point there was confusion about <= or <; changed to < on 13 july to match current paper. maybe shouldn't have?
                    temp_u = u
                    u = v
                    v = temp_u
                if (
                    w.coords[0] >= x.coords[0] and w.coords[1] >= x.coords[1]
                ):  ## should this be strict inequality? , also check the coordinates 0 and 1
                    omega = (
                        x.coords[0],
                        (eta / delta) * (v.coords[1] - u.coords[1]) + w.coords[1],
                    )

                elif w.coords[0] <= x.coords[0] and w.coords[1] <= x.coords[1]:
                    omega = (
                        x.coords[0],
                        (eta / delta) * (u.coords[1] - v.coords[1]) + w.coords[1],
                    )

                else:
                    omega = (
                        x.coords[0],
                        (eta / delta) * (u.coords[1] - v.coords[1]) + w.coords[1],
                    )
                    omega1 = (
                        x.coords[0],
                        (eta / delta) * (v.coords[1] - u.coords[1]) + w.coords[1],
                    )

                    if (
                        check_omega_x_below(u, v, w, x, omega1)
                        and omega1 not in all_CritPts
                    ):
                        Omega_pts.append(omega1)  ## append
                        ##  add omega pts to dictionary
                        dict_omega_pts.append(
                            [omega1, x.coords, u.coords, v.coords, w.coords, eta, delta]
                        )

                    # dict_omega_pts.append({ "omega_pts": omega1 , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })

                if check_omega_x_below(u, v, w, x, omega) and omega not in all_CritPts:
                    Omega_pts.append(omega)  ## in any case we append omegaa
                    # dict_omega_pts.append({ "omega_pts": omega , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                    dict_omega_pts.append(
                        [omega, x.coords, u.coords, v.coords, w.coords, eta, delta]
                    )

            ### Is indentation correct? yes, same as above
            if check_x_push_right(x.coords, u.coords, v.coords, w.coords):
                # adding because of claudia's null cost comment
                if u.coords[0] == v.coords[0]:
                    continue

                if (
                    u.coords[0] < v.coords[0]
                ):  ## confusion about <= or <, but updated 13 july to match paper
                    temp_u = u
                    u = v
                    v = temp_u
                if (
                    w.coords[0] >= x.coords[0] and w.coords[1] >= x.coords[1]
                ):  ## check < vs <= and coordinates 0,1
                    omega = (
                        (eta / delta) * (v.coords[0] - u.coords[0]) + w.coords[0],
                        x.coords[1],
                    )

                elif w.coords[0] <= x.coords[0] and w.coords[1] <= x.coords[1]:
                    omega = (
                        (eta / delta) * (u.coords[0] - v.coords[0]) + w.coords[0],
                        x.coords[1],
                    )

                else:
                    omega = (
                        (eta / delta) * (v.coords[0] - u.coords[0]) + w.coords[0],
                        x.coords[1],
                    )
                    omega1 = (
                        (eta / delta) * (u.coords[0] - v.coords[0]) + w.coords[0],
                        x.coords[1],
                    )

                    if (
                        check_omega_x_above(u, v, w, x, omega1)
                        and omega1 not in all_CritPts
                    ):  # not check_in_list(omega1, critptscoords):
                        Omega_pts.append(omega1)
                        ## dict for debuging
                        # dict_omega_pts.append({ "omega_pts": omega1 , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                        dict_omega_pts.append(
                            [omega1, x.coords, u.coords, v.coords, w.coords, eta, delta]
                        )

                if (
                    check_omega_x_above(u, v, w, x, omega) and omega not in all_CritPts
                ):  # and not check_in_list(omega, critptscoords):
                    Omega_pts.append(omega)
                    # dict_omega_pts.append({ "omega_pts": omega , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                    dict_omega_pts.append(
                        [omega, x.coords, u.coords, v.coords, w.coords, eta, delta]
                    )

    """with open('test.csv', 'a', newline='') as file:  #### find a way to write everything in file
        writer = csv.DictWriter(file, fieldnames = fields,dialect='excel')
        writer.writeheader() 
        writer.writerows(dict_omega_pts)"""
    # dict_omega_pts = list(set(dict_omega_pts))

    return Omega_pts, dict_omega_pts


#### Check Omega points 2 vs 2 unpaired


def check_omega_3(omega, u, v, w, x):
    Q = {}  ## dictionary of quadrants
    m = {}  ## dictionary of slopes

    for p in [u, v, w, x]:
        if p[0] > omega[0] and p[1] > omega[1]:
            Q[p] = 1
            m[p] = (p[1] - omega[1]) / (p[0] - omega[0])
        elif p[0] <= omega[0] and p[1] >= omega[1]:
            Q[p] = 2
        elif p[0] < omega[0] and p[1] < omega[1]:
            Q[p] = 3
            m[p] = (p[1] - omega[1]) / (p[0] - omega[0])
        else:
            Q[p] = 4
    if omega in [u, v, w, x]:
        return False
    elif Q[x] == 2 or Q[v] == 2 or Q[u] == 4 or Q[w] == 4:
        return False
    elif Q[x] == 4 and Q[v] == 4 and Q[u] == 2 and Q[w] == 2:
        return True
    else:
        P = []
        S = []

        for p in [v, x]:
            if (
                Q[p] == 4
            ):  ### THIS is ugly maybe we can do this in a shorter way by checking if Q[p] in [1,3]
                continue
            else:
                P.append(p)

        for p in [u, w]:  ## same here
            if Q[p] == 2:
                continue
            else:
                S.append(p)

        for p in P:
            r_p = 1
            for q in [val for val in P if val != p]:
                if Q[p] == 1:
                    if Q[q] == 3:  ## can this be on the line above?
                        if m[p] >= m[q]:
                            r_p = 0
                    elif Q[q] == 1:
                        if m[p] < m[q]:
                            r_p = 0
                elif Q[p] == 3:
                    if Q[q] == 1:
                        if m[p] <= m[q]:
                            r_p = 0
                    elif Q[q] == 3:
                        if m[p] > m[q]:
                            r_p = 0

            if r_p > 0:
                for q in S:
                    if Q[p] == 1:
                        if Q[q] == 3:
                            if m[p] < m[q]:
                                r_p = 0
                        elif Q[q] == 1:
                            if m[p] >= m[q]:
                                r_p = 0
                    elif Q[p] == 3:
                        if Q[q] == 1:
                            if m[p] > m[q]:
                                r_p = 0
                        elif Q[q] == 3:
                            if m[p] <= m[q]:
                                r_p = 0
                ###### THis is as far as we got checking the pseudo code, continue from here

            if r_p == 1:  ## for some p
                return True

        for s in S:
            r_s = 1
            for t in [val for val in S if val != s]:
                if Q[s] == 1:
                    if Q[t] == 3:
                        if m[s] <= m[t]:
                            r_s = 0  ## check line 94 in pseudo code
                    elif Q[t] == 1:
                        if m[s] > m[t]:
                            r_s = 0
                elif Q[s] == 3:
                    if Q[t] == 1:
                        if m[s] >= m[t]:  ## Check line 103
                            r_s = 0
                    elif Q[t] == 3:
                        if m[s] < m[t]:
                            r_s = 0

            if r_s > 0:
                for t in S:
                    if Q[s] == 1:
                        if Q[t] == 3:
                            if m[s] > m[t]:
                                r_s = 0
                        elif Q[t] == 1:
                            if m[s] <= m[t]:
                                r_s = 0
                    elif Q[s] == 3:
                        if Q[t] == 1:
                            if m[s] < m[t]:
                                r_s = 0
                        elif Q[t] == 3:
                            if m[s] >= m[t]:
                                r_s = 0

        if r_s == 1:  ## check indentation
            return True

        return False


# IN PROGRESS
def algo_2v2_unpaired(CritPts, all_CritPts):
    # x paired with w
    # u paired with v
    # x,v on one side of line, u,w on the other side

    critptscoords = []
    for x in CritPts:
        critptscoords.append(x.coords)

    assert check_3distinct(
        critptscoords
    ), "There is more than one repeated point in the list"

    Omega_pts = []  ## will contain just the valid omega points that were computed
    info_list = (
        []
    )  ## contains the omega points and the additional info from which critical pts it came from
    for c, d in combinations(CritPts, 2):
        x = c
        v = d
        CritPts_no_x_v = CritPts.copy()
        CritPts_no_x_v.remove(v)
        CritPts_no_x_v.remove(x)
        for f in CritPts_no_x_v:
            if f == x:
                continue
            else:
                w = f
        CritPtsno_x_v_w = CritPts_no_x_v.copy()
        CritPtsno_x_v_w.remove(w)
        for g in CritPtsno_x_v_w:
            if g == v:
                continue
            else:
                u = g
            if x.parent_module == w.parent_module:
                eta = 2
            else:
                eta = 1
            if u.parent_module == v.parent_module:
                delta = 2
            else:
                delta = 1

        if check_pts_2v2_paired(x, v, w, u):
            if (
                (lub(u, v) == u.coords and lub(x, w) == w.coords)
                or (lub(u, v) == v.coords and lub(x, w) == x.coords)
                or lub(u, v) not in [u.coords, v.coords]
                or lub(x, w) not in [x.coords, w.coords]
            ):
                # this is the new thing that robyn just added
                if (
                    (delta == eta)
                    and (v.coords[0] != x.coords[0])
                    and (u.coords[1] != w.coords[1])
                ):
                    omega = (
                        v.coords[0] - x.coords[0],
                        u.coords[1] - w.coords[1],
                    )  ## line 29 pseudo code . check this!!!
                    m = (u.coords[1] - w.coords[1]) / (v.coords[0] - x.coords[0])
                    # added here (on tuesday) that m > 0
                    if (
                        max(
                            x.coords[1] - m * x.coords[0], v.coords[1] - m * v.coords[0]
                        )
                        < min(
                            u.coords[1] - m * u.coords[0], w.coords[1] - m * w.coords[0]
                        )
                        and m > 0
                    ):
                        Omega_pts.append(omega)
                        ## append the slope
                        info_list.append(
                            [
                                omega,
                                x.coords,
                                u.coords,
                                v.coords,
                                w.coords,
                                eta,
                                delta,
                                m,
                            ]
                        )

                elif delta != eta:
                    omega = (
                        (eta * v.coords[0] - delta * x.coords[0]) / (eta - delta),
                        (eta * u.coords[1] - delta * w.coords[1]) / (eta - delta),
                    )
                    if (
                        check_omega_3(omega, u.coords, v.coords, w.coords, x.coords)
                        and omega not in all_CritPts
                    ):
                        Omega_pts.append(omega)
                        info_list.append(
                            [
                                omega,
                                x.coords,
                                u.coords,
                                v.coords,
                                w.coords,
                                eta,
                                delta,
                                None,
                            ]
                        )

        if (
            (lub(u, v) == u.coords and lub(x, w) == x.coords)
            or (lub(u, v) == v.coords and lub(x, w) == w.coords)
            or lub(u, v) not in [u.coords, v.coords]
            or lub(x, w) not in [x.coords, w.coords]
        ):
            omega = (
                (eta * v.coords[0] + delta * x.coords[0]) / (eta + delta),
                (eta * u.coords[1] + delta * w.coords[1]) / (eta + delta),
            )

            if (
                check_omega_3(omega, u.coords, v.coords, w.coords, x.coords)
                and omega not in all_CritPts
            ):  ## corresponds to CheckOmega2 in the pseudo code
                Omega_pts.append(omega)
                info_list.append(
                    [omega, x.coords, u.coords, v.coords, w.coords, eta, delta, None]
                )

    return Omega_pts, info_list


### least upper bound function


def lub(point1, point2):
    """
    Finds the least upper bound of two points.

    Parameters:
    - point1: Tuple representing the first point.
    - point2: Tuple representing the second point.

    Returns:
    Tuple representing the least upper bound of the two points.
    """
    return (
        max(point1.coords[0], point2.coords[0]),
        max(point1.coords[1], point2.coords[1]),
    )


def output_alg_2_2_unpaired(CritPts, name):
    Pts = []
    Dict_pts = [["omega_pts", "x", "u", "v", "w", "eta", "delta", "m"]]
    set_of_points = set({})
    length = len(CritPts)

    all_critptscoords = []
    for x in CritPts:
        all_critptscoords.append(x.coords)

    closure = closure_lub(CritPts)
    for key in closure.keys():
        all_critptscoords += closure[
            key
        ]  ## add the closure under lub to the list of all critical points

    all_critptscoords = list(set(all_critptscoords))  ## remove duplicates

    for a in range(length):
        for b in range(a + 1, length):
            for c in range(b + 1, length):
                for d in range(c, length):
                    if check_3distinct(
                        [
                            CritPts[a].coords,
                            CritPts[b].coords,
                            CritPts[c].coords,
                            CritPts[d].coords,
                        ]
                    ):
                        pts, dict_pts = algo_2v2_unpaired(
                            [CritPts[a], CritPts[b], CritPts[c], CritPts[d]],
                            all_critptscoords,
                        )
                        Pts += pts
                        # a first attempt to get rid of duplicates
                        # this should be moved to the omega file
                        for p in range(len(pts)):
                            if pts[p] not in set_of_points:
                                set_of_points.add(pts[p])
                                Dict_pts += [dict_pts[p]]

    print("**********")
    num_duplicates = len(Pts)
    print("Computed {} points (with duplicates)".format(num_duplicates))

    # # checking a weird number discrep; uncomment later
    Pts = list(set(Pts))
    print("Without duplicates {}".format(len(Pts)))

    # Dict_pts.sort()
    # new_pts= list(k for k,_ in itertools.groupby(k))
    is_inf = []
    for t in range(len(Dict_pts)):
        is_inf.append(Dict_pts[t][-1])
    print(is_inf)

    # w+ option overwrites file each time (good thing)
    with open("../output/" + name + "_2v2_unpaired.csv", "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(Dict_pts)

    return Pts, num_duplicates, len(Pts), is_inf


def closure_lub(CritPts):
    """
    Computes the closure of the least upper bound of a set of points.

    Parameters:
    - CritPts: List of critical points.

    Returns:
    List of critical points.
    """
    closure = {}
    for point1 in CritPts:
        for point2 in CritPts:
            if point1 != point2 and point1.parent_module == point2.parent_module:
                if point1.parent_module not in closure.keys():
                    closure[point1.parent_module] = [lub(point1, point2)]
                else:
                    closure[point1.parent_module].append(lub(point1, point2))

    return closure
