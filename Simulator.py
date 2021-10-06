from Poisson import Poisson
import DiscPrms as dsc 
import FEM
import math
import sys
from RHS import polynomialRHS
from BC import constBC

# Derived class to implement the right hand side  
# and boundary conditions for FDM
class PoissonSub(Poisson):

    def __init__(self, nno_x, nno_y, xmax, ymax, xmin, ymin, no_plot=False):
        super().__init__(nno_x, nno_y, xmax, ymax, xmin, ymin, no_plot)
        self.bc = constBC()
        self.rhs = polynomialRHS()

    # Used for simulators wanting the nodal values of the solution
    def nodeValues(self):
        return self.solu
        

# Derived class to implement the right hand side  
# and boundary conditions for FEM solution
class FEMPoissonSub(FEM.PoissonFEM):

    def __init__(self, params_, grid_):
        super().__init__(params_, grid_)
        self.bc = constBC()
        self.rhs = polynomialRHS()

    # Used for simulators wanting the nodal values of the solution
    def nodeValues(self):
        return self.grid.interpolSolution()


# Parses a float from a string
def string2float(str):

    sign = 1
    lst = str.split('.')
    if len(lst) > 2:
        print("string2float: Error, ", str, " is not a valid floating point value")
        return 0.0

    if str[0] == '-':
        sign = -1
        str = str[1:]

    if len(lst) == 1:
        if str.isnumeric():
            return sign*float(str)

    if len(lst) == 2:
        if str.isnumeric() and lst[1].isnumeric():
            return sign*float(str)

    print(" S2F 2: Error, ", str, " is not a valid number ")
    return 0.0

def parse_rhs(arg, coeff):
    """ Parses information on the right hand side of the Poisson eq. 

    Args:
        arg (string): Specifies the degree of the (polynomial) right hand side 
        coeff (string): Polynom coefficients separated by a comma 

    Returns:
        list: Right hand side coefficients
    """    
    a = []
    lst = coeff.split(',')

    if arg == 'Constant':
        if len(lst) != 1:
            return []
        a.append(string2float(lst[0]))
        return a
    elif arg == 'Linear':
        if len(lst) != 3:
            print("Coefficient string is incorrect for linear rhs ", coeff)
            return []

        for i in range(3):
            a.append(string2float(lst[i].strip()))
        return a
    elif arg == 'Quadratic':
        if len(lst) != 6:
            print("Coefficient string is incorrect for quadratic rhs ", coeff)
            return []

        for i in range(6):
            a.append(string2float(lst[i].strip()))
        return a
    else:
        return []


def parse_bc(arg):
    """ Parses the (constant) boundary conditions

    Args:
        arg (dictionary): Contains the BC values at each boundary

    Returns:
        list: Boundary conditions at each boundary, in the order defined for the
        boundary indices
    """    
    a = []
    a.append(string2float(arg['bcright'].strip()))
    a.append(string2float(arg['bcupp'].strip()))
    a.append(string2float(arg['bcleft'].strip()))
    a.append(string2float(arg['bclow'].strip()))
  
    return a


def parse_domain(arg):
    temp = arg.strip()
    if temp[0] != '[':
        print("Invalid domain :", temp)
        return ()

    temp = temp[1:]
    pos = temp.find(',')
    x_min = string2float(temp[:pos].strip())
    temp = temp[(pos+1):]
    
    pos = temp.find(']')
    x_max = string2float(temp[:pos].strip())
       
    pos = temp.find('x')
    temp = temp[pos+1:].strip()  

    if temp[0] != '[':
        print("Invalid domain :", temp)
        return ()

    temp = temp[1:]
    pos = temp.find(',')
    y_min = string2float(temp[:pos])
    temp = temp[(pos+1):]
 
    pos = temp.find(']')
    y_max = string2float(temp[:pos].strip())

    return (x_min, x_max, y_min, y_max)



def run(mylist, no_plot=True):

    print("Simulator started \n")
    
    # Put input into dictionary to reuse old code
    values = {}
    
    for inp in mylist:
        tmp = inp.split(':')
        values[tmp[0]] = tmp[1]

    
    (x_min, x_max, y_min, y_max) = parse_domain(values['Domain'])

    nnos = values['Number of nodes']
    if not nnos.isnumeric():
        print("Number of nodes is not an integer")
        nno = 900
    else:
        nno = int(nnos)

    sol_met = values['Method of solution']
    if (not sol_met):
        sol_met = 'FDM'

    # for now, assume a  box
    lx = (x_max - x_min)
    ly = (y_max - y_min)        
    nno_x = int((nno*lx/ly)**0.5) 
    nno_y = int(nno/nno_x)

    if sol_met == 'FEM':
        print("Creating FEM solver \n")
        print("NOTE: There is  bug in the FEM solver. \n Works if rhs=0")
        print("Boundary conditions are incorrectly incorporated")


        if ((not math.isclose(x_min,0.0)) or (not math.isclose(x_max,1.0)) or (not math.isclose(y_min, 0.0)) or (not math.isclose(y_max, 1.0))):
            return -1

        parameters = dsc.DiscPrms(nnx=nno_x, nny=nno_y, dt=1000, x_max=x_max, y_max=y_max, t_max=2000, x_min=x_min, y_min=y_min)
        grid = dsc.Grid2d(parameters)
        # For now, assume only Dirichlet BC's 
        boind_list = [1,2,3,4]
        grid.setBoindWithEssBC(boind_list)                
        sim = FEMPoissonSub(parameters, grid)
        
        rhs_val = parse_rhs(values['Right hand side'], values['rhs_coeff'].strip())

        if ((len(rhs_val) != 1) or (rhs_val[0] != 0) ):
            return -1

        sim.rhs.attachRHS(parse_rhs(values['Right hand side'], values['rhs_coeff'].strip()))                
        sim.bc.attachBC(parse_bc(values))
        
        if not sim.rhs.rhs:
            print("Illegal right hand side ", sim.rhs.rhs)
                
        sim.solve(-1)
        if (no_plot):
           return sim.nodeValues()
        else:
            return 0
    
    else: # Finite differences
        print("Creating FDM solver \n")
        sim = PoissonSub(nno_x, nno_y, x_max, y_max, x_min, y_min, no_plot)
        sim.rhs.attachRHS(parse_rhs(values['Right hand side'], values['rhs_coeff'].strip()))
        sim.bc.attachBC(parse_bc(values))

        if not sim.rhs.rhs:
            print("Illegal right hand side ", sim.rhs.rhs)

        sim.solve()
        if (no_plot):
            return sim.nodeValues()
        else:    
            return 0

# Will probably never be used
if __name__ == '__main__':
    run(sys.argv)
