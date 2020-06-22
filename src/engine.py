import pygame
from pygame.locals import *

import os
import math
import sys

from lib.matrix import *
from lib.triangle import *
from lib.vector import *


### Optional settings
### change how you see fit

# Field of view
FOV = 90

# Framerate
FPS = 60

# Window width, height
WIN_WIDTH = 600
WIN_HEIGHT = 360


## pygame vars
pygame.init()

# window settings
SCREEN = pygame.display.set_mode(( WIN_WIDTH, WIN_HEIGHT ))
pygame.display.set_caption( "Simple 3d Engine" )

# framerate settings
CLOCK = pygame.time.Clock()

# projection
ASPECT_RATIO = WIN_HEIGHT / WIN_WIDTH
FOV_RAD = math.radians( FOV )
F_NEAR = 10
F_FAR = 1000

z_max = 0


class Mesh( object ):

    def __init__( self ):

        # The triangles of the mesh
        self.t = list()


def mesh_loadmodel( fname ):

    # Converts and .obj file into a mesh

    file = open( fname )
    vect_cache = list()
    mesh = Mesh()

    # z_max is used for translating the model later
    global z_max

    for line in file:

        # Get the individual components
        s = line.split()

        # Avoid IndexError
        if len( s ) > 0:

            # If line describes a vertex
            if s[0] == "v":

                v = Vector()

                # Clean up the occasional E operand
                # Most of the time this won't need to execute but hey
                for i in range( len( s ) ):

                    e_buffer = s[i].split( "E" )

                    # If there is an E operand
                    if len( e_buffer ) > 1:

                        # Check if there's a + or a -
                        if e_buffer[1][0] == "+":

                            # Separate into magnitude and exponent
                            e_buffer[1] = e_buffer[1][ 1: ]

                            # Typecasting because fuck my life
                            e_buffer[0] = float( e_buffer[0] )
                            e_buffer[1] = float( e_buffer[1] )

                            s[i] = e_buffer[0] * ( 10 ** e_buffer[1] )

                        # Negative exponent
                        elif e_buffer[1][0] == "-":
                            e_buffer[1] = e_buffer[1][ 1: ]
                            e_buffer[0] = float( e_buffer[0] )
                            e_buffer[1] = float( e_buffer[1] )
                            s[i] = float( e_buffer[0] / ( 10 ** e_buffer[1] ) )

                v.x = float( s[1] )
                v.y = float( s[2] )
                v.z = float( s[3] )

                # Check for z_max
                if v.z > z_max:
                    z_max = v.z

                vect_cache.append( v )

            # Index of faces
            #
            elif s[0] == "f":

                v0 = vect_cache[ int(s[1]) - 1 ]
                v1 = vect_cache[ int(s[2]) - 1 ]
                v2 = vect_cache[ int(s[3]) - 1 ]

                t = Triangle( v0, v1, v2 )
                mesh.t.append( t )

    if z_max < 1:
        z_max = 1

    file.close()

    return mesh;


### Main
def main_loop():

    # I chose to init the objects here

    pygame.key.set_repeat( 400, 600 )

    # z_max is used for sorting
    global z_max

    # Camera
    v_cam = Vector()
    v_lookdir = Vector()

    # Pitch and Yaw
    f_pitch = 0
    f_yaw = 0

    # Rotation angle
    f_ang = 0

    # matrices for projections and rotations
    m_proj = matrix_makeproj( FOV_RAD, WIN_HEIGHT / WIN_WIDTH, 0.1, 1000 )

    while True:

        # The forward direction
        v_forward = vector_multi( v_lookdir, 0.1 )

        # Event polling
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()

        # Controls
        if pressed[ K_UP ]:
            v_cam.y += 0.06
        if pressed[ K_DOWN ]:
            v_cam.y -= 0.06
        if pressed[ K_LEFT ]:
            v_cam.x -= 0.06
        if pressed[ K_RIGHT ]:
            v_cam.x += 0.06

        if pressed[ K_e ]:
            v_cam = vector_add( v_cam, v_forward )
        if pressed[ K_d ]:
            v_cam = vector_sub( v_cam, v_forward )
        if pressed[ K_s ]:
            f_yaw -= 0.06
        if pressed[ K_f ]:
            f_yaw += 0.06

        # Clear the screen
        SCREEN.fill(( 0, 0, 0 ))

        # Increment the angle
        # Uncomment this to make the object rotate
        f_ang += 0.02     # about 2 degrees

        # z-rotation matrix
        m_zrot = matrix_makeyrot( f_ang / 2 )

        # x-rotation matrix
        m_xrot = matrix_makexrot( f_ang )

        # Translation matrix
        m_trans = matrix_maketrans( 0, 0, z_max * 3 )

        # World matrix
        m_world = matrix_multimm( m_zrot, m_xrot )
        m_world = matrix_multimm( m_world, m_trans )

        ## Camera shenanigans
        v_up = Vector( 0, 1, 0 )
        v_targ = Vector( 0, 0, 1 )

        # Rotation of the camera
        m_camrot = matrix_makeyrot( f_yaw )

        v_lookdir = matrix_multimv( v_targ, m_camrot )
        v_targ = vector_add( v_cam, v_lookdir )

        m_cam = matrix_point( v_cam, v_targ, v_up )

        # The camera's viewmatrix
        m_view = matrix_invert( m_cam )

        # I actually cannot figure out why I can't just preload a
        # mesh once at runtime
        # Be careful not to set fire to your PC
        fname = "icosahaedron.obj"
        fname = os.path.join( "example", fname )

        try:
            mesh = mesh_loadmodel( fname )

        except:
            print( "File " + fname + " not found." )
            pygame.quit()
            sys.exit()


        tris_to_render = list()

        # Drawing the triangles
        for t in range( len( mesh.t ) ):

            tri = mesh.t[t]
            tri_new = mesh.t[t]
            tri_view = mesh.t[t]

            #  World mat transform
            tri_new.pts[0] = matrix_multimv( tri.pts[0], m_world )
            tri_new.pts[1] = matrix_multimv( tri.pts[1], m_world )
            tri_new.pts[2] = matrix_multimv( tri.pts[2], m_world )

            # Calculate if it's visible
            l_0 = vector_sub( tri_new.pts[1], tri_new.pts[0] )
            l_1 = vector_sub( tri_new.pts[2], tri_new.pts[0] )

            norm = vector_xprod( l_0, l_1 )
            norm = vector_normalise( norm )

            v_camray = vector_sub( tri_new.pts[0], v_cam )

            if ( vector_dot( norm, v_camray ) < 0 ):

                ## Lighting
                v_light = Vector( 0, 0, -1 )
                v_light = vector_normalise( v_light )

                # Calculate the amout of light a surface recieves
                light_dp = max( 0.1, vector_dot( v_light, norm ) )

                # Worldspace to viewspace
                for i in range( 3 ):
                    tri_view.pts[i] = matrix_multimv( tri_new.pts[i], m_view )

                # Inherit the color
                tri_view.cl = tri_shade( light_dp )

                # Clipping
                clipped = tri_clipplane( Vector(0, 0, 1), Vector(0, 0, 1), tri_view )

                # tri_clipplane returns a list if new triangles are formed and
                # and int otherwise so check what it returned
                if isinstance( clipped, list ):

                    # Loop throught all the clipped tris
                    for c in clipped:

                        tri_proj = Triangle()

                        # Projection into 2D
                        for p in range( 3 ):
                            tri_proj.pts[p] = matrix_multimv( c.pts[p], m_proj )

                            # Scaling into view
                            tri_proj.pts[p] = vector_div( tri_proj.pts[p], tri_proj.pts[p].w )

                            # Return the axis
                            tri_proj.pts[p].x *= -1
                            tri_proj.pts[p].y *= -1

                        # Inherit the color
                        tri_proj.cl = c.cl

                        # Offset vectors
                        v_offset = Vector( 1, 1, 0 )
                        for p in range( 3 ):
                            tri_proj.pts[p] = vector_add( tri_proj.pts[p], v_offset )
                            tri_proj.pts[p].x *= WIN_WIDTH / 2
                            tri_proj.pts[p].y *= WIN_HEIGHT / 2

                        # Add to list for sorting
                        tris_to_render.append( tri_proj )

        # Sorting by Z position
        tris_to_render.sort( key=tri_getz )
        tris_to_render.reverse()


        # Clipping and rendering
        for t in tris_to_render:

            t_list = list()
            t_list.append( t )
            n_newtris = 1

            for p in range( 4 ):

                t_clipped = 0

                while n_newtris > 0:

                    t_test = t_list[0]
                    t_list.pop( 0 )
                    n_newtris -= 1

                    if p == 0:
                       t_clipped = tri_clipplane( Vector(0, 0, 0), Vector(0, 1, 0), t_test )
                    elif p == 1:
                        t_clipped = tri_clipplane( Vector(0, WIN_HEIGHT - 1, 0), Vector(0, -1, 0), t_test )
                    elif p == 2:
                        t_clipped = tri_clipplane( Vector(0, 0, 0), Vector(1, 0, 0), t_test )
                    elif p == 3:
                        t_clipped = tri_clipplane( Vector(WIN_WIDTH - 1, 0, 0), Vector(-1, 0, 0), t_test )

                    if isinstance( t_clipped, list ):

                        for triangle in t_clipped:
                            t_list.append( triangle )

                n_newtris = len( t_list )

            for t in t_list:

                # Coords of the vertices
                # typecasted to int
                raster = [
                    ( int( t.pts[0].x ), int( t.pts[0].y) ),
                    ( int( t.pts[1].x ), int( t.pts[1].y) ),
                    ( int( t.pts[2].x ), int( t.pts[2].y) )
                ]

                # Mesh
                pygame.draw.polygon( SCREEN, t.cl, raster )

                # Wireframe
                #pygame.draw.polygon( SCREEN, ( 255, 0, 0 ), raster, 1 )

        # Uncomment to print framerate
        #print( CLOCK.get_fps() )

        try:
            pygame.display.update()
        except:
            pygame.display.flip()

        CLOCK.tick( FPS )

    return;


main_loop()
