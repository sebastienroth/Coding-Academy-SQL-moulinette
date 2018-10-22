import os
import difflib
import sys
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def exec_sql_script(sql_statement):
	"""Execute simple SQL script using subprocess. On error will give the error code and the output.
	Usage::
		>>> my_string = exec_sql_script('SHOW Tables;')
	:param sql_statement: A string with sql_statement to execute
	:rtype: A string with the output of the sql_statement (if fail the sting contain the error code too).
	"""
	cmd = 'mysql -u root --password=root coding -e \"{}\"'.format(sql_statement)
	try:
		output = subprocess.check_output(
			cmd, stderr=subprocess.STDOUT, shell=True, timeout=3,
			universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		return('Status : FAIL ' + str(exc.returncode) + ' ' + exc.output)
	else:
		return('{}'.format(output))

def help(code):
	"""Display the help and exit.
	:param code: A int specifying the return code for the program (can be 84 or 0).
	"""
	print('USAGE\n\t\t./mouli-d01.py <dossier ref> <dossier test>')
	sys.exit(code)

def write_trace(trace):
	"""Write in file trace.txt the complete output of the test
	:param trace: A list containing complete logging of the testing
	"""
	n = 1
	my_file = open('trace.txt', 'w')
	for line in trace:
		my_file.write('exercice n°'+str(n)+'\n\n')
		my_file.writelines(line)
		my_file.write('\n')
		n += 1
	my_file.close()

def read_arbo(arbo, folder):
	"""Read the filesystem and return all sql exercices in folder.
	Usage::
		>>> import os
		>>> arbo = Sorted(os.listdir(folder_reference), key=str.lower)
		>>> folder = '.'
		>>> my_list = read_arbo(arbo, folder)
	:param arbo: A list of the files in the folder given in parameters.
	:param folder: A string containing the name of the folder to browse.
	:rtype: A list of tuple of the form ``(num_exercice, sql_statement)``
	"""
	statement_list = []
	n = 1
	for files in arbo:
		with open(folder+files+'/'+files+'.sql', 'r') as f:
			statement_list.append((n, f.read()))
		n += 1
	return statement_list

def create_arbo(folder):
	"""Create a List sorted by alphabetical order with the 
		content of the folder given as parameter.
	:param folder: A string containing the folder to list files.
	:rtype: A list of the files in folder.
	"""
	return sorted(os.listdir(folder), key=str.lower)

if __name__ == "__main__":
	if '-h' in sys.argv[1:]:
		help(0)
	try:
		if len(sys.argv) != 3:
			raise Exception('Invalid number of arguments')
		folder_reference = sys.argv[1]
		folder_test = sys.argv[2]
		arbo_test = create_arbo(folder_test)
		arbo_ref = create_arbo(folder_reference)
		list_ref = read_arbo(arbo_ref, folder_reference)
		list_test = read_arbo(arbo_test, folder_test)
	except Exception as e:	
		print('Error:', e)	
		help(84)

	fails = 0
	trace = []	
	for elem_ref, elem_test in zip(list_ref, list_test):
		print('Correcting exercice n°{}'.format(elem_ref[0]))
		ref = exec_sql_script(elem_ref[1]).splitlines()
		test = exec_sql_script(elem_test[1]).splitlines()
		diff = difflib.ndiff(ref, test)
		delta1 = ''.join(x[2:] for x in diff if x.startswith('- '))
		diff = difflib.ndiff(ref, test)
		delta2 = ''.join(x[2:] for x in diff if x.startswith('+ '))
		if delta1 or delta2:
			fails += 1
			print(bcolors.FAIL + 'OUTPUT DIFFER [KO]\n' + bcolors.ENDC, 'you:\t\t', delta2, '\nexpected:\t', delta1, sep='')
			trace.append('OUTPUT DIFFER [KO]\n' + 'you:\t\t ' + delta2 + ' ' + '\nexpected:\t ' + delta1)
			trace.append('Your SQL statement is probably false\n>>> \"{}\"\n'.format(elem_test[1].strip('\n')))
		else:
			print(bcolors.OKGREEN + 'Test Passed [OK]' + bcolors.ENDC)
			trace.append('Test Passed [OK]')
	
	write_trace(trace)
	print(bcolors.WARNING + '\nEnd of the tests', fails, 'fails out of', len(list_ref), 'exercises')
	print('\n\nSee trace.txt to view your errors' + bcolors.ENDC)
	sys.exit(0)
