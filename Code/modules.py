import gudhi
from math import cos, sin, pi
import numpy as np

"""TODO: 
    - implement algorithm to find all equivalence classes of a given module
    - function to plot easily a module and some lines though the parameter space
    - include "infinite rectangles", ie, open at the top and/or to the right 
    - check that the functions work also with infinite rectanlges
"""

# Class for single rectangles.
class Rectangle:
    def __init__(self, bottom_left, top_right, dim = 1):
        """bottom_left and top_right are (x,y) coordinate tuples, 
        dim = a non-negative integer representing the dimension of this rectangle."""
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.dim = dim
        #add error message when format is not good

    def __eq__(self, other):
        """Check equality of rectangles. Overrides the default."""
        if self.bottom_left != other.find_bl():
            return False
        if self.top_right != other.find_tr():
            return False
        if self.dim != other.find_dim():
            return False
        return True

    def eq_upto_dim(self, other):
        """Check equality of rectangles up to dimension."""
        if self.bottom_left != other.find_bl():
            return False
        if self.top_right != other.find_tr():
            return False
        return True

    def find_bl(self):
        """Returns the bottom left corner."""
        return self.bottom_left

    def find_tl(self):
        """Returns the top left corner."""
        x = self.bottom_left[0]
        y = self.top_right[1]
        return (x,y)

    def find_tr(self):
        """Returns the top right corner."""
        return self.top_right

    def find_br(self):                
        """Returns the bottom right corner."""
        x = self.top_right[0]
        y = self.bottom_left[1]
        return (x,y)

    def find_coordinates(self):
        return [self.find_bl(), self.find_tl(), self.find_tr(), self.find_br()]

    def find_dim(self):
        """Returns the dimension."""
        return self.dim

    def update_dim(self, d):
        """Sets dimension to d."""
        self.dim = d
    
    def find_intersection(self, line):
        """Find the intersection of the given line with self, in the appropriate notation."""
        #### what about intersection at a corner...???? 

        b = line.b[0]
        m1 = line.m[0]
        m2 = line.m[1]
        
        ## intersection with bottom side: 
        bl = self.bottom_left[1]
        t_bs = (bl+b)/m2
        pt_bs = (m1*t_bs +b, bl)
        
        ## intersection with top side: 
        tl = self.find_tl()[1]
        t_ts = (tl+b)/m2
        pt_ts = (m1*t_ts +b, tl)
       
        ## intersection with right side: 
        br= self.find_br()[0]
        t_rs = (br-b)/m1
        pt_rs = (br, m2*t_rs-b)
        
        ## intersection with left side:
        bl = self.bottom_left[0]
        t_ls = (bl-b)/m1
        pt_ls = (bl, m2*t_ls-b)
        
        inter = []
        params = []
        
        if self.bottom_left[0] <= pt_bs[0] <= self.find_br()[0]:
            inter.append(pt_bs)
            params.append(t_bs)
        
        if self.bottom_left[1] <= pt_ls[1] <= self.find_tl()[1]: 
            if pt_ls not in inter: 
                inter.append(pt_ls)
                params.append(t_ls) 
            
        if self.find_tl()[0] <= pt_ts[0] <= self.top_right[0]: 
                inter.append(pt_ts)
                params.append(t_ts)
              
        
        if self.find_br()[1] <= pt_rs[1] <= self.top_right[1]: 
            if pt_rs not in inter:
                inter.append(pt_rs)
                params.append(t_rs)
      
        return inter, params
    
    
###########################################################

class Right_infinite_rectangle:
    """ Complete this class"""
   
    def __init__(self, bottom_left,top_left, dim = 1):
        """bottom_left and top_left are (x,y) coordinate tuples, 
        dim = a non-negative integer representing the dimension of this rectangle."""
        self.bottom_left = bottom_left
        self.top_left = top_left
        self.top_right = np.inf
        self.bottom_right = np.inf
        self.dim = dim

    def find_dim(self):
        """Returns the dimension."""
        return self.dim
    
    def find_bl(self):
        """Returns the bottom left corner."""
        return self.bottom_left

    def find_tl(self):
        """Returns the top left corner."""
        return self.top_left

    def find_tr(self):
        """Returns the top right corner."""
        return self.top_right

    def find_br(self):                
        """Returns the bottom right corner."""
        return self.bottom_right
    
    def find_coordinates(self):
        return [self.find_bl(), self.find_tl(), self.find_tr(), self.find_br()]

    def find_dim(self):
        """Returns the dimension."""
        return self.dim

    def update_dim(self, d):
        """Sets dimension to d."""
        self.dim = d

    def find_intersection(self, line):
        """ Finds the intersection of a line and the rectangle module    """
        ## include intersection with corner... 
        b = line.b[0]
        m1 = line.m[0]
        m2 = line.m[1]

        ## intersection with bottom side: 
        bl = self.bottom_left[1]
        t_bs = (bl+b)/m2
        pt_bs = (m1*t_bs +b, bl)
        
        ## intersection with top side: 
        tl = self.find_tl()[1]
        t_ts = (tl+b)/m2
        pt_ts = (m1*t_ts +b, tl)
       
        ## intersection with right side: 
        t_rs = np.inf
        pt_rs = (np.inf,np.inf)
        ## intersection with left side:
        bl = self.bottom_left[0]
        t_ls = (bl-b)/m1
        pt_ls = (bl, m2*t_ls-b)
        
        inter = []
        params = []

        #### !! check if this could append more than two points if the intersecion is the uppper left corner!!

        ## do we need to check all the following conditioins? 
        
        #print(pt_bs)
        if self.bottom_left[0] <= pt_bs[0]: #<= self.find_br()[0]:
            inter.append(pt_bs)
            params.append(t_bs)
        
        if self.bottom_left[1] <= pt_ls[1] <= self.find_tl()[1]: 
            if pt_ls not in inter: 
                inter.append(pt_ls)
                params.append(t_ls) 
            
        if self.find_tl()[0] <= pt_ts[0]: # <= self.top_right[0]: 
                inter.append(pt_ts)
                params.append(t_ts)
              
        
        #if self.find_br()[1] <= pt_rs[1] <= self.top_right[1]: 
        #    if pt_rs not in inter:
         #       inter.append(pt_rs)
          #      params.append(t_rs)
      
        return inter, params

        
class Top_infinite_rectangle:
    """ Complete this class"""
   
    def __init__(self, bottom_left,bottom_right, dim = 1):
        """bottom_left and bottom_right are (x,y) coordinate tuples, 
        dim = a non-negative integer representing the dimension of this rectangle."""
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.top_left = np.inf 
        self.top_right = np.inf 
        self.dim = dim    

    def find_dim(self):
        """Returns the dimension."""
        return self.dim
    
    def find_bl(self):
        """Returns the bottom left corner."""
        return self.bottom_left

    def find_tl(self):
        """Returns the top left corner."""
        return self.top_left

    def find_tr(self):
        """Returns the top right corner."""
        return self.top_right

    def find_br(self):                
        """Returns the bottom right corner."""
        return self.bottom_right
    
    def find_coordinates(self):
        return [self.find_bl(), self.find_tl(), self.find_tr(), self.find_br()]

    def find_dim(self):
        """Returns the dimension."""
        return self.dim

    def update_dim(self, d):
        """Sets dimension to d."""
        self.dim = d

    def find_intersection(self, line):
        
        b = line.b[0]
        m1 = line.m[0]
        m2 = line.m[1]
        
        ## intersection with bottom side: 
        bl = self.bottom_left[1]
        t_bs = (bl+b)/m2
        pt_bs = (m1*t_bs +b, bl)
        
        ## intersection with top side: 
        t_ts = np.inf
        pt_ts = (np.inf,np.inf)
        
        ## intersection with right side: 
        br= self.find_br()[0]
        t_rs = (br-b)/m1
        pt_rs = (br, m2*t_rs-b)
        
        ## intersection with left side:
        bl = self.bottom_left[0]
        t_ls = (bl-b)/m1
        pt_ls = (bl, m2*t_ls-b)
        
        inter = []
        params = []
        
        if self.bottom_left[0] <= pt_bs[0] <= self.find_br()[0]:
            inter.append(pt_bs)
            params.append(t_bs)
        
        if self.bottom_left[1] <= pt_ls[1]: 
            if pt_ls not in inter: 
                inter.append(pt_ls)
                params.append(t_ls) 
        
        if self.find_br()[1] <= pt_rs[1]:
            if pt_rs not in inter:
                inter.append(pt_rs)
                params.append(t_rs)
      
        return inter, params

    
## Class for rectangles open to the right and the top 
class Infinite_rectangle:
    def __init__(self, bottom_left, dim = 1):
        """bottom_left and top_right are (x,y) coordinate tuples, 
        dim = a non-negative integer representing the dimension of this rectangle."""
        self.bottom_left = bottom_left
        self.bottom_right = np.inf
        self.top_right = np.inf
        self.top_left = np.inf
        self.dim = dim
        
    def __eq__(self, other):
        """Check equality of rectangles. Overrides the default."""
        #### what does this do??
        if self.bottom_left != other.find_bl():
            return False
        if self.dim != other.find_dim():
            return False
        return True
    
    def find_dim(self):
        """Returns the dimension."""
        return self.dim
    
    def find_bl(self):
        """Returns the bottom left corner."""
        return self.bottom_left

    def find_tl(self):
        """Returns the top left corner."""
        return self.top_left

    def find_tr(self):
        """Returns the top right corner."""
        return self.top_right

    def find_br(self):                
        """Returns the bottom right corner."""
        return self.bottom_right
    
    def find_coordinates(self):
        return [self.find_bl(), self.find_tl(), self.find_tr(), self.find_br()]

    def find_dim(self):
        """Returns the dimension."""
        return self.dim

    def update_dim(self, d):
        """Sets dimension to d."""
        self.dim = d


    def find_intersection(self, line):
        """Find the intersection of the given line with self, in the appropriate notation."""
        ## Check that it works properly !!!! 
        b = line.b[0]
        m1 = line.m[0]
        m2 = line.m[1]
        
        ## intersection with bottom side: 
        bl = self.bottom_left[1]
        t_bs = (bl+b)/m2
        pt_bs = (m1*t_bs +b, bl)
       
        ## intersection with top 
        t_ts = np.inf
        pt_ts = (np.inf,np.inf)
        ## intersection with right side: 
        t_rs = np.inf
        pt_rs = (np.inf,np.inf)
        
        ## intersection with left side:
        bl = self.bottom_left[0]
        t_ls = (bl-b)/m1
        pt_ls = (bl, m2*t_ls-b)
        
        inter = []
        params = []
        
        if self.bottom_left[0] <= pt_bs[0]:
            inter.append(pt_bs)
            params.append(t_bs)
        
        if self.bottom_left[1] <= pt_ls[1]: 
            if pt_ls not in inter: 
                inter.append(pt_ls)
                params.append(t_ls) 
       
        return inter, params 
    
#################################################################
# Class for rectangle modules (i.e. direct sums of rectangles).

#### Change so that it also includes infinite rectangles 
class RectangleModule:
    def __init__(self, rect_list):
        self.rectangles = rect_list
         ## add a method to check if  the same rectangle is there several times and change multiplicity

    def add_rectangle(self, rect):
        """Add the given rectangle to the list of rectangles"""
        self.rectangles.append(rect)
        return None

    def trim(self):
        """Trims the list of rectangles to remove duplicates, updating dimensions as necessary."""
        myrects = []
        for r in self.rectangles:
            print('first rect', r)
            for s in myrects:
                print(s)
                if r.eq_upto_dim(s):
                    s.update_dim(s.find_dim() + r.find_dim())
                    break
                myrects = myrects + [r]
        self.rectangles = myrects
        

    def find_dim(self, point):
        """Find the dimension at the given point"""
        d = 0
        for rect in self.rectangles: 
            if rect.bottom_left[0] <= point[0] <= rect.top_right[0] and rect.bottom_left[1] <= point[1] <= rect.top_right[1]:
                d+=rect.dim
        return d
    

    def find_intersection(self, line):
        """Find the intersection of the given line with self, in the appropriate notation."""
        ## finding intersections with all rectangles 
        inter = []
        params= []
        for rect in self.rectangles: 
            pts, t = rect.find_intersection(line)
            inter.append(pts)
            params.append(t)
      
        return inter, params
    
 
    
    def find_critical_pts(self):
        Crit_pts = []
        for ra in self.rectangles:
            bra = ra.find_br()
            bla = ra.find_bl()
            tra = ra.find_tr()
            tla = ra.find_tl()
            Crit_pts.append(bra)
            Crit_pts.append(bla)
            Crit_pts.append(tra)
            Crit_pts.append(bla)
        return list(set(Crit_pts))
        
       
    def compute_barcode(self, line): 
        Int, params = self.find_intersection(line)
        dgm = []
        for rect, i in zip(self.rectangles, range(len(self.rectangles))): 
            dim = rect.dim
            if len(params[i]) ==2: 
                for d in range(dim):
                    dgm.append([params[i][0],params[i][1]])
                     
            elif len(params[i]) ==1:
                for d in range(dim):
                    dgm.append([params[i][0],np.inf])
        return dgm 
    
    def closure_lub(self): 
        """ Find the closure under least upper boud of the critical points"""
        ## Todo: check that it works properly on an example
        ## Not the most efficient way to code this function 
    
        C_bar = self.find_critical_pts()
        l = len(C_bar)
        for i in range(l): 
            p = C_bar[i]
            for j in range(i+1, l): 
                q = C_bar[j]
                if not are_comparable(p,q):
                    lub = (max(p[0],q[0]), max(p[1],q[1]))
                    C_bar.append(lub)

        return list(set(C_bar))

    
################################
# Class for lines in the appropriate notation.
""" !!!Attention!!! this gives an error when the slope of the line is negative in direction (1,-1)
      ---> Change the way to normalize the line 
""" 

class Line_old:
    ## sufficient for b to be just one real number b2 = -b1, for m as well as 0<m<=1 (m,1) or (1,m) .
    def __init__(self,m,b):
        """ Format for 
        m = (m1,m2) direction of the line 
        b=(b1,b2)
        We want max(m1,m2) = 1 and positive slope
        and b1=-b2
        """
        self.positive = True
        self.b = b
        self.m = m 
        if b[0]!= -b[1]: 
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])
            
        maxm = max(abs(m[0]),abs(m[1])) 
        #print(m[0])
        #print(m[1])
        if maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
        if self.m[0] <=0 or self.m[1] <=0:
            self.positive = False
            
class Line:
    ## sufficient for b to be just one real number b2 = -b1, for m as well as 0<m<=1 (m,1) or (1,m) .
    def __init__(self,m,b):
        """ Format for 
        m = (m1,m2) direction of the line 
        b=(b1,b2)
        We want max(m1,m2) = 1 and positive slope
        and b1=-b2
        """
        self.positive = True
        self.b = b
        self.m = m 
        maxm = max(abs(m[0]),abs(m[1])) 
        if maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
        m = self.m    
        if b[0]!= -b[1] and m[0]!=-m[1]:
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])

        if self.m[0] <=0 or self.m[1] <=0:
            self.positive = False

    
    def translate(self,s):
    ## translate a line of direction (m1,m2) in the direction s*(1,-1) 
    ## L: (x,y) = (m1, m2)*t +(b,-b) ---> L': (x,y) = (m1, m2)*t +(b,-b)+s*(1,-1)     
        self.b = (self.b[0]+s, self.b[1]-s)
        return None
    
    def rotate(self, center, theta): 
        ## implement rotation
        s =sin(theta)
        c = cos(theta)
        c1 = center[0]
        c2 = center[1]
        m1 = self.m[0]
        m2 = self.m[1]
        b1 = self.b[0]
        b2 = self.b[1]
        
        m = (c*m1-s*m2 , s*m1+c*m2) 
        b = (c*(b1-c1)-s*(b2-c2)+c1, s*(b1-c1)+ c*(b2-c2)+c2)
        
        if b[0]!= -b[1]: 
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])
            #print(self.b)
        maxm = max(abs(m[0]),abs(m[1])) 
        print(maxm)
        #print(m[0])
        #print(m[1])
        if maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
       
        return None

           
 ## sufficient for b to be just one real number b2 = -b1, for m as well as 0<m<=1 (m,1) or (1,m) . 



################### Extra Functions   ##################


def translate_line(line,s):
    ## translate a line of direction (m1,m2) in the direction s*(1,-1) 
    ## L: (x,y) = (m1, m2)*t +(b,-b) ---> L': (x,y) = (m1, m2)*t +(b,-b)+s*(1,-1) 
    L_tr = Line(line.m,(line.b[0]+s, line.b[1]-s) )
    return L_tr 

def rotate_line(line, center, theta):
       
        s =sin(theta)
        c = cos(theta)
        c1 = center[0]
        c2 = center[1]
        m1 = line.m[0]
        m2 = line.m[1]
        b1 = line.b[0]
        b2 = line.b[1]
        
        m_rot = (c*m1-s*m2 , s*m1+c*m2) 
        b_rot = (c*(b1-c1)-s*(b2-c2)+c1, s*(b1-c1)+ c*(b2-c2)+c2)
        L_rot = Line(m_rot, b_rot)
        
        return L_rot


def compute_bottleneck(M,N,line): 
    dgmM = M.compute_barcode(line)
    dgmN = N.compute_barcode(line) 
    db= gudhi.bottleneck_distance(dgmN,dgmM)
    
    return db


def compute_weighted_bottleneck(M,N,line): 
    dgmM = M.compute_barcode(line)
    dgmN = N.compute_barcode(line) 
    db= gudhi.bottleneck_distance(dgmN,dgmM)
    w = min(line.m) 
    
    return w*db

def line_through_2points(pt1, pt2):
    if pt1[0]<=pt2[0]:
        direction = (pt2[0]-pt1[0], pt2[1]-pt1[1])
        line = Line(direction,pt1) 
    else: 
        direction = (pt1[0]-pt2[0], pt1[1]-pt2[1])
        line = Line(direction,pt2)
    
    return line


def intersect(p1, p2, p3, p4):
    '''function finding the intersections of two line segments [p1,p2] and [p3,p4]'''
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return (x,y)


def are_comparable(p,q): 
    """ function to check whether two points are comparable or not 
    """
    comp = False 
    if p[0] <= q[0] and p[1] <= q[1]: 
        comp = True 
    if p[0] >= q[0] and p[1] >= q[1]: 
        comp = True 
    return comp

#### Intersecting modules 


def intersect_modules(M,N): 
    """ find intersection points of two rectanlge modules"""
    
    return None 



def find_critical_pts_old(self):
        # #method to find intersection points of two rectangles --> gives all the critical poitns of the module
        # #
        # coordinates = []
        # for r in self.rectangles:
        #     coordinates += r.find_coordinates()
        # hull = ConvexHull(coordinates)
        # return hull.vertices
        """method to find intersection points of two rectangles 
        --> gives all the critical points of the module
        """
        
        """ This finds intersection of rectangles, not only the critical points... """
        
        Crit_pts = []
        for ra in self.rectangles:
            ## corners of rectangles, add them to the list of critical points 
            bra = ra.find_br()
            bla = ra.find_bl()
            tra = ra.find_tr()
            tla = ra.find_tl()
            Crit_pts.append(bra)
            Crit_pts.append(bla)
            Crit_pts.append(tra)
            Crit_pts.append(bla)
            ## segments
            ta = [tla, tra]
            ba = [bra,bla]
            la = [bla,tla]
            ra = [bra,tra]
            Seg_a = [ta,ba,la,ra]
            ## fill in all the corners 
            for rb in self.rectangles:
                brb = rb.find_br()
                blb = rb.find_bl()
                trb = rb.find_tr()
                tlb = rb.find_tl()
                tb = [tlb, trb]
                bb = [brb,blb]
                lb = [blb,tlb]
                rb = [brb,trb]
                Seg_b = [tb,bb,lb,rb]
                ## find interections of all semgments
                for p in Seg_a: 
                    for q in Seg_b: 
                        pt = intersect(p[0],p[1],q[0],q[1])
                        if pt != None: 
                            Crit_pts.append(pt)
        return list(set(Crit_pts)) 



        
