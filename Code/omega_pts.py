import gudhi
from math import cos, sin, pi
import numpy as np

import modules as mod

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

    
###### 3 vs 1 point 

def compute_3vs1(M, N): 
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
                                                

