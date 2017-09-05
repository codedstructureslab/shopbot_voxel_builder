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

if len(sys.argv)<3:
    print("not enough arguments passed")

filename = sys.argv[1]
linenum = sys.argv[2]

print filename
print linenum

tmp_file_name = "at_line_" + str(linenum) + '_of_' + filename
print tmp_file_name

tmp_file = []
with open(filename,'r') as x:
    for l_num, each_line in enumerate(x):
	    if l_num >= int(linenum):
			#print l_num+1, each_line  # +1 b/c l_num from enumerate starts with 0
			tmp_file.append(each_line)

with open(tmp_file_name,'w') as newfile:		
	for each in tmp_file:
		print each
		newfile.write(each)
		

	
	
	
	