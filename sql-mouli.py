import os
import difflib
import sys
import subprocess
import signal

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
	cmd = 'mysql -u root --password=root coding -e'.split(' ')
	cmd.append('{}'.format(sql_statement.replace('\n', ' ')))
	try:
		output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as exc:
		return('Status : FAIL ' + str(exc.returncode) + ' ' + str(exc.output))
	else:
		return('{}'.format(output))

def help(code):
	"""Display the help and exit.
	:param code: A int specifying the return code for the program (can be 84 or 0).
	"""
	print('USAGE\n\t\t./mouli-d01.py <dossier ref> <dossier test>')
	sys.exit(code)

def write_trace(trace, trace_name='trace.txt'):
	"""Write in file trace.txt the complete output of the test
	:param trace: A list containing complete logging of the testing
	"""
	my_file = open(trace_name, 'w')
	for line in trace:
		my_file.writelines(line)
		my_file.write('\n')
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
			statement = f.read()
			statement_list.append((int(files[3:]), statement))
		n += 1
	return statement_list

def create_arbo(folder):
	"""Create a List sorted by alphabetical order with the 
		content of the folder given as parameter.
	:param folder: A string containing the folder to list files.
	:rtype: A list of the files in folder.
	"""
	return sorted(os.listdir(folder), key=str.lower)

def set_folders(reference, test):
	"""Sets list for ref and test
	"""
	folder_reference = reference
	folder_test = test
	arbo_test = create_arbo(folder_test)
	arbo_ref = create_arbo(folder_reference)
	if '.git' in arbo_test:
		arbo_test.remove('.git')
	if 'trace.txt' in arbo_test:
		arbo_test.remove('trace.txt')
	list_ref = read_arbo(arbo_ref, folder_reference)
	list_test = read_arbo(arbo_test, folder_test)
	return list_ref, list_test

def compute_delta(ref, test):
	"""Compute the delta between ref and test using diffLib.
	Usage:
		>>> delta1, delta2 = compute_delta(ref, test)
	:param ref: reference output.
	:param test: test output.
	:rtype delta1 and delta2 (string).
	"""
	diff = difflib.ndiff(ref, test)
	delta1 = ''.join(x[2:] for x in diff if x.startswith('- '))
	diff = difflib.ndiff(ref, test)
	delta2 = ''.join(x[2:] for x in diff if x.startswith('+ '))
	return delta1, delta2

def handler(signum, frame):
	raise Exception('Timeout')

def compute_moulinette(list_ref, list_test, trace_origin=[]):
	"""Logic of the mouli.
	Usage:
		>>> ref, test = 'SQLDAY01_ref', 'SQLDAY01_test'
		>>> list_ref, list_test = set_folders(ref, test)
		>>> compute_moulinette(list_ref, list_test)
	"""
	fails = 0
	fail = []
	trace = []
	trace.append(trace_origin)
	for elem_ref, elem_test in zip(list_ref, list_test):
		print('Correcting exercice n°{}'.format(elem_test[0]))
		trace.append('Correcting exercice n°{}'.format(elem_test[0]))
		ref = exec_sql_script(elem_ref[1]).splitlines()
		test = exec_sql_script(elem_test[1]).splitlines()
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(10)
		try:
			delta1, delta2 = compute_delta(ref, test)
			if delta1 or delta2:
				fails += 1
				fail.append(elem_test[0])
				print(bcolors.FAIL + 'OUTPUT DIFFER [KO]\n' + bcolors.ENDC, 'you:\t\t', delta2[:200], '\nexpected:\t', delta1[:200], sep='')
				trace.append('OUTPUT DIFFER [KO]\n' + 'you:\t\t ' + delta2 + ' ' + '\nexpected:\t ' + delta1)
				trace.append('Your SQL statement is probably false\n>>> \"{}\"\n'.format(elem_test[1].strip('\n')))
			else:
				print(bcolors.OKGREEN + 'Test Passed [OK]' + bcolors.ENDC)
				trace.append('Test Passed [OK]')
				pass
		except Exception as e:
			fail.append(elem_test[0])
			print(bcolors.FAIL + 'Test CRASH [KO]', str(e), bcolors.ENDC)
			trace.append('Test CRASH: ' + str(e))
			pass
	t = ''.join(str(fail))
	trace.append('\nEnd of the tests '+ str(fails)+ ' fails out of '+ str(len(list_test))+ ' exercises. Total is ' + str(len(list_ref))+ '\n'+ 'Exercices failed: '+ t)
	print(bcolors.WARNING + '\nEnd of the tests', fails, 'fails out of', len(list_test), 'exercises\n', 'Exercices failed: ', fail)
	print('\n\nSee trace.txt to view your errors' + bcolors.ENDC)
	return trace

def call_mouli_for_all(folder, ref_folder='test/SqlDay01/'):
	"""this function will call the moulinette for all student in folder
	if this function is called no reference is given so the reference folder is by default ''
	:param folder: A string that contain the name of the folder for all students
	"""
	a =	create_arbo(folder)
	for files in a:
		list_ref, list_test = set_folders(ref_folder, folder+files+'/')
		trace = compute_moulinette(list_ref, list_test, trace_origin=folder+files+'/')
		write_trace(trace, folder+files+'/'+'trace.txt')

if __name__ == "__main__":
	if '-h' in sys.argv[1:]:
		help(0)
	try:
		if len(sys.argv) == 2:
			call_mouli_for_all(sys.argv[1])
			exit(0)
		if len(sys.argv) > 3 or len(sys.argv) < 2:
			raise Exception('Invalid number of arguments')
		list_ref, list_test = set_folders(sys.argv[1], sys.argv[2])
	except Exception as e:
		print('Error:', e)	
		help(84)
	trace = compute_moulinette(list_ref, list_test)
	write_trace(trace)
	sys.exit(0)
