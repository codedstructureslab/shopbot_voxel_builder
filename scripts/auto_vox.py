## test script to build/visualize arbitrary voxel structure
'''
TODO:
- remove redundancy; id_matrix creation
- put in check to ensure every vox has at least one attachment
- consider making a voxel definition gui
- consider make overwrite warning for duplicate files

USAGE:
  mspython auto_vox.py <geometry> <filename>
  
OUTPUT:
 ./SBP_output/<geometry>.SBP
'''

## IMPORTS -----------------------------------
import matplotlib.pylab as plt           # working with plots
from mpl_toolkits.mplot3d import Axes3D  # working in 3d
import numpy as np                       # working with matrixes
import copy                              # working with copies of lists
# import shopbot_base_programs as sbp      # working with SHOPBOT
import Tkinter as tk                     # working with GUI
import tkFileDialog                      # working with file browser
import tkMessageBox                      # working with message boxes
import os                                # working with file input/output
import sys                               # working with input arguments
import voxGeo                            # working with voxel geometry
import voxUtils                          # working with voxel utility functions # TODO: not yet implemented

# # testing the waters with embedding figure into tkinter window such that text frame can later be added
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # testing the waters with PyOpenGL  # NOT YET IMPLEMENTED
# import OpenGL
# import pygame

# TODO: change usage to mspython auto_vox.py <input voxel geometry matrix> >> ./SBP_output/<filename>.SBP

#---------------------------------------------
class vox:
    def __init__(self, id, center):
        self.id = id  # ID
        self.center = center
        # NOT USED; thinking whether or not to store this info within vox class
        self.perimeter = [-1,-1,-1,-1,-1,-1]  # perimeter/neighbor [px,mx,py,my,pz,mz] 

#---------------------------------------------
        
def main():
    global plot_cuboct_flag
    global seeded_num
    global SBP_output
    global output_fullpath_filename
    
    # checking inputs
    if len(sys.argv) != 2:
        print "ERROR - expecting input: geometry that is defined in geoVox.py; exiting..."
        sys.exit()
    
    # checking voxGeo.py for voxel structure definitions
    defined_voxel_structures = [x for x in dir(voxGeo) if x.startswith('v')]

    geo_name = sys.argv[1].split('/')[-1]
    if geo_name in defined_voxel_structures:
        input_geometry = getattr(voxGeo, geo_name)
    
    output_fullpath_filename = '../SBP_output/make_' + geo_name + '.sbp'
    
    # user inputs
    seeded_num = 2                     # number of layers seeded; typically 2
    show_vox_build_flag = False        # shows plot of vox build 
    output_shopbot_build_flag = True   # outputs shopbot build
    plot_cuboct_flag = True            # shows full cuboct lattice on plot
    SBP_output = []                    # container for sbp file
    
    # setup
    setup_vox_geometry()      # sets voxel geometry
    setup_shopbot_table(vgeo)  # sets table offset and coordinate transformation
    plt.ion()              # interactive plotting; used so plt.pause will work
    
    # input voxel structures are defined in voxGeo.py
    input_vox_structure = input_geometry  # <-------------------------- USER INPUT
    
    # print input_vox_structure
    if show_vox_build_flag:
        show_vox_build(input_vox_structure)
    if output_shopbot_build_flag:
        output_shopbot_build(input_vox_structure)
    
    plt.ioff()
    plt.show()
    # setup_GUI(fig)  # initiating GUI
    

def setup_GUI(fig):
    # working with GUI --------------------------------------------
    print '\ninitializing...'
    
    GUI = tk.Tk()
    GUI.title('CSL - Autovox')
    GUI.minsize(150,150)
    GUI.geometry('1280x400+0+0')
    
    f0 = tk.Frame(GUI)                            # defining frame
    f0.pack(fill='both',expand=True)
    
    f0_area = tk.Canvas(f0, width=10,height=10)   # defining canvas area within frame
    f0_area.pack(side=tk.TOP)
    
    graph = FigureCanvasTkAgg(fig)
    graph.show()
    graph.pack()
    # but1 = tk.Button(f0, text='Show Voxel Build', height=1, width=15, command= lambda: show_vox_build())
    # but1.pack(side=tk.RIGHT)
    # f0_area.create_window(10,10, window=but1)
    
    GUI.mainloop()
    # -------------------------------------------------------------
    
def setup_vox_geometry():
    global in2mm
    global mm2in
    global vgeo
    global cuboct_verts
    
    in2mm = 25.4  # 1 inch = 25.4 mm
    mm2in = 1/in2mm
    vgeo = [3*in2mm,3*in2mm,3*in2mm]  # 3 inch voxels in mm
    cuboct_verts = [(   0,   0,-0.5),
                    (   0,-0.5,   0),
                    (   0,   0, 0.5),
                    (   0, 0.5,   0),
                    (   0,   0,-0.5),
                    ( 0.5,   0,   0),
                    (   0,   0, 0.5),
                    (-0.5,   0,   0),
                    (   0, 0.5,   0),
                    ( 0.5,   0,   0),
                    (   0,-0.5,   0),
                    (-0.5,   0,   0),
                    (   0,   0,-0.5)]

                    
def setup_shopbot_table(vgeo):
    global sb_off
    global sb_dir
    
    sb_off = [vgeo[0]*1, vgeo[1]*1, vgeo[2]*-1]  # shopbot zero offset
    sb_dir = [-1, -1, 1]  # shopbot direction map; could be matrix for axis transformation
    
    
def setup_figure(max_dim=5):
    global fig
    global ax
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_xlabel('X [mm]  --->')  # red
    ax.set_ylabel('Y [mm]  --->')  # green
    ax.set_zlabel('Z [mm]  --->')  # blue
    
    # setting axis colors to match solid works default
    ax.xaxis.label.set_color('red')
    ax.tick_params(axis='x', colors='red')
    ax.yaxis.label.set_color('green')
    ax.tick_params(axis='y', colors='green')
    ax.zaxis.label.set_color('blue')
    ax.tick_params(axis='z', colors='blue')
    
    ax.set_xlim([sb_dir[0]*(max_dim - 1.5*vgeo[0]),  1.5*vgeo[0]])
    ax.set_ylim([sb_dir[0]*(max_dim - 1.5*vgeo[0]),  1.5*vgeo[0]])
    ax.set_zlim([-1.5*vgeo[2], max_dim - 1.5*vgeo[2]])
    # ax.set_zlim([-1*vgeo[2], max_dim - 1*vgeo[2]])
    # ax.axis('equal')
    ax.view_init(30,140)  # elevation, azimuth


def setup_seed():  # NOT USED
    global seed_matrix
    seed_matrix = np.ones((2,2,2))  # 3d square 2x2 voxel matrix (z,y,x)
    
    seed_matrix[1][1][1] = 0
    seed_matrix[1][1][0] = 0
    seed_matrix[1][0][1] = 0
    seed_matrix[0][1][1] = 0
    show_vox_build(seed_matrix, 0, 9)
    
    
def seeded(voxMatrix):
    seeded_voxMatrix = copy.deepcopy(voxMatrix)
    seeded_voxMatrix[0][0][0] = 0
    seeded_voxMatrix[0][1][0] = 0
    seeded_voxMatrix[1][0][0] = 0
    seeded_voxMatrix[0][0][1] = 0
    return seeded_voxMatrix
    
def seeded7(voxMatrix):
    seeded_voxMatrix = copy.deepcopy(voxMatrix)
    seeded_voxMatrix[0][0][0] = 0
    seeded_voxMatrix[0][1][0] = 0
    seeded_voxMatrix[1][0][0] = 0
    seeded_voxMatrix[0][0][1] = 0
    seeded_voxMatrix[1][0][1] = 0
    seeded_voxMatrix[0][1][1] = 0
    seeded_voxMatrix[1][1][0] = 0
    return seeded_voxMatrix

    
def show_working_area(vox):
    # showing voxel zero point
    ax.scatter(0, 0, 0, color='red', marker='o', s=200)
    
    # showing nut pickup zero point?
    # showing bolt pickup zero point?
    # showing voxel pickup zero point?
    
    # plotting x for each potential voxel
    for each in vox:
        show_vox(vox[each], ax, 0)
        
        
def show_vox(vox, build_num, style=1):  # plots individual voxels
    # TODO: replace if with case of different styles
    if style == 0:  # plotting empty voxel space as red "x"
        ax.scatter(vox.center[0], vox.center[1], vox.center[2], color='red', marker='x', s=20)
    elif style == 9:
        ax.scatter(vox.center[0], vox.center[1], vox.center[2], marker='*', s=200)
        ax.text(vox.center[0], vox.center[1], vox.center[2], '%s' % str(build_num), size=20)
        # plotting cubocts if global flag set
        if plot_cuboct_flag:
            show_lattice(vox.center, 'k')
    else:
        ax.scatter(vox.center[0], vox.center[1], vox.center[2], marker='*', s=200)
        ax.text(vox.center[0], vox.center[1], vox.center[2], '%s' % str(build_num), size=20)
        # plotting cubocts if global flag set
        if plot_cuboct_flag:
            show_lattice(vox.center)

            
def show_lattice(vox_pos,color='b'):
    xs,ys,zs=[],[],[]
    for (x,y,z) in cuboct_verts:
        xs.append(x*vgeo[0] + vox_pos[0])
        ys.append(y*vgeo[1] + vox_pos[1])
        zs.append(z*vgeo[2] + vox_pos[2])
    ax.plot(xs, ys, zs, zdir='z', c=color, linewidth=2)
    

def show_vox_build(voxMatrix, delay=0.1, style=1):  # plots voxel build
    # setup_figure(len(voxMatrix[0])*vgeo[0])
    setup_figure(3*vgeo[0])
    vox, build = get_voxbuild(voxMatrix)
    show_working_area(vox)

    # fig.suptitle('Numbered by build order', fontsize=20)
    fig.suptitle('Numbered by vox id', fontsize=20)
    # fig.set_xlim3d(135,24)
    # 135 27
    # plt.pause(25) # initial pause to give time to setup video recording 20170222
    
    for num,each in enumerate([i for sublist in build for i in sublist]):
        # print vox[each].id, vox[each].center, vox[each].perimeter
        # show_vox(vox[each], num+1)  # numbered by build order
        show_vox(vox[each], vox[each].id, style)  # numbered by vox id
        #print delay
        if delay:  # 0 = no delay
            plt.pause(delay)
        
        
def output_shopbot_build(voxMatrix):
    vox, build = get_voxbuild(voxMatrix)
    # dir = ['x','-x','y','-y','z','-z']
    dir = ['-x','x','-y','y','z','-z']  # shopbot dir
    assembled = []
    
    SBP_output.append("''AUTOGENERATED by auto_vox.py (EDIT w/ CAUTION)\n")
    SBP_output.append("\'\'\nSA \'\'sets absolute coordinates\n\'\'\n")
    SBP_output.append('PRINT ""\n')
    SBP_output.append('PRINT "Start Date Time:"\n')
    SBP_output.append('PRINT %(146); " "; %(147)\n')  # print date and time using shopbot
    SBP_output.append('PRINT "Settings:"\n')
    SBP_output.append('PRINT "Software/Firmware:"\n')
    SBP_output.append('PRINT %(48); "/"; %(49)\n')  # print date and time using shopbot
    SBP_output.append('PRINT "Speeds:"\n')
    SBP_output.append('PRINT "mxy: "; %(71); ",mz: "; %(73); ",ma: "; %(74); ",mb: "; %(75);\n')
    SBP_output.append('PRINT "jxy: "; %(76); ",jz: "; %(78); ",ja: "; %(79); ",jb: "; %(80);\n')
    SBP_output.append('PRINT ""\n')
    SBP_output.append('PRINT "Voxel size ' + str(round(vgeo[0]*mm2in,1)) + ' ' + str(round(vgeo[1]*mm2in,1)) + ' ' + str(round(vgeo[2]*mm2in,1)) + ' in."\n\'\'\n')
    
    # Account for pre-built seed structure ------------------------------------------------
    build_seed = build[:seeded_num]
    build = build[seeded_num:]  # first <seeded_num> build arrays are for seed;
    
    for num, each in enumerate([i for sublist in build_seed for i in sublist]):
        assembled.append(vox[each].id)
    #----------------------------------------------------------------------------
    
    for num, each in enumerate([i for sublist in build for i in sublist]):
        shp_reload_voxel()
        # setting voxel location in shopbot
        SBP_output.append('PRINT "NEXT VOXEL: ' + str(vox[each].id) + ' at ' + str(vox[each].center).replace(',', '') + ' <-------------------------- VOXEL"\n')
        shp_set_vox_pos(vox[each].center[0],vox[each].center[1],vox[each].center[2])
        xyz_flag = [0,0,0]
        SBP_output.append("''\n")
        # make attachments
        for i in reversed(range(len(vox[each].perimeter))):  # doing z connections then y then x
            if vox[each].perimeter[i] in assembled:
                SBP_output.append('PRINT "ATTACH voxel: ' + str(vox[each].id) + ' to ' + str(vox[each].perimeter[i]) + ' at ' + dir[i] + '"\n')
                if 'z' in dir[i]:
                    xyz_flag[2] = 1
                elif 'y' in dir[i]:
                    xyz_flag[1] = 1
                elif 'x' in dir[i]:
                    xyz_flag[0] = 1
        # initial placement and first attachment
        if xyz_flag[2]:  # position and attach Z
            #print sbp.position_attach_z(vox[each].center[0],vox[each].center[1],vox[each].center[2])
            shp_place_vox_z(vox[each].id)
            xyz_flag[2] = 0  # z-attached, reseting flag
        elif xyz_flag[1]:  # position and attach Y
            #print sbp.position_attach_y(vox[each].center[0],vox[each].center[1],vox[each].center[2])
            shp_place_vox_y(vox[each].id)
            xyz_flag[1] = 0  # y-attached, reseting flag
        elif xyz_flag[0]:
            #print sbp.position_attach_x(vox[each].center[0],vox[each].center[1],vox[each].center[2])
            shp_place_vox_x(vox[each].id)
            xyz_flag[0] = 0  # x-attached, reseting flag
        
        # making remaining attachments
        if xyz_flag[1]:
            #print sbp.attach_y(vox[each].center[0],vox[each].center[1],vox[each].center[2])
            shp_attach_y(vox[each].id)
            xyz_flag[1] = 0
        if xyz_flag[0]:
            #print sbp.attach_x(vox[each].center[0],vox[each].center[1],vox[each].center[2])
            shp_attach_x(vox[each].id)
            xyz_flag[0] = 0
        
        assembled.append(vox[each].id)  
    
    shp_reload()  # Return to reload position after build completes
    SBP_output.append('PRINT "End Time:"\n')
    SBP_output.append('PRINT %(146); " "; %(147)\n')  # print date and time using shopbot
    # print 'PRINT "Total Duration:"'  # shopbot's elasped time not quite working... outputed 0
    # print 'PRINT %(130)'               # print total elapsed time using shopbot
    SBP_output.append("''\n")
    SBP_output.append("END\n")
    
    save_SBP_output()

    
def shp_move_pickup_loc():
    SBP_output.append('FP, move_pickup_zero.sbp, 1,1,1,1,0\n')
    

def shp_pickup_screw():
    SBP_output.append("''ready to pickup SCREW?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, pickup_screw.sbp, 1,1,1,1,0\n')


def shp_pickup_nut():
    SBP_output.append("''ready to pickup NUT?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, pickup_nut.sbp, 1,1,1,1,0\n')
    

def shp_pickup_voxel():
    SBP_output.append("''ready to pickup VOXEL?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, pickup_voxel_0.sbp, 1,1,1,1,0\n')

    
    
def shp_reload_voxel():
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "RELOAD_VOXEL_SCREW_NUT"\n')
    shp_move_pickup_loc()
    shp_pickup_screw()
    shp_pickup_nut()
    shp_pickup_voxel()
    SBP_output.append('ST\n')
    shp_reload()  # TODO: remove once pickup is ready...

    
def shp_reload_bolts():
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "RELOAD_SCREW_NUT"\n')
    shp_move_pickup_loc()
    shp_pickup_screw()
    shp_pickup_nut()
    SBP_output.append('ST\n')
    shp_reload()  # TODO: remove once pickup is ready...


def shp_reload(grip = 0):  # old location where people can manually reload
    SBP_output.append("''\n")
    SBP_output.append('PRINT "RELOAD_PAUSE"\n')
    SBP_output.append('J5 -130,-300,170,0,0\n')
    SBP_output.append('FP, effector_jawOpen.sbp,1,1,1,1,0\n')
    if grip:
        SBP_output.append('MSGBOX(YES: Engage Gripper  NO: Do nothing,yesno,Engage Gripper?  )\n')
        SBP_output.append('IF &MSGANSWER = "YES" THEN FP, effector_gripperEngage.sbp,1,1,1,1,0\n')
    SBP_output.append("''Finished screw/nut feed?\n")
    SBP_output.append('PAUSE\n')
    
      
def shp_set_vox_pos(x,y,z):
    SBP_output.append('&current_vox_x = ' + str(x) + '\n')
    SBP_output.append('&current_vox_y = ' + str(y) + '\n')
    SBP_output.append('&current_vox_z = ' + str(z) + '\n')
        
def shp_place_vox_x(vox_num):
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "PLACE_VOXEL_X_' + str(vox_num) + ':"\n')
    SBP_output.append('PLACE_VOXEL_X_' + str(vox_num) + ':\n')
    SBP_output.append('FP, place_vox_p120.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_x.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, effector_gripperDisengage.sbp,1,1,1,1,0\n')
    SBP_output.append('MOVE_OUT_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out Baxis@+120?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_p120.sbp, 1,1,1,1,0\n')

    
def shp_place_vox_y(vox_num):
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "PLACE_VOXEL_Y_' + str(vox_num) + ':"\n')
    SBP_output.append('PLACE_VOXEL_Y_' + str(vox_num) + ':\n')
    SBP_output.append('FP, place_vox_m120.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_y.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, effector_gripperDisengage.sbp,1,1,1,1,0\n')
    SBP_output.append('MOVE_OUT_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out Baxis@-120?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_m120.sbp, 1,1,1,1,0\n')

    
def shp_place_vox_z(vox_num):
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "PLACE_VOXEL_Z_' + str(vox_num) + ':"\n')
    SBP_output.append('PLACE_VOXEL_Z_' + str(vox_num) + ':\n')
    SBP_output.append('FP, place_vox_0.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_z.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, effector_gripperDisengage.sbp,1,1,1,1,0\n')
    SBP_output.append('MOVE_OUT_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out B@0?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_0.sbp, 1,1,1,1,0\n')

   
def shp_attach_x(vox_num):
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "ATTACH_X_' + str(vox_num) + ':"\n')
    SBP_output.append('ATTACH_X_' + str(vox_num) + ':\n')
    shp_reload_bolts()
    SBP_output.append('MOVE_BOLT_PX:\n')
    SBP_output.append('FP, place_vox_p120.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_x.sbp,1,1,1,1,0\n')
    SBP_output.append("''\n")
    SBP_output.append('MOVE_OUT_p120_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out B@+120?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_p120.sbp, 1,1,1,1,0\n')


def shp_attach_y(vox_num):
    SBP_output.append("''\n")
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "ATTACH_Y_' + str(vox_num) + ':"\n')
    SBP_output.append('ATTACH_Y_' + str(vox_num) + ':\n')
    shp_reload_bolts()
    SBP_output.append('MOVE_BOLT_PY:\n')
    SBP_output.append('FP, place_vox_m120.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_y.sbp,1,1,1,1,0\n')
    SBP_output.append("''\n")
    SBP_output.append('MOVE_OUT_m120_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out B@-120?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_m120.sbp, 1,1,1,1,0\n')
    

def shp_attach_z(vox_num):  # not used as it's typically the first attachment made
    SBP_output.append('PRINT %(147)\n')  # print timing using shopbot
    SBP_output.append('PRINT "ATTACH_Z_' + str(vox_num) + ':"\n')
    SBP_output.append('ATTACH_Z_' + str(vox_num) + ':\n')
    shp_reload_bolts()
    SBP_output.append('MOVE_BOLT_MZ:\n')
    SBP_output.append('FP, place_vox_0.sbp,1,1,1,1,0\n')
    SBP_output.append('FP, bolt.sbp,1,1,1,1,0\n')
    # SBP_output.append('FP, shake_z.sbp,1,1,1,1,0\n')
    SBP_output.append("''\n")
    SBP_output.append('MOVE_OUT_0_' + str(vox_num) + ':\n')
    SBP_output.append("''Ok to move out B@0?\n")
    SBP_output.append('PAUSE\n')
    SBP_output.append('FP, release_vox_0.sbp, 1,1,1,1,0\n')

        
def get_neighbor(id_matrix):
    # returns dictionary with matrix id and it's corresponding neighbors
    x,y,z = [np.size(id_matrix,0), np.size(id_matrix,1), np.size(id_matrix,2)]   # extracting matrix dimensions
    neighbor = {}
    for kk in range(z):       # looping through id_matrix to get element perimeter/neighbors 
        for jj in range(y):   # ...needed to know which attachments to make
            for ii in range(x):
                PX,MX,PY,MY,PZ,MZ = -1,-1,-1,-1,-1,-1  # initialize to -1 = no neighbor
                px,py,pz,mx,my,mz = ii+1,jj+1,kk+1,ii-1,jj-1,kk-1
                if px >= 0 and px < x:
                    PX = id_matrix[kk][jj][px]
                if mx >= 0 and mx < x:
                    MX = id_matrix[kk][jj][mx]
                if py >= 0 and py < x:
                    PY = id_matrix[kk][py][ii]
                if my >= 0 and my < x:
                    MY = id_matrix[kk][my][ii]
                if pz >= 0 and pz < x:
                    PZ = id_matrix[pz][jj][ii]
                if mz >= 0 and mz < x:
                    MZ = id_matrix[mz][jj][ii]
                neighbor[id_matrix[kk][jj][ii]] = [PX,MX,PY,MY,PZ,MZ]
    return neighbor

    
def buildorder(voxMatrix):
    x,y,z = [np.size(voxMatrix,0), np.size(voxMatrix,1), np.size(voxMatrix,2)]   # extracting voxMatrix dimensions
    id_matrix = np.array([i+1 for i in range(x*y*z)]).reshape((x,y,z))           # creating vox matrix with id
    neighbor = get_neighbor(id_matrix)  # getting neighbor info for knowing where attachments are made
    
    buildsteps = [[] for i in range(x+y+z-2)]
    for layer in range(z):
        for step in range((x+y)-1):  
            step_matrix = np.array([[0]*x for each in range(y)])
            # looping through step_matrix and assigning boolean diagonals
            a,b = step,0  # initialize index pointer of step matrix
            while a >= 0:
                if a < x and b < y:
                    step_matrix[a][b] = 1
                a-=1  # decrement to go along diagonal
                b+=1  # increment to go along diagonal
        
            # # diagnostic info
            # print 'layer:', str(layer+1),'step:', str(step+1+layer)
            # print step_matrix * id_matrix[layer]
            
            # transpose function reverse order to Y then X: to match Molly's code 10/5/16
            build_matrix = np.transpose(voxMatrix[layer] * step_matrix * id_matrix[layer])
            
            for each_voxel in [element for sublist in build_matrix for element in sublist]:
                if each_voxel != 0:
                    buildsteps[step+layer].append(each_voxel)
    # print buildsteps
    return buildsteps  # list of (list of steps)

    
def ingest_voxMatrix(voxMatrix):
    # voxMatrix is a binary 3d matrix of arbitrary dimensions describing the vox structure
    # ingest_voxMatrix() takes in voxMatrix and returns list of vox class of given vox structure
    # ... with vox ID, vox CENTER (based on vox geometry), vox PERIMETER (neighbors)
    # ... it also returns a modified voxMatrix in cases where it's not a square matrix
    
    dx,dy,dz = vgeo[0],vgeo[1],vgeo[2]  # spacing between voxel centers WRT x,y,z axes
    
    # check input: ensure numpy matrix
    if type(voxMatrix) is not 'numpy.ndarray':
        try:
           voxMatrix = np.array(voxMatrix)
        except:
            print 'input voxMatrix is not a numpy array.  Attempt to convert failed!'
    
    # check for square matrix; if not, convert to square
    x0,y0,z0 = [np.size(voxMatrix,0), np.size(voxMatrix,1), np.size(voxMatrix,2)]
    if x0 != y0 or y0 != z0 or x0 != z0:
        max_dim = max(x0,y0,z0)
        empty_vox_matrix = np.zeros((max_dim, max_dim, max_dim))  # initialize square maxtrix
        empty_vox_matrix[:x0,:y0,:z0] = voxMatrix
        voxMatrix = empty_vox_matrix  # modified square version of vox structure
    
    x,y,z = [np.size(voxMatrix,0), np.size(voxMatrix,1), np.size(voxMatrix,2)]
    id_matrix = np.array([i+1 for i in range(x*y*z)]).reshape((x,y,z))  # creating vox matrix with id
     
    neighbor = get_neighbor(id_matrix)  # getting neighbor info for knowing where attachments are made
    
    voxlist = {}
    id = 1
    for k in range(z):
        for j in range(y):
            for i in range(x):
                voxlist[id] = vox(id,[round((i*dx*sb_dir[0]) + sb_off[0],1),  # accounts for vox geometry
                                      round((j*dy*sb_dir[1]) + sb_off[1],1),  # ... and table zero offset
                                      round((k*dz*sb_dir[2]) + sb_off[2],1)]) # ... and table direction
                voxlist[id].perimeter = neighbor[id]
                id += 1
    
    return voxlist, voxMatrix
    
    
def get_voxbuild(voxMatrix):  # abstracts
    # get_voxbuild returns list of vox class of the vox structure build order 
    # voxMatrix is pass through to other functions
    
    voxlist, voxMatrix = ingest_voxMatrix(voxMatrix)
    voxbuild = buildorder(voxMatrix)
        
    return voxlist, voxbuild
    
def save_SBP_output():
    with open(output_fullpath_filename,'w') as fileout:
        for each in SBP_output:
            fileout.write(each)
    print output_fullpath_filename + ' created'
        

def log():
    # TODO: add log to collect information about induced error perturbations and build results (success/failure)
    pass
    
    
def test():
    pass
    
    
if __name__ == '__main__':
    main()

    
