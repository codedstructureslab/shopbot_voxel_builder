# sbp_run.py
'''
DESCRIPTION: 
    Originally, resume_at_line.py was written to run a file at a particular line
	for the purpose of resuming a file that was ended with a kill switch.
	
	This is expaned in sbp_run.py to run an arbitrary file with an optional input
	of line number.
	
	resume_at_line.py:
	takes in a file and line number and creates a temporary
    file that starts at specified line number.
			 
	The objective is to resume a build file that was interupted by a kill switch.
	After the kill switch is initiated, shopbot program will notify operator of 
	the last line number executed.
			 
	Operator should review the file and pick an approporiate location (line_number)
	to resume running.
			 
USAGE:
    python run.py <filename> <(optional)line_number>
	(old) python resumet_at_line.py <filename> <line_number>			 
			 
EXAMPLE:
	python test_resume_at_line_num.sbp 10
	(old) python resume_at_line.py test_resume_at_line_num.sbp 10
	
'''
import sys
import os
import time

cwd = os.getcwd()
sb3_dir = "c:\\Program Files (x86)\\ShopBot\\ShopBot 3"

if len(sys.argv)<2:
    print("not enough arguments passed")

filename = sys.argv[1]

if len(sys.argv>2:
	linenum = sys.argv[2]

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

	# execute file in shopbot at particular line
	os.chdir(sb3_dir)       # directory for SB3.exe
	os.system('SB3.exe "' + cwd + "\\" + tmp_filename + '",1,5')  # argv[0] 1 = port; argv[1] 4 = move/cut no stop, 5 = preview no stop
	os.chdir(cwd)                                                 # changing back to working directory
	time.sleep(1)  # wait 1 second for command to make it to shopbot before deleting tmp file
	os.remove(tmp_filename)                                       # remove temporary file
else:
    # execute file
    os.chdir(sb3_dir)       # directory for SB3.exe
	os.system('SB3.exe "' + cwd + "\\" + filename + '",1,5')      # argv[0] 1 = port; argv[1] 4 = move/cut no stop, 5 = preview no stop
	os.chdir(cwd)                                                 # changing back to working directory
	time.sleep(1)  # wait 1 second for command to make it to shopbot before deleting tmp file