import gudhi
from math import cos, sin, pi
import modules 

def Eq_classes(C_bar):
    """
    Code to find the equivalences of lines passing through none of the critical points 

    """
    
    #return Eq_classes
    return None



def Eq_classes_through_1pt(C_bar): 
    """ Function to find all the equivalences classes of lines through 
        a single point in the set C_bar
    """
    return None



def Find_line_eq_classes(M):
    """" 
    Function to find all the equivalence classes of lines of a persistence module
    
    """
    C_bar = M.closure_lub()
    
    
    ## find representative lines through none of the critical points 
    Eq_classes(C_bar)
    ## find all positive lines through 1 critical point
    Eq_classes_through_1pt(C_bar)
    ## find all positive lines through 2 critical points 
    ## implement this 
    

    return None 
    
    

