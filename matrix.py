import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices larger than 2x2.")
        
        if self.h==1:
            return self[0]
        
        if self.h==2:
            return (self[0][0]*self[1][1]-self[0][1]*self[1][0])

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        
        trace = 0
        for i in range(self.w):
            trace=self[i][i]+trace
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        if self.h==1:
            self[0][0]=1/(self[0][0])
            return self
        return (1/self.determinant()) * (self.trace() * identity(self.h) - self)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        trans_matrix=zeroes(self.w,self.h)
        
        for i in range(self.w):
            for j in range(self.h):
                trans_matrix[i][j]=self[j][i]
        return trans_matrix

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        add_matrix=zeroes(self.w,self.h)
        
        for i in range(self.h):
            for j in range(self.w):
                add_matrix[i][j] = self[i][j]+other[i][j]
        return add_matrix
    
        return Matrix([[self.g[j][i] + other.g[j][i] for j in range(0, self.h)] for i in range(0, self.w)])

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
             #   add_matrix=zeroes(self.w,self.h)
        neg_matrix=zeroes(self.w,self.h)
        
        for i in range(self.h):
            for j in range(self.w):
                neg_matrix[i][j]=(self[i][j])*(-1)
        return neg_matrix

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        sub_matrix=zeroes(self.w,self.h)
        
        for i in range(self.h):
            for j in range(self.w):
                sub_matrix[i][j] = self[i][j]-other[i][j]
        return sub_matrix

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if self.w != other.h:
            raise(ValueError, "Matrices can only be multiplied if the number of columns of 1st matrix is equal to the number \
                  of rows of the second matrix") 
        
        mul_matrix=zeroes(self.h,other.w)
        otherT=other.T()
        
        for i in range(self.h):
            for j in range(other.w):
                for k in range(self.w):
                    mul_matrix[i][j]=self[i][k]*otherT[j][k]+mul_matrix[i][j]
        
        return mul_matrix
        # TODO - your code here
        #

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        rmul_matrix=zeroes(self.w,self.h)
        if isinstance(other, numbers.Number):
            for i in range (self.w):
                for j in range (self.h):
                        rmul_matrix[i][j]=other*self[i][j]
            return rmul_matrix