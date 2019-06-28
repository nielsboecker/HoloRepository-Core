import subprocess
import fileHandler

success = True
slash = fileHandler.slash

def main(fname="-h", delObj=False):
	print("hey imma run:           " + "obj2gltf " + str(fileHandler.outputPath + "OBJs" + slash + fname) + " -b")
	success = subprocess.run(["obj2gltf", "-i", str(fileHandler.outputPath + "OBJs" + slash + fname), "-b"])
	#success = subprocess.run(["pwd"])
	if success:
		success = subprocess.run(["mv", str(fileHandler.outputPath + "OBJs" + slash + fname.replace(".obj", ".glb")), str(fileHandler.outputPath + "GLBs" + slash)])
		if delObj:
			success = subprocess.run(["rm", str(fileHandler.outputPath + "OBJs" + slash + fname)])
		print("conversion complete")
	else:
		print("conversion failed")

if __name__ == '__main__':
	main()