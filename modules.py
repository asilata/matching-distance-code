import gudhi

# Class for single rectangles.
class Rectangle:
    def __init__(self, bottom_left, top_right, dim ):
        # bottom_left and top_right are (x,y) coordinate tuples, and dim is a non-negative integer representing the dimension of this rectangle.
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
            
        if self.find_tl()[0] <= pt_ts[0] <= self.top_right[0]: 
            if pt_ts not in inter: 
                inter.append(pt_ts)
                params.append(t_ts)
              
        if self.bottom_left[1] <= pt_ls[1] <= self.find_tl()[1]: 
            if pt_ls not in inter: 
                inter.append(pt_ls)
                params.append(t_ls) 
        if self.find_br()[1] <= pt_rs[1] <= self.top_right[1]: 
            if pt_rs not in inter:
                inter.append(pt_rs)
                params.append(t_rs)
      
        return inter, params

# Class for rectangle modules (i.e. direct sums of rectangles).
class RectangleModule:
    def __init__(self, rect_list):
        self.rectangles = rect_list
         ## add a method to check if  the same rectangle is there several times and change mul

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
        #method to find intersection points of two rectangles --> gives all the critical poitns of the module
        #
        return None 

    def compute_barcode(self, line): 
        Int, params = self.find_intersection(line)
        dgm = []
        for rect, i in zip(self.rectangles, range(len(self.rectangles))): 
            dim = rect.dim
            if len(params[i]) ==2: 
                for d in range(dim):
                    dgm.append([params[i][0],params[i][1]])
        return dgm 

# Class for lines in the appropriate notation.
class Line:
    # Unimplemented
    ## sufficient for b to be just one real number b2 = -b1, for m as well as 0<m<=1 (m,1) or (1,m) .
    def __init__(self,m,b):
        """ Format for 
        m = (m1,m2) direction of the line 
        b=(b1,b2)
        We want max(m1,m2) = 1 and positive slope
        and b1=-b2
        """
        self.b = b
        self.m = m 
        if b[0]!= -b[1]: 
            
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])
            #print(self.b)
        maxm = max(m[0],m[1]) 
        #print(m[0])
        #print(m[1])
        if maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
    
    
    def translate(self,s):
    ## translate a line of direction (m1,m2) in the direction s*(1,-1) 
    ## L: (x,y) = (m1, m2)*t +(b,-b) ---> L': (x,y) = (m1, m2)*t +(b,-b)+s*(1,-1)     
        self.b = (self.b[0]+s, self.b[1]-s)
        return None
    
    def rotate(self, theta): 
        ## implement rotation
        return None

           
 ## sufficient for b to be just one real number b2 = -b1, for m as well as 0<m<=1 (m,1) or (1,m) . 



###################  Functions   ##################


def translate_line(line,s):
    ## translate a line of direction (m1,m2) in the direction s*(1,-1) 
    ## L: (x,y) = (m1, m2)*t +(b,-b) ---> L': (x,y) = (m1, m2)*t +(b,-b)+s*(1,-1) 
    L_tr = Line(line.m,(line.b[0]+s, line.b[1]-s) )
    return L_tr 

def rotate_line(line, theta): 
        ## implement rotation to get a new line 
        return None


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


#### plotting function for lines and modules 











        
