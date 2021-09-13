import gudhi

# Class for single rectangles.
class Rectangle:
    def __init__(self, bottom_left, top_right, dim):
        # bottom_left and top_right are (x,y) coordinate tuples, and dim is a non-negative integer representing the dimension of this rectangle.
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.dim = dim

    def find_bl(self):
        """Returns the bottom left corner."""
        return None

    def find_tl(self):
        """Returns the top left corner."""
        return None

    def find_tr(self):
        """Returns the top right corner."""
        return None

    def find_br(self):                
        """Returns the bottom right corner."""
        return None


# Class for rectangle modules (i.e. direct sums of rectangles).
class RectangleModule:
    def __init__(self, rect_list):
        self.rectangles = rect_list

    def add_rectangle(self, rect):
        """Add the given rectangle to the list of rectangles"""
        return None

    def find_dim(self, point):
        """Find the dimension at the given point"""
        return None

    def find_intersection(self, line):
        """Find the intersection of the given line with self, in the appropriate notation."""
        return None

# Class for lines in the appropriate notation.
class Line:
    # Unimplemented
    def __init__(self):
        
