#
# This file contains vector classes and functions for various
# vector operations
#
# All of these are pretty simple so I won't bother commenting them
#

import math

class Vector( object ):

    def __init__( self, x=0, y=0, z=0 ):

        self.x = x
        self.y = y
        self.z = z

        # w is required for matrix operations
        self.w = 1


def vector_add( v1, v2 ):

    return Vector( v1.x + v2.x, v1.y + v2.y, v1.z + v2.z );


def vector_sub( v1, v2 ):

    return Vector( v1.x - v2.x, v1.y - v2.y, v1.z - v2.z );


def vector_multi( v, k ):

    return Vector( v.x * k, v.y * k, v.z * k );


def vector_div( v, k ):

    if k != 0:
        return Vector( v.x / k, v.y / k, v.z / k );

    else:
        return 1;


def vector_dot( v1, v2 ):

    return ( v1.x * v2.x + v1.y * v2.y + v1.z * v2.z );


def vector_len( v ):

    return math.sqrt( vector_dot( v, v ) );


def vector_normalise( v ):

    # Normalizes a given vector

    l = vector_len( v )

    try:
        return Vector( v.x / l, v.y / l, v.z / l );
    except ZeroDivisionError:
        return v;


def vector_xprod( v1, v2 ):

    # Cross product

    v = Vector()

    v.x = v1.y * v2.z - v1.z * v2.y
    v.y = v1.z * v2.x - v1.x * v2.z
    v.z = v1.x * v2.y - v1.y * v2.x

    return v;


def vector_intersect( plane_p, plane_n, v_start, v_end ):

    # Intersection

    plane_n = vector_normalise( plane_n )

    plane_d = vector_dot( plane_n, plane_p ) * -1
    ad = vector_dot( v_start, plane_n )
    bd = vector_dot( v_end, plane_n )
    t = ( -plane_d - ad ) / ( bd - ad )

    v_startend = vector_sub( v_end, v_start )
    v_intersect = vector_multi( v_startend, t )

    return vector_add( v_start, v_intersect );



