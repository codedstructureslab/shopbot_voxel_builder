'''
DESCRIPTION: 

INPUT:
  1. voxel grid x,y,z position
'''
import sys   # working with input arguments
import os
import time

cwd = os.getcwd()
shopbot_dir = "c:\\Program Files (x86)\\ShopBot\\ShopBot 3"
shopbot_mode = str(5)  # 4 = move/cut (no stop), 5 = preview (no stop)


if len(sys.argv)==2:
    grid_str = sys.argv[1]
    grid_x = int(grid_str.split(',')[0])
    grid_y = int(grid_str.split(',')[1])
    grid_z = int(grid_str.split(',')[2])
elif len(sys.argv)==4:
    voxel_num = sys.argv[1]
    grid_x = int(sys.argv[1])
    grid_y = int(sys.argv[2])
    grid_z = int(sys.argv[3])
else:
    print("ERROR - input voxel grid x,y,z expected; exiting...")
    sys.exit()

print 'grid: ' + str(grid_x) + ',' + str(grid_y) + ',' + str(grid_z) + ' --> ',
    
# TODO: get vox geometry from standard source
vox_size = 76.2  # mm


x = (-1 * (grid_x-1) * vox_size) + vox_size
y = (-1 * (grid_y-1) * vox_size) + vox_size
z = ((grid_z-1) * vox_size) - vox_size


print str(x) + ',' + str(y) + ',' + str(z)

    
tmp_file = []
tmp_file.append('&current_vox_x = ' + str(x))
tmp_file.append('&current_vox_y = ' + str(y))
tmp_file.append('&current_vox_z = ' + str(z))

tmp_filename = 'set_vox_pos_' + str(grid_x) + '_' + str(grid_y) + '_' + str(grid_z) + '.tmp_sbp'

# create temporary file to be executed
with open(tmp_filename,'w') as newfile:
    for each in tmp_file:
        newfile.write(each + '\n')
            
print tmp_filename + ' executing...',  

# execute tmp_file in shopbot
os.chdir(shopbot_dir)       # directory for SB3.exe
os.system('SB3.exe "' + cwd + "\\" + tmp_filename + '",1,' + shopbot_mode)
os.chdir(cwd)               # changing back to working directory
time.sleep(2)               # wait 5 second for command to make it to shopbot before deleting tmp file
os.remove(tmp_filename)     # remove temporary file
print('completed')
