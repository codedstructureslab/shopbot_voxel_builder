'''
DESCRIPTION: 
    resume_at_line.py takes in a file and line number and creates a temporary
    file that starts at specified line number.
			 
	The objective is to resume a build file that was interupted by a kill switch.
	After the kill switch is initiated, shopbot program will notify operator of 
	the last line number executed.
			 
	Operator should review the file and pick an approporiate location (line_number)
	to resumet running.
			 
USAGE:
    python resumet_at_line.py <filename> <line_number>			 
			 
EXAMPLE:
	python resume_at_line.py test_resume_at_line_num.sbp 10
	
'''
import sys
import os
import time

if len(sys.argv)<3:
    print("not enough arguments passed")

filename = sys.argv[1]
linenum = sys.argv[2]

# print filename
# print linenum

tmp_filename = "@line" + str(linenum) + '_' + filename
# print tmp_filename

tmp_file = []
# reading file and collecting lines to be executed
with open(filename,'r') as x:
    for l_num, each_line in enumerate(x):
	    if l_num+1 >= int(linenum):
			#print l_num+1, each_line  # +1 b/c l_num from enumerate starts with 0
			tmp_file.append(each_line)

# create temporary file to be executed
with open(tmp_filename,'w') as newfile:
	for each in tmp_file:
		# print each
		newfile.write(each)
		
print tmp_filename + ' created'

# execute file in shopbot
cwd = os.getcwd()
os.chdir("c:\\Program Files (x86)\\ShopBot\\ShopBot 3")       # directory for SB3.exe
os.system('SB3.exe "' + cwd + "\\" + tmp_filename + '",1,5')  # argv[0] 1 = port; argv[1] 4 = move/cut no stop, 5 = preview no stop
os.chdir(cwd)                                                 # changing back to working directory
time.sleep(1)  # wait 1 second for command to make it to shopbot before deleting tmp file
os.remove(tmp_filename)                                       # remove temporary file