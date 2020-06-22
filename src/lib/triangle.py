#
# This file contains a triangle class and functions for
# triangle operations required for the engine to work
#

from .matrix import *
from .vector import *

class Triangle( object ):

    def __init__( self, v0=Vector(0,0,0), v1=Vector(0,0,0), v2=Vector(0,0,0) ):

        # Points of the triangle
        self.pts = [ v0, v1, v2 ]

        # Color
        self.cl = (( 0, 0, 0 ))


def tri_dist( p, pn, pp ):

    # Returns a distance from a point p to
    # plane

    v = Vector( p.x, p.y, p.z )
    v = vector_normalise( v )

    return ( pn.x * p.x + pn.y * p.y + pn.z * p.z - vector_dot( pn, pp ) );


def tri_getnormal( t ):

    # Calculates the normal vector of the triangle t
    # Returns a normalized float of the normal

    norm = Vector( 0, 0, 0 )
    temp_v1 = Vector( 0, 0, 0 )
    temp_v2 = Vector( 0, 0, 0 )

    temp_v1.x = t.pts[1].x - t.pts[0].x
    temp_v1.y = t.pts[1].y - t.pts[0].y
    temp_v1.z = t.pts[1].z - t.pts[0].z

    temp_v2.x = t.pts[2].x - t.pts[0].x
    temp_v2.y = t.pts[2].y - t.pts[0].y
    temp_v2.z = t.pts[2].z - t.pts[0].z

    norm.x = temp_v1.y * temp_v2.z - temp_v1.z * temp_v2.y
    norm.y = temp_v1.z * temp_v2.x - temp_v1.x * temp_v2.z
    norm.z = temp_v1.x * temp_v2.y - temp_v1.y * temp_v2.x

    norm = vector_normalise( norm )

    return norm;


def tri_calcvis( v1, v2, p ):

    # Determine the visibility of an object

    op_x = ( v1.x * ( p.pts[1].x - v2.x ) )
    op_y = ( v1.y * ( p.pts[1].y - v2.y ) )
    op_z = ( v1.z * ( p.pts[1].z - v2.z ) )

    val = ( op_x + op_y + op_z )
    return val;


def tri_shade( dp ):

    # Set the shade of a surface
    # dp - dot product of a lighting vector and
    # the surface's normal

    s = int( dp * 200 )
    s = abs( s )

    return (( s, s, s ));


def tri_clipplane( plane_p, plane_n, t_in ):

    # The clipping function
    # Checks if a triangle intersects with a given plane
    # and does_stuff() based on the result

    plane_n = vector_normalise( plane_n )
    dp = vector_dot( plane_n, plane_p )

    # Lists of points inside (that should be rendered) and
    # outside (that should not)
    pts_in = list()
    pts_out = list()

    d0 = tri_dist( t_in.pts[0], plane_n, plane_p )
    d1 = tri_dist( t_in.pts[1], plane_n, plane_p )
    d2 = tri_dist( t_in.pts[2], plane_n, plane_p )

    d_list = [ d0, d1, d2 ]

    for i, d in enumerate( d_list ):

        if d >=0:
            pts_in.append( t_in.pts[i] )

        else:
            pts_out.append( t_in.pts[i] )

    n_in = len( pts_in )
    n_out = len( pts_out )

    # do_stuff() based on how many points of the
    # triangle are in vision

    # The entire triangle is in vision
    elif n_in == 3:

        t_out1 = t_in
        return [ t_out1 ];

    # Two points are in vision and one is out
    elif n_in == 2 and n_out == 1:

        # The shape that's in vision is a quad so make two new triangles
        # to form it
        t_out1 = Triangle()
        t_out2 = Triangle()

        t_out1.cl = t_in.cl
        t_out2.cl = t_in.cl

        t_out1.pts[0] = pts_in[0]
        t_out1.pts[1] = pts_in[1]
        t_out1.pts[2] = vector_intersect( plane_p, plane_n, pts_in[0], pts_out[0] )

        t_out2.pts[0] = pts_in[1]
        t_out2.pts[1] = t_out1.pts[2]
        t_out2.pts[2] = vector_intersect( plane_p, plane_n, pts_in[1], pts_out[0] )

        return [ t_out1, t_out2 ];

    # One point is in vision and two are out
    elif n_in == 1 and n_out == 2:

        # Keep the point that's inside vision radius
        t_out1 = Triangle()
        t_out1.cl = t_in.cl
        t_out1.pts[0] = pts_in[0]

        # ... and make a new triangle from the points outside of vision radius
        t_out1.pts[1] = vector_intersect( plane_p, plane_n, pts_in[0], pts_out[0] )
        t_out1.pts[2] = vector_intersect( plane_p, plane_n, pts_in[0], pts_out[1] )

        return [ t_out1 ];

    # The entire triangle is outside of vision
    if n_in == 0:

        return 0;


def tri_getz( t ):

    # Returns the approximate z position of a triangle
    # Used for sorting

    return ( ( t.pts[0].z + t.pts[1].z + t.pts[2].z ) / 3 );



