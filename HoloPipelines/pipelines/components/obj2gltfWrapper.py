import subprocess
from components import fileHandler

success = True
slash = fileHandler.slash
objPath = fileHandler.objPath
glbPath = fileHandler.glbPath

def main(fname="-h", delObj=False):
	success = subprocess.run(["obj2gltf", "-i", str(objPath + fname), "-b"])
	if success:
		success = subprocess.run(["mv", str(objPath + fname.replace(".obj", ".glb")), str(glbPath)])
		if delObj:
			success = subprocess.run(["rm", str(objPath + fname)])
		if "__temp__" in str(fname):
			success = subprocess.run(["mv", str(glbPath + fname.replace(".obj", ".glb")), str(glbPath + str(fname).replace(".obj", ".glb").replace("__temp__", ""))])
		print("obj2gltf: conversion complete")
	else:
		print("obj2gltf: conversion failed")

if __name__ == '__main__':
	main()