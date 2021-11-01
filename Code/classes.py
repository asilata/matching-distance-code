import gudhi
import csv

class Complex:
  def __init__(self, simplices_list, ordered_simplices, simplex_tree):
    # here we initialize everything. if defining an attribute with a function, must init func first.
    self.simplices = simplices_list
    self.critical_simplices = 0
    self.find_maxx()
    self.top_dim = self.find_maxx()
    self.st = simplex_tree
    self.num_verts = 0
    self.num_edges = 0
    self.num_triangles = 0
        
  def print_all_simplices(self):
    for s in self.simplices:
      print("boundary:",s.boundary,"critical?", s.criticality, "in dgvf", s.in_dgvf)
       
  def find_maxx(self):
    maxx = 0
    for s in self.simplices:
      if len(s.boundary) > maxx:
        maxx = (len(s.boundary))
    maxx = maxx - 1
    return maxx
    
  def print_num_i_simplices(self, dim):
  # prints the number of i-dimensional simplices in given complex
    st = self.st
    if dim > self.top_dim:
        print("Error! input dimension exceeds bounds")
    elif dim < 0:
        print("Error! input dimension less than zero")
    print("given dim is ", dim, " top dim is ", self.top_dim)
    simps_sum = 0
    i_simps = len(list(st.get_skeleton(dim)))
    i = 1
    for x in reversed(range(dim)):
    # range(dim) goes from 0 to dim-1; this reverses the order to end at 0
      i_simps = i_simps - (i) * len(list(st.get_skeleton(x)))
      if i == 1:
            i = 0
      else:
        i = 1
    print("number of",dim,"-simplices is ", i_simps)


class Simplex: 
  def __init__(self):
    # here we initialize everything. if defining an attribute with a function, must init func first.
    self.is_critical()
    self.criticality = self.is_critical()
    self.entrancevals = [-1.0, -1.0]
    self.boundary = [-2]
    self.init_index = -1
    self.paired_with = [-1]
    self.in_dgvf = 'X'

    
  def is_critical(self):
    critical = False
    return critical
    