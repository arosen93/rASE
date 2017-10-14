import os
def run_bader(keywords=''):
	"""Performs Bader analysis from AECCAR0, AECCAR2, and CHGCAR files. 
	Requires bader and chgsum.pl scripts from http://theory.cm.utexas.edu/henkelman/code/bader/
	added to path.
	keywords is a string containing any necessary command line arguments as discussed
	on the Bader website
	"""

	cmd1 = 'chgsum.pl AECCAR0 AECCAR2'
	os.system(cmd1)
	cmd2 = 'bader ' + keywords + 'CHGCAR -ref CHGCAR_sum'
	os.system(cmd2)