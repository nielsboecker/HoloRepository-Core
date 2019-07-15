import subprocess
import pathlib
from shutil import move as move
from os import remove as remove
from os import rename as rename
import os

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True
cwd = pathlib.Path.cwd()
objPath = cwd.joinpath("output", "OBJ")
glbPath = cwd.joinpath("output", "GLB")

def main(fname, delObj=False, compressGlb=True):#TODO remove delObj?
	success = subprocess.run(["obj2gltf", "-i", str(objPath.joinpath(fname)), "-b"])
	if success:
		#success = subprocess.run(["mv", str(objPath.joinpath(fname.replace(".obj", ".glb"))), str(glbPath)])
		newGlbPath = str(glbPath.joinpath(fname.replace(".obj", ".glb").replace("__temp__", "")))
		move(str(objPath.joinpath(fname.replace(".obj", ".glb"))), newGlbPath)#one line to solve all prob?
		if delObj:
			remove(str(objPath.joinpath(fname)))
		'''if "__temp__" in str(fname):
			#success = subprocess.run(["mv", str(glbPath.joinpath(fname.replace(".obj", ".glb"))), str(glbPath.joinpath(str(fname).replace(".obj", ".glb").replace("__temp__", "")))])
			move(str(glbPath.joinpath(fname.replace(".obj", ".glb"))), str(glbPath.joinpath(str(fname).replace(".obj", ".glb").replace("__temp__", ""))))
		'''
		print("obj2gltf: conversion complete")

		##########################    Draco compression using glTF Pipeline   ##############################
		if compressGlb:
			glbFname = fname.replace(".obj", ".glb")
			subprocess.call("gltf-pipeline -i " + newGlbPath + " -o " + newGlbPath + " -d", cwd=newCwd, shell=True)#TODO check statement
			print("obj2gltf: Draco compression finished")
		###################################################################################################
	else:
		print("obj2gltf: conversion failed")
		exit()
	print("obj2gltf: done")

if __name__ == '__main__':
	main()