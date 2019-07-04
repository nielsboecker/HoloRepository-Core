import subprocess
from components import fileHandler

success = True
slash = fileHandler.slash
objPath = fileHandler.objPath
glbPath = fileHandler.glbPath

def main(fname="-h", delObj=False):
	#print("hey imma run:           " + "obj2gltf " + str(fileHandler.outputPath + "OBJs" + slash + fname) + " -b")
	success = subprocess.run(["obj2gltf", "-i", str(objPath + fname), "-b"])
	#success = subprocess.run(["pwd"])
	if success:
		success = subprocess.run(["mv", str(objPath + fname.replace(".obj", ".glb")), str(glbPath)])
		if delObj:
			success = subprocess.run(["rm", str(objPath + fname)])
		print("obj2gltf: conversion complete")
	else:
		print("obj2gltf: conversion failed")

if __name__ == '__main__':
	main()