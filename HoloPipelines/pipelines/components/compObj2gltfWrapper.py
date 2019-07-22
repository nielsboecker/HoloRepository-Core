import subprocess
import pathlib
from shutil import move
import os
import sys

newCwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True
cwd = pathlib.Path.cwd()
objPath = cwd.joinpath("output", "OBJ")
glbPath = cwd.joinpath("output", "GLB")

def main(inputObjPath, outputGlbPath, deleteOriginalObj=False, compressGlb=False):
	success = subprocess.run(["obj2gltf", "-i", str(pathlib.Path(inputObjPath)), "-b"])#TODO check return
	if success:
		outputGlbPath = str(pathlib.Path(outputGlbPath))
		move(str(pathlib.Path(inputObjPath)).replace(".obj", ".glb"), outputGlbPath)
		if deleteOriginalObj:
			os.remove(str(pathlib.Path(inputObjPath)))
		print("obj2gltf: conversion complete")

		#Draco compression. note that draco compresssion in viewers may not be common
		if compressGlb:
			subprocess.call("gltf-pipeline -i " + outputGlbPath + " -o " + outputGlbPath + " -d", cwd=newCwd, shell=True)
			print("obj2gltf: Draco compression finished")
	else:
		sys.exit("obj2gltf: conversion failed")
	return outputGlbPath
	print("obj2gltf: done")

if __name__ == '__main__':
	print("component can't run on its own")