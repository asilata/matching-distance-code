import modules as mod
# from scipy.stats import qmc
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd
import modules as mod
import examples as ex
import plot as ourplot
import csv
# import bunny_smaller
import omega_pts as omega
from numpy import linalg as LA
from math import cos, sin, pi, atan
import time
import settings

def make_1dim_MN_example(tr_m, bl_m, tr_n, bl_n):
    # calculate other coords from tr and bl
    tl_m = np.array([bl_m[0],tr_m[1]])
    br_m = np.array([tr_m[0],bl_m[1]])
    tl_n = np.array([bl_n[0],tr_n[1]])
    br_n = np.array([tr_n[0],bl_n[1]])

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

def compute_switch_points(critpts, crits_no_lub, prune, makegraphyesno = False, title = 'title'):

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
    if settings.print_output:
        print("______________________________________")
    # print("Running the three algorithms.")
    # print("-------------")


    # print("3v1:")
    omegapts_3v1, _, _ = omega.output_alg_3_1(critpts, "socg/" + title, prune)
    if makegraphyesno:
        ourplot.plot_both_c_o(crits_no_lub, omegapts_3v1, title, dpi, "3v1")
    
    if settings.print_output:
        print("-------------")
    # algo 2v2 paired = Algorithm 5 in SoCG overleaf
    # print("2v2paired:")
    omegapts_2v2_p, _, _, is_inf_2v2p, orderedomegas2v2p = omega.output_alg_2_2_paired(
        critpts, "socg/" + title, prune
    )

    if makegraphyesno:
        ourplot.plot_c_o_with_inf(crits_no_lub, orderedomegas2v2p, is_inf_2v2p, title, dpi, "2v2 Paired")

    # algo 2v2 unpaired = Algorithm 7 in SoCG overleaf
    if settings.print_output:
        print("-------------")

    # print("2v2unpaired:")
    omegapts_2v2_unp, _, _, is_inf_2v2unp_orig , orderedomegas_2v2unp = omega.output_alg_2_2_unpaired(
        critpts, "socg/" + title, prune
    )
    if settings.print_output:
        print("______________________________________")

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

    ## Lines through pairs of points 
    all_bottle_time = 0
    for x in range(len(pointstoiterateover)):
        for y in range(x, len(pointstoiterateover)):
            L = mod.line_through_2points(pointstoiterateover[x], pointstoiterateover[y]) ## here is the issue with none type error
            if L.positive == True:
                Lines.append(L)

    ## Lines through a point and with a given slope
    for x in range(len(closureMN)): 
        for y in range(len(sloppyslopestoiterateover)):
            L = mod.Line(sloppyslopestoiterateover[y], closureMN[x])
            if L.positive == True:
                Lines.append(L)         


    # Lines of slope 1 through one point          
    for x in range(len(pointstoiterateover)):
        L = mod.Line((1,1), pointstoiterateover[x])
        if L.positive == True:
            Lines.append(L)

    if settings.actually_compute_matching_distance:
        # compute match dist separately out of for loops
        all_ws = []
        time_bottleneck = time.time()
        for L in Lines:
            w = mod.compute_weighted_bottleneck(M,N,L)
            all_ws.append(w)
        time_bottleneck_end = time.time()
        
        matching_dist = max(all_ws)
        idx = all_ws.index(matching_dist)
    else:
        time_bottleneck = 0
        time_bottleneck_end = 0
        matching_dist = -1

    # print("alt match dist {:.3f}".format(match_dist_2))

    
    # all_bottle_time += (bottletime_7 - bottletime_6)
    # print("BOTTLETIME", all_bottle_time)

    

    # print('Matching distance is {},'.format(matching_dist))
    # print('and is attained at the line with slope {} \nand intercept {}.'.format(Lines[idx].m, Lines[idx].b))
    if settings.print_output and settings.actually_compute_matching_distance:
        print('Matching dist: {:.3f} with slope ({:.3f}, {:.3f}) and intercept ({:.3f}, {:.3f}).'.format(matching_dist, Lines[idx].m[0], Lines[idx].m[1], Lines[idx].b[0], Lines[idx].b[1]))
    if settings.compare_line_counts:
        print('Lines counted: {}'.format(len(Lines)))
    if settings.print_output and settings.actually_compute_matching_distance:
        print("Time to compute bottleneck dists: {:.3f} sec".format(time_bottleneck_end - time_bottleneck))
    if settings.print_output == True and settings.actually_compute_matching_distance == False:
        print("WARNING: no exact matching distance computed! ")
    return matching_dist , len(Lines) ## C: added len(Lines) to return

def check_onedim_mods(bl_m, tr_m, bl_n, tr_n, graph):
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
    if settings.print_output:
        print("Matching distance (from equation) is {}.".format(min_all))

    ##########
    if graph:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.grid(visible = True )
        ## rectangles 
        # a1 = rect_m1.bottom_left 
        a1 = bl_m
        # h1= rect_m1.top_right[0]- a1[0]
        h1 = tr_m[0] - a1[0]
        # v1= rect_m1.top_right[1]- a1[1]
        v1 = tr_m[1] - a1[1]
        # a2 = rect_m2.bottom_left 
        a2 = bl_n
        # h2= rect_m2.top_right[0]- a2[0]
        h2 = tr_n[0] - a2[0]
        # v2= rect_m2.top_right[1]- a2[1]
        v2 = tr_n[1] - a2[1]
        from matplotlib import patches
        # m
        rect1 = patches.Rectangle(a1,h1,v1,color ='blue', alpha = 0.2)
        # n
        rect2 = patches.Rectangle(a2,h2,v2, color ='green',alpha = 0.2)

        # ## lines
        # x = np.linspace(-2, 10, 1000)

        # b1 = L_max.b[0]
        # b2 = L_max.b[1]
        # m1 = L_max.m[0]
        # m2 = L_max.m[1]
        # plt.plot(x, m2*(x-b1)/m1 +b2, linestyle='solid') ##L _
        # plt.plot(x,x,linestyle='dashed')

        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.legend(["N", "M"])
        ax.set_aspect("equal")
        plt.ylim([min(bl_m[1], bl_n[1]) - 1, max(tr_m[1], tr_n[1]) + 1])
        plt.xlim([min(bl_m[0], bl_n[0]) - 1, max(tr_m[0], tr_n[0]) + 1])

        plt.title('Modules')  
        #plt.savefig('moduleM')
        plt.show()
    #########
    return

def do_all_the_things(onedim_mods, graph, example, MN, prune = True):
    start_time = time.time()
    tr_m, bl_m, tr_n, bl_n = MN[0], MN[1], MN[2], MN[3]
    # tl_m = np.array([bl_m[0],tr_m[1]])
    # br_m = np.array([tr_m[0],bl_m[1]])
    # tl_n = np.array([bl_n[0],tr_n[1]])
    # br_n = np.array([tr_n[0],bl_n[1]])
    graphh = False
    if onedim_mods and graph:
        if settings.print_output:
            print("⚠️ Warning: Currently cannot print graphs from one-dim mod option.\nContinuing without graphs.\n")
        graph = False
        graphh = True

    if onedim_mods:
        critical_vals, nolub, M, N, critval_coords = make_1dim_MN_example(tr_m, bl_m, tr_n, bl_n)

    if not onedim_mods:
        critical_vals, nolub, M, N = example[0], example[1], example[2], example[3]
        critval_coords = []
        ## forgets the parent modules 
        for i in range(len(critical_vals)):
            critval_coords.append(critical_vals[i].coords)
        
        

    ## computes the least upper bound CM and CN separately 
    # using the parent module information 
    lub = omega.closure_lub(critical_vals) 

    start_time_switch_pts = time.time()
    ### run all three allgoriths 3v1, 2v2 paired , 2v2 unpaired
    critpts, crits_no_lub, is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp = compute_switch_points(critical_vals, nolub, prune, makegraphyesno = graph, title = " ")
    # combine the outputs together and deal with slopes vs points
    omega_points_collection, omega_slopes_collection = combine_omegas(is_inf_2v2unp_orig, omegapts_3v1, is_inf_2v2p, orderedomegas_2v2unp)
    end_time_switch_pts = time.time()
    switch_time = end_time_switch_pts - start_time_switch_pts

    start_time_match_dist = time.time()
    matching_dist, num_lines = compute_matching_dist(lub, critval_coords, omega_points_collection, omega_slopes_collection, M, N) ## C: added num_lines here 
    end_time_match_dist = time.time()
    match_time = end_time_match_dist - start_time_match_dist

    # print("\n")
    if onedim_mods:
        check_onedim_mods(bl_m, tr_m, bl_n, tr_n, graphh)
    end_time = time.time()
    tot_time = end_time - start_time
    if settings.print_output:
        print("Time elapsed:", "{:.3f}".format(tot_time),"sec")
        print("Time to compute switch pts:", "{:.3f}".format(switch_time),"sec")
        if settings.actually_compute_matching_distance:
            print("Time to compute match dist:", "{:.3f}".format(match_time),"sec")
        # print("_____________________________________")

    return matching_dist, num_lines

def make_example(M,N):
    # this is for two modules M and N 

    # input example (this is small_socg_ex_M_N): 
    # tr, bl 
    # M = [[(6.0, 6.0),(0.0, 0.0)]]
    # N = [[(8.0, 4.0),(4.0, 2.0)],
    #     [(2.0, 10.0),(1.0, 5.0)]]


    # M gets parent index 0
    # N gets parent index 1
    crits_no_lub = []
    critpts = []
    #(self, top_left,top_right, bottom_left, bottom_right, 
            # dim (num of rectangles), parent (M is 0, N is 1)):

    m_rects = []
    n_rects = []

    for i in range(len(M)):
        # iterate over the rectangles
        tr = M[i][0]
        bl = M[i][1]
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        # print("tr, bl, tl, br:\n", tr, bl, tl, br)
        # tl, tr, bl, br, dim, parent
        # print("⚠️chf.make_example: remember to check if dim always 1 here")
        m_i = mod.Rectangle(tl, tr, bl, br, 1, 0)
        m_rects.append(m_i)

        #bl, br, tl, NO tr
        crits_no_lub.append((bl,0))
        crits_no_lub.append((br,0))
        crits_no_lub.append((tl,0))
        # crits_no_lub.append((tr,0))
        #bl, br, tl, NO tr
        critpts.append(mod.critical_val(bl,0))
        critpts.append(mod.critical_val(br,0))
        critpts.append(mod.critical_val(tl,0))
        # critpts.append(mod.critical_val(tr,0))

    for i in range(len(N)):
        tr = N[i][0]
        bl = N[i][1]
        tl = (bl[0], tr[1])
        br = (tr[0], bl[1])
        # print("tr, bl, tl, br:\n", tr, bl, tl, br)
        # tl, tr, bl, br, dim, parent
        n_i = mod.Rectangle(tl, tr, bl, br, 1, 1)
        n_rects.append(n_i)

        #bl, br, tl, NO tr
        crits_no_lub.append((bl,1))
        crits_no_lub.append((br,1))
        crits_no_lub.append((tl,1))
        # crits_no_lub.append((tr,1))
        #bl, br, tl, NO tr
        critpts.append(mod.critical_val(bl,1))
        critpts.append(mod.critical_val(br,1))
        critpts.append(mod.critical_val(tl,1))
        # critpts.append(mod.critical_val(tr,1))

    retM = mod.RectangleModule(m_rects)
    retN = mod.RectangleModule(n_rects)
        
    return critpts, crits_no_lub, retM, retN



###########################
### Approximation functions 

def closure_lub(Points): 
        """ Find the closure under least upper boud of the critical points
            Input: list of points
        """
         
        l = len(Points)
        for i in range(l): 
            p = Points[i]
            for j in range(i+1, l): 
                q = Points[j]
                if not mod.are_comparable(p,q):
                    lub = (max(p[0],q[0]), max(p[1],q[1]))
                    Points.append(lub)

        return list(set(Points))
    
def plot_weighted_bottleneck(M,N, graph, filename = 'weightedBottlneckDistance'):
    start_time = time.time()
    """Takes M and N as RectangleModules 
        example: 
        rect_m1 = mod.Rectangle((0,0),(7,7),1)
        rect_m2 = mod.Rectangle((0,4),(7,11),1)
        M = mod.RectangleModule([rect_m1,rect_m2])
        rect_n1 = mod.Rectangle((0,0),(7,11),1)
        rect_n2 = mod.Rectangle((0,4),(7,7),1)
        N= mod.RectangleModule([rect_n1,rect_n2])
    """
    
    Crit_M = M.closure_lub() 
    Crit_N = N.closure_lub() 
    C = list(set(Crit_M+Crit_N))
    Crit_MN = closure_lub(C)
    #print(len(Crit_MN))
    #Crit_MN=list(set(Crit_M+Crit_N))
    Lines = []
    DD = []
    k = 0
    Crit = []
    for i in range(len(Crit_MN)-1):
        p = Crit_MN[i]
        for j in range(i+1,len(Crit_MN)):
            q = Crit_MN[j] 
            line = mod.line_through_2points(Crit_MN[i], Crit_MN[j])
            if line.positive: 
                d = mod.compute_weighted_bottleneck(M,N,line)
                Lines.append(line)
                Crit.append([Crit_MN[i], Crit_MN[j]])
                DD.append(d)
    # print('There are {} lines through critical points'.format(len(Lines)))
    #print('Bottleneck distance for lines through critical points: ')
    #print(D)
    if settings.print_output: 
        print('Maximum distance for lines through critical points: {:.3f}'.format(max(DD)))
    if settings.compare_line_counts:
        print('Lines counted crit pts: {}'.format(len(Lines)))   
    max_dist_critpts = max(DD)
    # print(max(DD))
    
    ## computing bottlneck for "every" line
    
    Theta = np.linspace(0,pi/2,100)[1:-1]
    B = np.linspace(-5,5,100)
    D= np.zeros((len(Theta), len(B)))
    T = []
    BB= []
    Dist = []
    for t in range(len(Theta)): 
        for n in range(len(B)): 
            s = sin(Theta[t])
            c = cos(Theta[t])
            maxm = max(s,c)
            line = mod.Line((c/maxm, s/maxm), (B[n],-B[n]))
            d = mod.compute_weighted_bottleneck(M,N,line)
            D[t,n] = d
            T.append(Theta[t])
            BB.append(B[n])
            Dist.append(d)
    val = max(Dist)
    idx = Dist.index(val)
    if settings.print_output:
        print('Maximum distance computed for grid of lines: {:.3f}'.format(max(Dist)))
        print('Number of grid points: {}'.format(len(Dist)))
    max_grids_lines = max(Dist)
    # print(max(Dist))

    if settings.save_figure and graph:     
        plt.figure(figsize=(8,8))
        plt.scatter(T, BB, c= Dist,s = 10, cmap = "summer")
        plt.scatter(T[idx], BB[idx], marker = 'x', color = 'red')
        # print(T[idx])
        # print(BB[idx])
        
        ## plot markers for the lines through critical points
        b_crit = []
        theta_crit = []
        for j in range(len(Lines)):
            Line = Lines[j]
            b= Line.b[0]
            theta = atan(Line.m[1]/Line.m[0])
            b_crit.append(b)
            theta_crit.append(theta)
        
        for j in range(len(Lines)): 
            plt.scatter(theta_crit[j], b_crit[j], marker = 'x', color = 'grey')
            #plt.text(theta_crit[j], b_crit[j], str(Crit[j]))
        val = max(DD)
        idx=DD.index(val)
        plt.scatter(theta_crit[idx], b_crit[idx], marker = 'x', color = 'black')
        ## plot titles
        plt.xlabel('theta')
        plt.ylabel('b')
        plt.title("Weighted bottleneck distance as a function of theta and b")
        plt.colorbar(label="Weighted distance", orientation="horizontal")
        plt.clim(0,max(Dist))
        plt.show()
        # plt.show()
        # plt.savefig(filename)

    end_time = time.time()
    tot_time = end_time - start_time
    if settings.print_output:
        print("Time elapsed:", "{:.3f}".format(tot_time),"sec")
        # print("____________________")
        # print("END")
        # print("____________________")

    # if settings.compare_line_counts:
    #     print("hi, this is where line counts go")
    # if settings.save_figure:
    #     plt.show()
    return max_dist_critpts, max_grids_lines
    
def compute_weighted_bottleneck_distances(M,N): 
    """Takes M and N as RectangleModules 
        example: 
        rect_m1 = mod.Rectangle((0,0),(7,7),1)
        rect_m2 = mod.Rectangle((0,4),(7,11),1)
        M = mod.RectangleModule([rect_m1,rect_m2])
        rect_n1 = mod.Rectangle((0,0),(7,11),1)
        rect_n2 = mod.Rectangle((0,4),(7,7),1)
        N= mod.RectangleModule([rect_n1,rect_n2])
    """
    
    Crit_M = M.closure_lub() 
    Crit_N = N.closure_lub() 
    C = list(set(Crit_M+Crit_N))
    Crit_MN = closure_lub(C)
    #print(len(Crit_MN))
    #Crit_MN=list(set(Crit_M+Crit_N))
    Lines = []
    DD = []
    k = 0
    Crit = []
    for i in range(len(Crit_MN)-1):
        p = Crit_MN[i]
        for j in range(i+1,len(Crit_MN)):
            q = Crit_MN[j] 
            line = mod.line_through_2points(Crit_MN[i], Crit_MN[j])
            if line.positive: 
                d = mod.compute_weighted_bottleneck(M,N,line)
                Lines.append(line)
                Crit.append([Crit_MN[i], Crit_MN[j]])
                DD.append(d)
    if settings.print_output:
        print('Lines counted {} again'.format(len(Lines)))
        print('Maximum distance for lines through critical points:')
        print(max(DD))
    
    ## computing bottlneck for "every" line
    
    Theta = np.linspace(0,pi/2,100)[1:-1]
    B = np.linspace(-5,5,100)
    D= np.zeros((len(Theta), len(B)))
    T = []
    BB= []
    Dist = []
    for t in range(len(Theta)): 
        for n in range(len(B)): 
            s = sin(Theta[t])
            c = cos(Theta[t])
            maxm = max(s,c)
            line = mod.Line((c/maxm, s/maxm), (B[n],-B[n]))
            d = mod.compute_weighted_bottleneck(M,N,line)
            D[t,n] = d
            T.append(Theta[t])
            BB.append(B[n])
            Dist.append(d)
    val = max(Dist)
    idx = Dist.index(val)
    if settings.print_output:
        print('Maximum distance computed from grid of lines:')
        print(max(Dist))     
        print(T[idx])
        print(BB[idx])
    
    s = sin(T[idx])
    c = cos(T[idx])
    maxm = max(s,c)
    L_max = mod.Line((c/maxm, s/maxm), (BB[idx],-BB[idx]))
    return T,BB, idx, L_max

######################
# EXPERIMENTS

def to_prune_or_not_to_prune(M,N):
    # prune by default true
    # what we want: 
    # prune TRUE means let algo decide if take the thing
    # prune FALSE means always return all the things
    ###################
    if settings.print_output:
        print("Rectangles in M: {} and N: {}. Total: {}.".format(len(M), len(N), len(M) + len(N)))
        print("PRUNE POINTS")
    prune = True

    ######### M AND N can have MORE THAN ONE RECTANGLE
    # set one_rect_mods -> FALSE
    # M,N = ex.test_ex_more_rects()

    graph = False
    one_rect_mods = False

    ##################
    tr_m, bl_m, tr_n, bl_n = ex.test_ex_one_rect()
    example = make_example(M,N)
    MN = [tr_m, bl_m, tr_n, bl_n]
    do_all_the_things(one_rect_mods, graph, example, MN, prune)
    if settings.print_output:
        print("\n")
        print("DON'T PRUNE POINTS")
    prune = False
    do_all_the_things(one_rect_mods, graph, example, MN, prune)

    # also do the approx matching dist
    if settings.print_output:
        print("\nApproximate Matching Distance:")
    Mmod = example[2]
    Nmod = example[3]
    plot_weighted_bottleneck(Mmod, Nmod, False, 'test_figure')

def to_prune_or_not_to_prune_csv(M,N):
    # prune by default true
    # what we want: 
    # prune TRUE means let algo decide if take the thing
    # prune FALSE means always return all the things
    ###################
    #print("Rectangles in M: {} and N: {}. Total: {}.".format(len(M), len(N), len(M) + len(N)))
    #print("PRUNE POINTS")
    prune = True

    ######### M AND N can have MORE THAN ONE RECTANGLE
    # set one_rect_mods -> FALSE
    # M,N = ex.test_ex_more_rects()

    graph = False
    one_rect_mods = False

    ################## PRUNE
    tr_m, bl_m, tr_n, bl_n = ex.test_ex_one_rect()
    example = make_example(M,N)
    MN = [tr_m, bl_m, tr_n, bl_n]

    #################### APPROX
    # also do the approx matching dist
    #print("\nApproximate Matching Distance:")
    Mmod = example[2]
    Nmod = example[3]
    approx_start_time = time.time()
    max_dist_critpts, max_grids_lines = plot_weighted_bottleneck(Mmod, Nmod, False, 'test_figure')
    settings.lower_bound_D = min(max_dist_critpts, max_grids_lines)
    approx_end_time = time.time()
    approx_time = approx_end_time - approx_start_time
    #return prune_time, no_prune_time, approx_time, prune_match_dist, no_prune_match_dist, max_dist_critpts, max_grids_lines

    ## This is the EXACT (slow) computation
    prune_start_time = time.time()
    prune_match_dist, _ = do_all_the_things(one_rect_mods, graph, example, MN, prune) ## C: added empty _ here for the the second output of do_all_the_things
    #print("\n")
    prune_end_time = time.time()
    prune_time = prune_end_time - prune_start_time

    ################# NO PRUNE
    #print("DON'T PRUNE POINTS")
    #prune = False
    #no_prune_start_time = time.time()
    #no_prune_match_dist = do_all_the_things(one_rect_mods, graph, example, MN, prune)
    #no_prune_end_time = time.time()
    #no_prune_time = no_prune_end_time - no_prune_start_time
    
    # note: if it matters, APPROX used to be down here. Moved up 21 March 2025 for NEW PRUNE thingy
    

    return prune_time, approx_time, prune_match_dist, max_dist_critpts, max_grids_lines

# Random rectangles
def plot_rectangles(M,N,img_path):
    from matplotlib import patches
    # Get rectangles from the example function
    # M, N = ex.test_ex_more_rects()

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot rectangles in M (colored red)
    for rect in M:
        tr, bl = rect
        width = tr[0] - bl[0]
        height = tr[1] - bl[1]
        ax.add_patch(patches.Rectangle(bl, width, height, linewidth=1, edgecolor='r', facecolor='red', alpha=0.5))

    # Plot rectangles in N (colored blue)
    for rect in N:
        tr, bl = rect
        width = tr[0] - bl[0]
        height = tr[1] - bl[1]
        ax.add_patch(patches.Rectangle(bl, width, height, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.5))

    # Set the limits of the plot
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 12)

    # Set the aspect of the plot to be equal
    ax.set_aspect('equal')

    import matplotlib.lines as mlines

    eight = mlines.Line2D([], [], color='red', marker='D', ls='', label='M')
    nine = mlines.Line2D([], [], color='blue', marker='D', ls='', label='N')
    # etc etc
    ax.legend(handles=[eight, nine])

    fig.savefig(img_path, format='png', dpi=250)

    # Show the plot
    # plt.show()


def generate_random_rectangles(num_M, num_N, seed = None):
    # Set the random seed if provided
    if seed is not None:
        rnd.seed(seed)

        def create_random_rectangle():
            while True:
                # Generate bottom-left corner (bl)
                bl_x = rnd.uniform(0, 15)
                bl_y = rnd.uniform(0, 15)
                # Generate top-right corner (tr)
                tr_x = rnd.uniform(0, 15)
                tr_y = rnd.uniform(0, 15)
                # Ensure width and height are at least 1
                width = tr_x - bl_x
                height = tr_y - bl_y
                if width >= 1 and height >= 1:
                    return [(tr_x, tr_y), (bl_x, bl_y)]
                else:
                    while width < 1 or height < 1:
                        # Generate bottom-left corner (bl)
                        bl_x = rnd.uniform(0, 15)
                        bl_y = rnd.uniform(0, 15)
                        # Generate top-right corner (tr)
                        tr_x = rnd.uniform(0, 15)
                        tr_y = rnd.uniform(0, 15)
                        width = tr_x - bl_x
                        height = tr_y - bl_y
                    return [(tr_x, tr_y), (bl_x, bl_y)]


    # Generate M with num_M rectangles
    M = [create_random_rectangle() for _ in range(num_M)]

    # Generate N with num_N rectangles
    N = [create_random_rectangle() for _ in range(num_N)]

    return M, N

def append_to_csv(file_path, new_data):
    column_name = new_data['Label']
    # Read the existing CSV into a list of dictionaries
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    # if settings.print_output: 
    #     print(rows[:2])
    
    # Add the new data to each row based on the 'Label' column
    for row in rows:
        key = row['Label']  # Now we explicitly look for the 'Label' column
        if key in new_data:
            row[column_name] = new_data[key]
    # if settings.print_output:
    #     print(rows[:2])
    
    # Write the updated rows back to the CSV
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = reader.fieldnames + [column_name]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)





def experiment_1(M,N):
    """Code to get the data for experiment 1
    Return the number of lines computed by our algorithm for the matching distanc
    
    """
    prune = True

    ######### M AND N can have MORE THAN ONE RECTANGLE
    # set one_rect_mods -> FALSE
    # M,N = ex.test_ex_more_rects()

    graph = False
    one_rect_mods = False

    ################## PRUNE
    tr_m, bl_m, tr_n, bl_n = ex.test_ex_one_rect()
    example = make_example(M,N)
    MN = [tr_m, bl_m, tr_n, bl_n]
    prune_start_time = time.time()
    prune_match_dist, num_lines = do_all_the_things(one_rect_mods, graph, example, MN, prune)
    #print("\n")
    prune_end_time = time.time()
    prune_time = prune_end_time - prune_start_time

    ################# NO PRUNE
    #print("DON'T PRUNE POINTS")
    #prune = False
    #no_prune_start_time = time.time()
    #no_prune_match_dist = do_all_the_things(one_rect_mods, graph, example, MN, prune)
    #no_prune_end_time = time.time()
    #no_prune_time = no_prune_end_time - no_prune_start_time
    
    #################### APPROX
    # also do the approx matching dist
    #print("\nApproximate Matching Distance:")
    Mmod = example[2]
    Nmod = example[3]
    #approx_start_time = time.time()
    #max_dist_critpts, max_grids_lines = plot_weighted_bottleneck(Mmod, Nmod, False, 'test_figure')
    #approx_end_time = time.time()
    #approx_time = approx_end_time - approx_start_time
    #return prune_time, no_prune_time, approx_time, prune_match_dist, no_prune_match_dist, max_dist_critpts, max_grids_lines
    
    return num_lines 
