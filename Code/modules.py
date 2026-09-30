"""Rectangle-decomposable 2-parameter persistence modules and lines of positive slope.

Rectangle and RectangleModule describe the modules, Line a line of positive slope,
critical_val a critical value together with the module it comes from, and
compute_weighted_bottleneck the weighted bottleneck distance between the barcodes of two
modules restricted to a line.
"""
import gudhi
import numpy as np


class Rectangle:
    def __init__(self, top_left,top_right, bottom_left, bottom_right, dim = 1, parent = 1):
        """Corners are (x, y) tuples; a top or right coordinate may be np.inf.

        dim is the multiplicity of the rectangle and parent the module it belongs to
        (0 for M, 1 for N).
        """
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.dim = dim
        self.parent = parent
        if self.top_right[0] < np.inf and self.top_right[1]< np.inf :
            self.type = 'finite'
        elif self.top_left[1] == np.inf and self.top_right[0]< np.inf:
            self.type = 'top infinite'
        elif self.top_right[0] == np.inf and self.top_left[1] < np.inf:
            self.type = 'right infinite'
        else:
            self.type = 'infinite quadrant'

    def __repr__(self):
        return f'(dim is {self.find_dim()}. Parent mod is {self.find_parent()}. \n Coords: \n {self.top_left} __________ {self.top_right} \n           |          | \n           |__________| \n {self.bottom_left}            {self.bottom_right} \n )'

    def __eq__(self, other):
        """Check equality of rectangles. Overrides the default."""
        if self.bottom_left != other.find_bl():
            return False
        if self.top_right != other.find_tr():
            return False
        if self.dim != other.find_dim():
            return False
        return True

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

    def find_dim(self):
        """Returns the dimension."""
        return self.dim

    def find_parent(self):
        """Returns the parent module."""
        return self.parent

    def find_intersection(self, line):
        """Intersection points of the line with the boundary of the rectangle, and their parameters t."""
        b = line.b[0]
        m1 = line.m[0]
        m2 = line.m[1]
        inter = []
        params = []
        EPS = 1e-12  # floating-point tolerance for boundary checks

        if self.type == 'finite':
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

            if self.bottom_left[0] - EPS <= pt_bs[0] <= self.find_br()[0] + EPS:
                inter.append(pt_bs)
                params.append(t_bs)

            if self.bottom_left[1] - EPS <= pt_ls[1] <= self.find_tl()[1] + EPS:
                if pt_ls not in inter:
                    inter.append(pt_ls)
                    params.append(t_ls)

            if self.find_tl()[0] - EPS <= pt_ts[0] <= self.top_right[0] + EPS:
                    inter.append(pt_ts)
                    params.append(t_ts)


            if self.find_br()[1] - EPS <= pt_rs[1] <= self.top_right[1] + EPS:
                if pt_rs not in inter:
                    inter.append(pt_rs)
                    params.append(t_rs)

            if len(params) == 1:
                pt = inter[0]
                t = params[0]
                inter.append(pt)
                params.append(t)

        if self.type == 'top infinite':

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

            if self.bottom_left[0] - EPS <= pt_bs[0] <= self.find_br()[0] + EPS:
                inter.append(pt_bs)
                params.append(t_bs)

            if self.bottom_left[1] - EPS <= pt_ls[1]:
                if pt_ls not in inter:
                    inter.append(pt_ls)
                    params.append(t_ls)

            if self.find_br()[1] - EPS <= pt_rs[1]:
                if pt_rs not in inter:
                    inter.append(pt_rs)
                    params.append(t_rs)

        if self.type == 'right infinite':
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

            if self.bottom_left[0] - EPS <= pt_bs[0]:
                inter.append(pt_bs)
                params.append(t_bs)

            if self.bottom_left[1] - EPS <= pt_ls[1] <= self.find_tl()[1] + EPS:
                if pt_ls not in inter:
                    inter.append(pt_ls)
                    params.append(t_ls)

            if self.find_tl()[0] - EPS <= pt_ts[0]:
                inter.append(pt_ts)
                params.append(t_ts)


        if self.type == 'infinite quadrant':
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

            if self.bottom_left[0] - EPS <= pt_bs[0]:
                inter.append(pt_bs)
                params.append(t_bs)

            if self.bottom_left[1] - EPS <= pt_ls[1]:
                if pt_ls not in inter:
                    inter.append(pt_ls)
                    params.append(t_ls)

        return inter, params


#################################################################

class RectangleModule:
    """A direct sum of rectangles."""

    def __init__(self, rect_list):
        self.rectangles = rect_list

    def find_dim(self, point):
        """Find the dimension at the given point"""
        d = 0
        for rect in self.rectangles:
            if rect.bottom_left[0] <= point[0] <= rect.top_right[0] and rect.bottom_left[1] <= point[1] <= rect.top_right[1]:
                d+=rect.dim
        return d


    def find_intersection(self, line):
        """Intersections of the line with each rectangle, as lists (see Rectangle.find_intersection)."""
        inter = []
        params= []
        for rect in self.rectangles:
            pts, t = rect.find_intersection(line)
            inter.append(pts)
            params.append(t)

        return inter, params



    def find_critical_pts(self):

        """The finite corners of all rectangles."""
        Crit_pts = []
        for r in self.rectangles:
            ## add bottom left (always finite)
            Crit_pts.append(r.find_bl())

            ## add top left value if finite
            tl = r.find_tl()
            if tl[1] < np.inf:
                Crit_pts.append(tl)

            # add top right value if finite
            tr = r.find_tr()
            if tr[0]<np.inf and tr[1]< np.inf:
                Crit_pts.append(tr)

            ## add bottom right if finite
            br = r.find_br()
            if br[0] < np.inf:
                Crit_pts.append(br)

        return list(set(Crit_pts))


    def compute_barcode(self, line):
        """Barcode of the module restricted to the line, in the line parameter t."""
        Int, params = self.find_intersection(line)
        dgm = []
        for rect, i in zip(self.rectangles, range(len(self.rectangles))):
            dim = rect.dim
            if len(params[i]) >= 2:
                for d in range(dim):
                    dgm.append([min(params[i]), max(params[i])])

            elif len(params[i]) ==1:
                for d in range(dim):
                    dgm.append([params[i][0],np.inf])
        return dgm

    def closure_lub(self):
        """The critical values together with the least upper bound of every incomparable pair."""
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

class Line:
    """A line L(t) = m t + b in the plane.

    The direction m = (m1, m2) is scaled so that max(|m1|, |m2|) = 1, and b is moved
    along the line to the point with b1 = -b2 (the anti-diagonal). positive is False
    when the line does not have positive slope.
    """

    def __init__(self,m,b):
        self.positive = True
        self.b = b
        self.m = m
        maxm = max(abs(m[0]),abs(m[1]))
        if maxm == 0:
            self.positive = False

        elif maxm !=1:
            self.m = (m[0]/maxm,m[1]/maxm)
        m = self.m
        if b[0]!= -b[1] and m[0]!=-m[1]:
            self.b =(-m[0] *(b[0]+b[1])/(m[0]+m[1]) +b[0],m[0]*(b[0]+b[1])/(m[0]+m[1]) -b[0])

        if self.m[0] <=0 or self.m[1] <=0:
            self.positive = False


################################

def compute_weighted_bottleneck(M,N,line):
    """Weighted bottleneck distance of M and N along the line: min(m1, m2) times the bottleneck distance."""
    dgmM = M.compute_barcode(line)
    dgmN = N.compute_barcode(line)
    db= gudhi.bottleneck_distance(dgmN,dgmM)
    w = min(line.m)

    return w*db

def line_through_2points(pt1, pt2):
    """The Line through two points, directed from the one with the smaller first coordinate."""
    if pt1[0]<=pt2[0]:
        direction = (pt2[0]-pt1[0], pt2[1]-pt1[1])
        line = Line(direction,pt1)
    else:
        direction = (pt1[0]-pt2[0], pt1[1]-pt2[1])
        line = Line(direction,pt2)

    return line


def are_comparable(p,q):
    """True if p <= q or q <= p componentwise."""
    comp = False
    if p[0] <= q[0] and p[1] <= q[1]:
        comp = True
    if p[0] >= q[0] and p[1] >= q[1]:
        comp = True
    return comp

class critical_val:
    """A critical value: coordinates and the module it comes from (0 for M, 1 for N).

    A point that is a critical value of both modules is represented by two objects.
    Equality is identity, so a repeated point in a quadruple is the same object twice.
    """

    def __init__(self, coords, parent_module):
        self.parent_module = parent_module
        self.coords = coords

    def __repr__(self):
        return f'(parent module of {self.find_coords()} is {self.find_parent_mod()})'

    def find_parent_mod(self):
        return self.parent_module

    def find_coords(self):
        return self.coords

