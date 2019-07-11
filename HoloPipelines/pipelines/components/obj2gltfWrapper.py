import subprocess
import pathlib

success = True
cwd = pathlib.Path.cwd()
objPath = cwd.joinpath("output", "OBJ")
glbPath = cwd.joinpath("output", "GLB")

def main(fname="-h", delObj=False):
	success = subprocess.run(["obj2gltf", "-i", str(objPath.joinpath(fname)), "-b"])
	if success:
		success = subprocess.run(["mv", str(objPath.joinpath(fname.replace(".obj", ".glb"))), str(glbPath)])
		if delObj:
			success = subprocess.run(["rm", str(objPath.joinpath(fname))])
		if "__temp__" in str(fname):
			success = subprocess.run(["mv", str(glbPath.joinpath(fname.replace(".obj", ".glb"))), str(glbPath.joinpath(str(fname).replace(".obj", ".glb").replace("__temp__", "")))])
		print("obj2gltf: conversion complete")
	else:
		print("obj2gltf: conversion failed")

if __name__ == '__main__':
	main()