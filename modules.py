import gudhi
from math import cos, sin, pi

"""TODO: 
    - implement algorithm to find all equivalence classes of a given module
    - function to plot easily a module and some lines though the parameter space
    - include "infinite rectangles", ie, open at the top and/or to the right 
"""

# Class for single rectangles.
class Rectangle:
    def __init__(self, bottom_left, top_right, dim ):
        """bottom_left and top_right are (x,y) coordinate tuples, 
        dim = a non-negative integer representing the dimension of this rectangle."""
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.dim = dim
        #add error message when format is not good
        
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
    
    def find_intersection(self, line):
        """Find the intersection of the given line with self, in the appropriate notation."""
        ## finding intersections of this rectangle and a given line
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
    
#################################################################
# Class for rectangle modules (i.e. direct sums of rectangles).
class RectangleModule:
    def __init__(self, rect_list):
        self.rectangles = rect_list
         ## add a method to check if  the same rectangle is there several times and change multiplicity

    def add_rectangle(self, rect):
        """Add the given rectangle to the list of rectangles"""
        self.rectangles.append(rect)
        return None

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
        """method to find intersection points of two rectangles 
        --> gives all the critical points of the module
        """
        
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
    

    def compute_barcode(self, line): 
        Int, params = self.find_intersection(line)
        dgm = []
        for rect, i in zip(self.rectangles, range(len(self.rectangles))): 
            dim = rect.dim
            if len(params[i]) ==2: 
                for d in range(dim):
                    dgm.append([params[i][0],params[i][1]])
        return dgm 
    
    def closure_lub(self): 
        """ Find the closure under least upper boud of the critical points"""
        """REMARK: finding the closure under least upper bound is very similar to 
        finding all the intersection points of rectangles in the modules but it finds extra points """ 
        
        return None
    
################################
# Class for lines in the appropriate notation.
""" !!!Attention!!! this gives an error when the slope of the line is negative in direction (1,-1)
      ---> Change the way to normalize the line 
""" 
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
        if b[0]!= -b[1]: 
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])
            
        maxm = max(abs(m[0]),abs(m[1])) 
        #print(m[0])
        #print(m[1])
        if maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
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
    
    direction = (pt2[0]-pt1[0], pt2[1]-pt1[1])
    line = Line(direction,pt1) 
    
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

def intersect_modules(M,N): 
    """ find intersection points of two rectanlge modules"""
    
    return None 

#### plotting function for lines and modules 



        
