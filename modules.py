import gudhi

# Class for single rectangles.
class Rectangle:
    def __init__(self, bottom_left, top_right, dim):
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

# Class for rectangle modules (i.e. direct sums of rectangles).
class RectangleModule:
    def __init__(self, rect_list):
        self.rectangles = rect_list

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
        return None

# Class for lines in the appropriate notation.
class Line:
    # Unimplemented
    def __init__(self,m,b):
        self.m = m 
        self.b = b
        ## check right format for m and b 
        
