import os
import shutil
import pathlib
#import subprocess
from subprocess import Popen,PIPE,STDOUT
import sys

newCwd = os.getcwd()

'''try:
	output = subprocess.check_output('python pipelineController.py -c test/testList.json s0 -p 1', cwd=newCwd, shell=True).decode("utf-8")
	print("yoyoyoyoyoyoy" + output)
except subprocess.CalledProcessError as temp:
	print("hey its ya boi")
	print(str(temp.returncode))
	print(str(temp.output))
	print(temp.output)'''

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

class Capturing(list):
	def __enter__(self):
		self._stdout = sys.stdout
		sys.stdout = self._stringio = StringIO()
		return self
	def __exit__(self, *args):
		self.extend(self._stringio.getvalue().splitlines())
		del self._stringio
		sys.stdout = self._stdout

print("er hello?")

with Capturing() as output:
	try:
		thestuff = Popen(['python', 'pipelineController.py', '-c', 'test/testList.json', 's0', '-p', '1'], cwd=newCwd, shell=True, stderr=STDOUT, stdout=PIPE)#.decode("utf-8")
		t = out.communicate()[0],out.returncode
		print(t)
		'''print("yoyoyoyoyoyoy" + output)'''
	except:# subprocess.CalledProcessError as temp:
		'''print("hey its ya boi")
		print(str(temp.returncode))
		print(str(temp.output))
		print(temp.output)'''
	
print("yo this is what i got         " + str(output))





print("yoyoyoyoyoyoy test yo")
thestuff = Popen(['python', 'pipelineController.py', '-c', 'test/testList.json', 's0', '-p', '1'], cwd=newCwd, shell=True, stderr=STDOUT, stdout=PIPE)#.decode("utf-8")
t = out.communicate()[0],out.returncode
print(t)