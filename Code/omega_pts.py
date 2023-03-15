import gudhi
from math import cos, sin, pi
import numpy as np

import modules as mod
import numpy.linalg

## for checking if in convex hull
import scipy.spatial
from scipy.optimize import linprog

import modules as mod

import csv


###### Convex hull functions ####

def in_hull(points, x):
    ## check if x in convex hull of points 
    ## points = array of pts in R^2 
    
    n_points = len(points)
    c = np.zeros(n_points)
    A = np.r_[points.T,np.ones((1,n_points))]
    b = np.r_[x, np.ones(1)]
    lp = linprog(c, A_eq=A, b_eq=b, )
    return lp.success

def sort_bottom_and_right(u,v,w): 
    """return the rightmost and bottommost points of u,v,w """
    
    rm = u
    if v[0]>rm[0]:
        rm = v
    if w[0] > rm[0]:
        rm = w
        
    bm = u
    if v[1]< bm[1]:
        bm = v
    if w[1] < bm[1]:
        bm = w

    return bm, rm


def check_in_quadrant_tl(x, p, q): 
    """"assume p is the bottomost pt of u,v,w
        assume q is the rightmost of u,v,w 
        return True if x is in the top left quadrant 
    """
 
    if x[0]<= q[0] and x[1]>=p[1]: 
        return True 
    else: 
        return False 
        

def check_x_push_up(x,u,v,w): ## Check-point-A and Check-point-B like in the overleaf 
    """Check if the points x,u,v,w are admissible for:
            - x pushing up
            - u,v,w pushing right 
        returns True if they are an admissible quadruple 
        and False if they are not admissible or would create superfluous omegapoints 
    """    
    p,q = sort_bottom_and_right(u,v,w)
    a = (q[0],p[1])
    
    ## First check if x is in the upper left quadrant: 
    if check_in_quadrant_tl(x,p,q): 
        ## Check if x is in convex hull
        if in_hull(np.array([u,v,w]),x):
            return False
        
        elif in_hull(np.array([u,v,w,a]),x ):
            return True
        
        else:
            return False
        
    else: 
        return True 

    
def sort_top_and_left(u,v,w): 
    """return the leftmost and topmost points of u,v,w """
        
    lm = u
    if v[0]<lm[0]:
        lm = v
    if w[0] < lm[0]:
        lm = w
        
    tm = u
    if v[1]> tm[1]:
        tm = v
    if w[1] > tm[1]:
        tm = w

    return tm, lm


def check_in_quadrant_br(x, p, q): 
    """"assume p is the topmost pt of u,v,w
        assume q is the leftmost of u,v,w 
        return True if x is in the bottom right quadrant(including the boundary)
    """
    
    if x[0]>= q[0] and x[1]<=p[1]: 
        return True 
    else: 
        return False 

    
def check_x_push_right(x,u,v,w): 
    """Check if the points x,u,v,w are admissible for:
            - x pushing right
            - u,v,w pushing up 
        returns True if they are an admissible quadruple 
        and False if they are not admissible or would create superfluous omegapoints 
    """    
    
    p,q = sort_top_and_left(u,v,w)
    a = (q[0],p[1])
    
    ## First check if x is in the upper left quadrant: 
    if check_in_quadrant_br(x,p,q): 
        ## Check if x is in convex hull
        if in_hull(np.array([u,v,w]),x):
            return False
        
        elif in_hull(np.array([u,v,w,a]),x ):
            return True  
        else: 
            return False 
    else: 
        return True 
        

    
### éalskdjfséladkjs


def check_3distinct(C):
    # this function checks that 3 out of 4 things in a set are distinct
    assert len(C) == 4 , "C is not of length 4 "
    if (len(C) - len(set(C))) > 1: 
        return False
    else: 
        return True 
    
def check_c_distinct(c,C):
    """this function checks that c, assumed to be in C, is not repeated in C"""
    C_new = C.copy()
    C_new.remove(c)
    val = True 
    for d in C_new: 
        if c.coords == d.coords: 
            val = False
    
    return val

def check_omega(CritPts,omega): 
    """ Function to be implemented later to check if the computed omegapoint is valid 
        for now: returns true all the time
    """
    
    return True
    





##### helper functions ###
def distance_line_pt(p1,p2,x):
    
    d= abs((p2[0]-p1[0])*(p1[1]-x[1]) - (p1[0]-x[0])*(p2[1]-p1[1])) / np.sqrt(np.square(p2[0]-p1[0]) + np.square(p2[1]-p1[1])) 
    return d 

def min_dist(list_pt,x,omega): 
    dists = [distance_line_pt(x,omega,pt) for pt in list_pt]
    min_idx = dists.index(min(dists))
    return list_pt[min_idx]
    
    
def check_omega(list_pt, x,omega):
    if x == omega: 
        return False
    else:
        pt = min_dist(list_pt, x,omega)
        if pt == omega:
            list_pt.remove(pt)
            pt = min_dist(list_pt, x,omega)
            if pt == omega: 
                list_pt.remove(pt)  
          
        L1 = mod.line_through_2points(min_dist(list_pt,x,omega), omega)
        L = mod.line_through_2points(x,omega)
    if L.positive and L1.positive:
        return True 
    else: 
        return False 

    
    
    
    
#####  3 vs 1 new version 


def algo_3vs1(CritPts): 
    ## input: 4 critical points from C_M and C_N

    ## Check that we have at least three distinct points, otherwise stop
    assert check_3distinct(CritPts), "There is more than one repeated point in the list"

    Omega_pts = []
    dict_omega_pts = []


    for c in CritPts: 
        # Trying to find x (of the points x,w,u,v in the paper)
        if check_c_distinct(c, CritPts): ## want a critical point x that is distinct from u,v,w
            x = c 
        else: 
            continue ### Skips the rest of the loop if c appears multiple times in C 

        CritPts_no_x = CritPts.copy()
        CritPts_no_x.remove(x)

        for d in CritPts_no_x: 
            w = d
            CritPts_no_x_no_w  = CritPts_no_x.copy()
            CritPts_no_x_no_w.remove(w) ## lol (with a french accent), list with two elements only 
            
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
            if check_x_push_up(x.coords,u.coords,v.coords,w.coords):

                if u.coords[1] <= v.coords[1]: ## check if this needs to be <= or < 
                    temp_u = u
                    u = v
                    v = temp_u
                if w.coords[0] >= x.coords[0] and  w.coords[1] >= x.coords[1] : ## should this be strict inequality? , also check the coordinates 0 and 1 

                    omega = (x.coords[0],(eta/delta)*(v.coords[1]-u.coords[1])+w.coords[1])

                elif w.coords[0] <= x.coords[0] and  w.coords[1] <= x.coords[1] :

                    omega = (x.coords[0],(eta/delta)*(u.coords[1]-v.coords[1])+w.coords[1])

                else :
                    omega = (x.coords[0],(eta/delta)*(u.coords[1]-v.coords[1])+w.coords[1])
                    omega1 = (x.coords[0],(eta/delta)*(v.coords[1]-u.coords[1])+w.coords[1])

                    Omega_pts.append(omega1) ## append
                    ##  add omega pts to dictionary 
                    
                    dict_omega_pts.append([omega1,x.coords,u.coords,v.coords,w.coords,eta,delta])

                    #dict_omega_pts.append({ "omega_pts": omega1 , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })


                Omega_pts.append(omega) ## in any case we append omegaa
                #dict_omega_pts.append({ "omega_pts": omega , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                dict_omega_pts.append([omega,x.coords,u.coords,v.coords,w.coords,eta,delta])





                ## print!
                print('The omega point {} was generated from'.format(omega))
                print('x = {}'.format(x))
                print('w = {}'.format(w))
                print('u = {}'.format(u))
                print('v = {}'.format(v))
                print('****************')



               ### Is indentation correct? yes, same as above 
            if check_x_push_right(x.coords,u.coords,v.coords,w.coords):

                if u.coords[0]<= v.coords[0]: ## why not strict??
                    temp_u = u
                    u = v
                    v = temp_u
                if w.coords[0] >= x.coords[0] and w.coords[1] >= x.coords[1]: ## check < vs <= and coordinates 0,1

                    omega = ((eta/delta)*(v.coords[0]-u.coords[0])+w.coords[0], x.coords[1])

                elif w.coords[0] <= x.coords[0] and w.coords[1] <= x.coords[1]:
                    omega = ((eta/delta)*(u.coords[0]-v.coords[0])+w.coords[0], x.coords[1])

                else: 
                    omega = ((eta/delta)*(v.coords[0]-u.coords[0])+w.coords[0], x.coords[1])
                    omega1 = ((eta/delta)*(u.coords[0]-v.coords[0])+w.coords[0], x.coords[1])
                    Omega_pts.append(omega1)
                    ## dict for debuging
                    #dict_omega_pts.append({ "omega_pts": omega1 , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                    dict_omega_pts.append([omega1,x.coords,u.coords,v.coords,w.coords,eta,delta])



                Omega_pts.append(omega)
                ## dict for debuging
        
                #dict_omega_pts.append({ "omega_pts": omega , "x" : x.coords, "u":u.coords, "v": v.coords, "w": w.coords, "eta" :eta, "delta":delta })
                dict_omega_pts.append([omega,x.coords,u.coords,v.coords,w.coords,eta,delta])


                
                
                #### 

                #print('The omega point {} was generated from'.format(omega))
                #print('x = {}'.format(x))
                #print('w = {}'.format(w))
                #print('u = {}'.format(u))
                #print('v = {}'.format(v))
                #print('eta = {}'.format(eta))
                #print('delta = {}'.format(delta))
                #print('****************')




    print("Computed {} omega points with duplicates".format(len(Omega_pts)))         
                
    Omega_pts = list(set(Omega_pts))   
    print("Without duplicates: {}".format(len(Omega_pts)))
    
    #fields = ["omega_pts", "x","u","v","w","eta","delta"]

    
    """with open('test.csv', 'a', newline='') as file:  #### find a way to write everything in file
        writer = csv.DictWriter(file, fieldnames = fields,dialect='excel')
        writer.writeheader() 
        writer.writerows(dict_omega_pts)"""
    #dict_omega_pts = list(set(dict_omega_pts))

    return Omega_pts, dict_omega_pts




    
###### 3 vs 1 point old version

def compute_3vs1_old(M, N): 
    """M,N are modules"""
    CM = M.find_critical_pts()
    CN = N.find_critical_pts()
    C = list(set(CM + CN))
    lenc = len(C)
    Omega_pts= []
    for i in range(lenc):
        for j in range(i+1, lenc):
            for k in range(j+1, lenc):
                for l in range(k, lenc):
                    c1 = C[i]
                    c2 = C[j]
                    c3 = C[k]
                    c4 = C[l] ## c3 and c4 can be equal 
                    pts = [c1,c2,c3,c4]
                    for x in range(4):
                        pts = [c1,c2,c3,c4]
                        #print('choosing x')
                        for w in range(4):
                            pts = [c1,c2,c3,c4]
                            #print('choosing w')
                            X = pts[x]
                            W = pts[w]## 
                            if w != x:
                                pts.remove(W)
                                pts.remove(X)
                                ## choose delta = 1, 2, implement choice later
                                if pts[0] != pts[1]: 
                                    if pts[0][1] > pts[1][1]: 
                                        U = pts[0]
                                        V = pts[1]   
                                    else: 
                                        U = pts[1]
                                        V = pts[0]
                                    ## all possible choices of delta, eta

                                    ## pushing up 
                                    if X in CM and W in CM or X in CN and W in CN:
                                        eta = 2 
                                        if U in CM and V in CM or U in CN and V in CN: 
                                            delta = 2
                                            omega = (X[0], (eta/delta)*(V[1]-U[1]) + W[1])
                                            if omega != X: 
                                                Omega_pts.append(omega)
                                            omega = (X[0], (eta/delta)*(U[1]-V[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                        if U in CM and V in CN or U in CN and V in CM: 
                                            delta = 1
                                            omega = (X[0], (eta/delta)*(V[1]-U[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                            omega = (X[0], (eta/delta)*(U[1]-V[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)

                                    if X in CM and W in CN or X in CM and W in CN:
                                        eta = 1 
                                        if U in CM and V in CM or U in CN and V in CN: 
                                            delta = 2
                                            omega = (X[0], (eta/delta)*(V[1]-U[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                            omega = (X[0], (eta/delta)*(U[1]-V[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                        if U in CM and V in CN or U in CN and V in CM: 
                                            delta = 1
                                            omega = (X[0], (eta/delta)*(V[1]-U[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                            omega = (X[0], (eta/delta)*(U[1]-V[1]) + W[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega) 
                                    ## pshing right 
                                    if pts[0][0] > pts[1][0]: 
                                        U = pts[0]
                                        V = pts[1]   
                                    else: 
                                        U = pts[1]
                                        V = pts[0]
                                    ## all possible choices of delta, eta
                                    if X in CM and W in CN or X in CM and W in CN:
                                        eta = 1 
                                        if U in CM and V in CM or U in CN and V in CN:
                                            delta = 2
                                            omega = ((eta/delta)*(V[0]-U[0]) + W[0],X[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega) 
                                            omega = ((eta/delta)*(U[0]-V[0]) + W[0],X[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)
                                        if U in CM and V in CN or U in CN and V in CM:
                                            delta = 1
                                            omega = ((eta/delta)*(V[0]-U[0]) + W[0],X[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega) 
                                            omega = ((eta/delta)*(U[0]-V[0]) + W[0],X[1])
                                            if check_omega([U,V,W],X,omega):
                                                Omega_pts.append(omega)

                                                
    return Omega_pts
                                                

