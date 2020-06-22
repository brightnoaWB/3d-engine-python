#
# This file contains a class for 4x4 matrices and
# function for various matrix operations
#

from .vector import *
import math

class Matrix( object ):

    # A 4x4 matrix populated with 0s

    def __init__( self ):

        mat = list()

        for x in range( 4 ):
            holder = list()

            for y in range( 4 ):
                holder.append( 0 )

            mat.append( holder )

        self.mat = mat


def matrix_makeproj( fov, asp, near, far ):

    # Creates a projection matrix based off of
    # field of view     fov
    # aspect ratio      asp
    # cutoff points     near, far
    # fov is in RAD as opposed to DEG

    m = Matrix()

    m.mat[0][0] = asp * fov
    m.mat[1][1] = fov
    m.mat[2][2] = far / ( far - near )
    m.mat[2][3] = 1
    m.mat[3][2] = ( -far * near ) / ( far - near )

    return m;


def matrix_makeidentity():

    # Creates and identity matrix

    m = Matrix()

    m.mat[0][0] = 1;
    m.mat[1][1] = 1;
    m.mat[2][2] = 1;
    m.mat[3][3] = 1;

    return m;


def matrix_makexrot( ang ):

    # Creates a rotation matrix for
    # rotating around X axis
    # ang is in RAD

    m = Matrix()

    m.mat[0][0] = 1
    m.mat[1][1] = math.cos( ang )
    m.mat[1][2] = math.sin( ang )
    m.mat[2][1] = math.sin( ang ) * -1
    m.mat[2][2] = math.cos( ang )
    m.mat[3][3] = 1

    return m;


def matrix_makeyrot( ang ):

    # Same as above but Y axis instead
    # ang is in RAD

    m = Matrix()

    m.mat[0][0] = math.cos( ang )
    m.mat[0][2] = math.sin( ang )
    m.mat[2][0] = math.sin( ang ) * -1
    m.mat[1][1] = 1
    m.mat[2][2] = math.cos( ang )
    m.mat[3][3] = 1

    return m;


def matrix_makezrot( ang ):

    # Same as above but for Z axis
    # ang is in RAD

    m = Matrix()

    m.mat[0][0] = math.cos( ang )
    m.mat[0][1] = math.sin( ang )
    m.mat[1][0] = math.sin( ang ) * -1
    m.mat[1][1] = math.cos( ang )
    m.mat[2][2] = 1
    m.mat[3][3] = 1

    return m;


def matrix_maketrans( x, y, z ):

    # Returns a translation matrix

    m = Matrix()

    m.mat[0][0] = 1
    m.mat[1][1] = 1
    m.mat[2][2] = 1
    m.mat[3][0] = x
    m.mat[3][1] = y
    m.mat[3][2] = z
    m.mat[3][3] = 1

    return m;


def matrix_multimv( v, m ):

    # matrix multiplication with a vector
    # v - vector
    # m - matrix

    x = v.x * m.mat[0][0] + v.y * m.mat[1][0] + v.z * m.mat[2][0] + m.mat[3][0]
    y = v.x * m.mat[0][1] + v.y * m.mat[1][1] + v.z * m.mat[2][1] + m.mat[3][1]
    z = v.x * m.mat[0][2] + v.y * m.mat[1][2] + v.z * m.mat[2][2] + m.mat[3][2]
    w = v.x * m.mat[0][3] + v.y * m.mat[1][3] + v.z * m.mat[2][3] + m.mat[3][3]

    vect = Vector( x, y, z )
    vect.w = w

    return vect;


def matrix_multimm( m1, m2 ):

    # matrix multiplication with another matrix

    m = Matrix()

    for y in range( 4 ):
        for x in range( 4 ):
            m.mat[x][y] =   m1.mat[x][0] * m2.mat[0][y] +   \
                            m1.mat[x][1] * m2.mat[1][y] +   \
                            m1.mat[x][2] * m2.mat[2][y] +   \
                            m1.mat[x][3] * m2.mat[3][y]

    return m;


def matrix_point( pos, targ, up ):

    # "Points" the matrix toward a target (targ)

    # Current forward direction
    c_forw = vector_sub( targ, pos )
    c_forw = vector_normalise( c_forw )

    # Current up direction
    v_temp = vector_multi( c_forw, vector_dot( up, c_forw ) )

    c_up = vector_sub( up, v_temp )
    c_up = vector_normalise( c_up )

    # Current right dir
    c_right = vector_xprod( c_up, c_forw )

    # Make the matrix
    m = Matrix()

    m.mat[0][0] = c_right.x
    m.mat[0][1] = c_right.y
    m.mat[0][2] = c_right.z
    m.mat[0][3] = 0

    m.mat[1][0] = c_up.x
    m.mat[1][1] = c_up.y
    m.mat[1][2] = c_up.z
    m.mat[1][3] = 0

    m.mat[2][0] = c_forw.x
    m.mat[2][1] = c_forw.y
    m.mat[2][2] = c_forw.z
    m.mat[2][3] = 0

    m.mat[3][0] = pos.x
    m.mat[3][1] = pos.y
    m.mat[3][2] = pos.z
    m.mat[3][3] = 1

    return m;


def matrix_invert( m ):

    # Inverts a given matrix

    inv = Matrix()

    inv.mat[0][0] = m.mat[0][0]
    inv.mat[0][1] = m.mat[1][0]
    inv.mat[0][2] = m.mat[2][0]
    inv.mat[0][3] = 0

    inv.mat[1][0] = m.mat[0][1]
    inv.mat[1][1] = m.mat[1][1]
    inv.mat[1][2] = m.mat[2][1]
    inv.mat[1][3] = 0

    inv.mat[2][0] = m.mat[0][2]
    inv.mat[2][1] = m.mat[1][2]
    inv.mat[2][2] = m.mat[2][2]
    inv.mat[2][3] = 0

    inv.mat[3][0] = -(m.mat[3][0] * inv.mat[0][0] + m.mat[3][1] * inv.mat[1][0] + m.mat[3][2] * inv.mat[2][0])
    inv.mat[3][1] = -(m.mat[3][0] * inv.mat[0][1] + m.mat[3][1] * inv.mat[1][1] + m.mat[3][2] * inv.mat[2][1])
    inv.mat[3][2] = -(m.mat[3][0] * inv.mat[0][2] + m.mat[3][1] * inv.mat[1][2] + m.mat[3][2] * inv.mat[2][2])

    inv.mat[3][3] = 1

    return inv;


