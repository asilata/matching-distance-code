import modules as mod
from scipy.stats import qmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd
import modules as mod
import examples as ex
import plot as ourplot
import csv
import bunny_smaller
import omega_pts as omega
from numpy import linalg as LA

def make_1dim_MN_example(tl_m, tr_m, bl_m, br_m, tl_n, tr_n, bl_n, br_n):

    #######################
    a1 = ((bl_m[0], bl_m[1]), 0)
    a2 = ((br_m[0], br_m[1]), 0)
    a3 = ((tl_m[0], tl_m[1]), 0)

    b1 = ((bl_n[0], bl_n[1]), 1)
    b2 = ((tl_n[0], tl_n[1]), 1)
    b3 = ((br_n[0], br_n[1]), 1)

    ############## make them into crit vals 
    c1 = mod.critical_val((bl_m[0], bl_m[1]), 0)
    c2 = mod.critical_val((br_m[0], br_m[1]), 0)
    c3 = mod.critical_val((tl_m[0], tl_m[1]), 0)

    d1 = mod.critical_val((bl_n[0], bl_n[1]), 1)
    d2 = mod.critical_val((tl_n[0], tl_n[1]), 1)
    d3 = mod.critical_val((br_n[0], br_n[1]), 1)

    crits_no_lub = [a1, a2, a3, b1, b2, b3]
    critpts = [c1, c2, c3, d1, d2, d3]

   #(self, top_left,top_right, bottom_left, 
    # bottom_right, dim = 1, parent = 1):

    m1 = mod.Rectangle((tl_m[0], tl_m[1]), (tr_m[0], tr_m[1]), (bl_m[0], bl_m[1]), (br_m[0], br_m[1]), 1, 0)
    n1 = mod.Rectangle((tl_n[0], tl_n[1]), (tr_n[0], tr_n[1]), (bl_n[0], bl_n[1]), (br_n[0], br_n[1]), 1, 1)   

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n1])

    # put the modules into the correct format (eg like in examples.py)
    critval_coords = [] ## forgets the parent modules 
    for i in range(len(critpts)):
        critval_coords.append(critpts[i].coords)

    return critpts, crits_no_lub, M, N, critval_coords

def compute_switch_points(critpts, crits_no_lub, makegraphyesno = False, title = 'title'):

    ############################
    ### originally from socg_examples.ipynb
    if makegraphyesno:
        title = "M and N"
        dpi = 300

        ############ make the example
        fig, ax0 = plt.subplots()
        fig.set_dpi(dpi)
        fig.set_size_inches(6, 5)
        # fig.tight_layout

        fig.suptitle("Input rectangle modules M and N")
        for i in [0, 3, 6]:
            p1, p2, p3 = crits_no_lub[0 + i][0], crits_no_lub[1 + i][0], crits_no_lub[2 + i][0]
            p4 = np.array(p2) + np.array(p3) - np.array(p1)
            x = [p1[0], p2[0], p4[0], p3[0], p1[0]]
            y = [p1[1], p2[1], p4[1], p3[1], p1[1]]
            ax0.plot(x, y, "k--")

        for c in crits_no_lub:
            if c[1] == 0:
                ax0.plot(
                    c[0][0],
                    c[0][1],
                    "o",
                    color="black",
                    label="black",
                    markersize=4,
                )
            else:
                ax0.plot(
                    c[0][0],
                    c[0][1],
                    "o",
                    color="black",
                    markersize=4,
                )
                ax0.plot(
                    c[0][0],
                    c[0][1],
                    "o",
                    color="orange",
                    label="orange",
                    markersize=3,
                )


        black_patch = mpatches.Patch(color="black", label="critical values from M")
        orange_patch = mpatches.Patch(color="orange", label="critical values from N")
        ax0.legend(
            handles=[black_patch, orange_patch],
            loc="upper right",
        )
        plt.show()


    ############# do computations
    # algo 3v1 = Algorithm 3 in SoCG overleaf
    # never has points at infinity, so we can plot all points
    print("3v1")
    omegapts_3v1, _, _ = omega.output_alg_3_1(critpts, "socg/" + title)
    if makegraphyesno:
        ourplot.plot_both_c_o(crits_no_lub, omegapts_3v1, title, dpi, "3v1")

    # algo 2v2 paired = Algorithm 5 in SoCG overleaf
    print("2v2paired")
    omegapts_2v2_p, _, _, is_inf_2v2p, orderedomegas2v2p = omega.output_alg_2_2_paired(
        critpts, "socg/" + title
    )

    if makegraphyesno:
        ourplot.plot_c_o_with_inf(crits_no_lub, orderedomegas2v2p, is_inf_2v2p, title, dpi, "2v2 Paired")

    # algo 2v2 unpaired = Algorithm 7 in SoCG overleaf
    print("2v2unp")
    omegapts_2v2_unp, _, _, is_inf_2v2unp_orig , orderedomegas_2v2unp = omega.output_alg_2_2_unpaired(
        critpts, "socg/" + title
    )
    if makegraphyesno:
        ourplot.plot_c_o_with_inf(
            crits_no_lub, orderedomegas_2v2unp, is_inf_2v2unp_orig, title, dpi, "2v2 Unpaired"
        )
    return critpts, crits_no_lub, is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp

def combine_omegas(is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp):

    omega_points_collection = []
    omega_slopes_collection = []

    is_inf_2v2unp = is_inf_2v2unp_orig  

    for n in range(len(omegapts_3v1)):
        omega_points_collection.append(omegapts_3v1[n])

    omega_points_collection += omegapts_3v1[0:] 


    for s in is_inf_2v2p[1:]:
        m1 = s 
        m2 = 1
        omega_slopes_collection.append((m1, m2))
        
        
    orderedomegas_2v2unp_copy = orderedomegas_2v2unp.copy()

    orderedomegas_2v2unp_copy.pop(0)

    # print(orderedomegas_2v2unp_copy)


    is_inf_2v2unp = is_inf_2v2unp[1:]
    for thing in range(len(orderedomegas_2v2unp_copy)-1):
        if is_inf_2v2unp[thing] == None: 
            omega_points_collection.append(orderedomegas_2v2unp_copy[thing])

        else:
            omega_slopes_collection.append(orderedomegas_2v2unp_copy[thing])
            # print(orderedomegas_2v2unp_copy[thing]) 

            

    return omega_points_collection, omega_slopes_collection

def compute_matching_dist(lub, critval_coords, omega_points_collection, omega_slopes_collection, M, N):

    lub0  = list(set(lub[0]))
    lub1 = list(set(lub[1]))
    closureMN = critval_coords + lub0 + lub1

    pointstoiterateover = closureMN + omega_points_collection  ### do we need to add again the critical values here 
    sloppyslopestoiterateover = omega_slopes_collection

    Lines = []
    Wb  = []


    ## Lines through pairs of points 

    for x in range(len(pointstoiterateover)):
        for y in range(x, len(pointstoiterateover)):
            L = mod.line_through_2points(pointstoiterateover[x], pointstoiterateover[y]) ## here is the issue with none type error
            if L.positive == True:
                Lines.append(L)
                w = mod.compute_weighted_bottleneck(M,N,L)
                Wb.append(w)

                ##########
    ## Lines through a point and with a given slope

    for x in range(len(closureMN)): 
        for y in range(len(sloppyslopestoiterateover)):
            L = mod.Line(sloppyslopestoiterateover[y], closureMN[x])
            if L.positive == True:
                Lines.append(L)
                w = mod.compute_weighted_bottleneck(M,N,L)
                Wb.append(w)
                


    # Lines of slope 1 through one point 
                
    for x in range(len(pointstoiterateover)):
        L = mod.Line((1,1), pointstoiterateover[x])
        if L.positive == True:
            Lines.append(L)
            w = mod.compute_weighted_bottleneck(M,N,L)
            Wb.append(w) 
                
            
    matching_dist = max(Wb)
    idx = Wb.index(matching_dist)

    print('The matching distance is {}'.format(matching_dist))
    print('Matching distance is attained at the line with slope {} and intercept {}'.format(Lines[idx].m, Lines[idx].b))

    return 

def check_onedim_mods(bl_m, tr_m, bl_n, tr_n):
    # # figuring stuff out: 
    # bl tr YES
    ai = bl_m
    bi = tr_m

    ci = bl_n
    di = tr_n


    min_ba = min((bi[0] - ai[0])/2, (bi[1] - ai[1])/2 )
    min_cd = min((di[0] - ci[0])/2, (di[1] - ci[1])/2 )
    max_abcd = max(min_ba, min_cd)

    infnorm_ca= LA.norm(ci - ai, np.inf)
    infnorm_db= LA.norm(di - bi, np.inf)

    max_infs = max(infnorm_ca, infnorm_db)

    min_all = min(max_abcd, max_infs)
    print("matching distance (from equation) is", min_all)
    return

def do_all_the_things(onedim_mods, graph, example, MN):
    tl_m, tr_m, bl_m, br_m, tl_n, tr_n, bl_n, br_n = MN[0], MN[1], MN[2], MN[3], MN[4], MN[5], MN[6], MN[7]
    if onedim_mods and graph:
        print("Warning: Currently cannot print graphs from one-dim mod option. Continuing without graphs.\n")
        graph = False

    if onedim_mods:
        critical_vals, nolub, M, N, critval_coords = make_1dim_MN_example(tl_m, tr_m, bl_m, br_m, tl_n, tr_n, bl_n, br_n)

    if not onedim_mods:
        critical_vals, nolub, M, N = example[0], example[1], example[2], example[3]
        critval_coords = []
        ## forgets the parent modules 
        for i in range(len(critical_vals)):
            critval_coords.append(critical_vals[i].coords)
        
        

    ## computes the least upper bound CM and CN separately 
    # using the parent module information 
    lub = omega.closure_lub(critical_vals) 

    ### run all three allgoriths 3v1, 2v2 paired , 2v2 unpaired
    critpts, crits_no_lub, is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp = compute_switch_points(critical_vals, nolub, makegraphyesno = graph, title = " ")
    # combine the outputs together and deal with slopes vs points
    omega_points_collection, omega_slopes_collection = combine_omegas(is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp)

    print("\n")
    compute_matching_dist(lub, critval_coords, omega_points_collection, omega_slopes_collection, M, N)

    print("\n")
    if onedim_mods:
        check_onedim_mods(bl_m, tr_m, bl_n, tr_n)
    return