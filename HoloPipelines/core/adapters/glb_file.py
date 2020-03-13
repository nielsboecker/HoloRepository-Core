"""
This module contains functionality related to writing a mesh to disk as an OBJ file.
"""
import numpy as np
import math

import trimesh
from trimesh import visual


import logging

def write_mesh_as_glb(
    meshes, output_obj_file_path: str, metadata={}
) -> None:
    scene = trimesh.Scene(metadata=metadata)
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0],
                           faces=mesh[1],
                           vertex_normals=mesh[2])

        mesh2.apply_transform(trimesh.transformations.rotation_matrix(90,(0,0,1)))
        scene.add_geometry(mesh2)
    scene.export(output_obj_file_path)


def write_mesh_as_glb(
        meshes, output_obj_file_path: str,colour, metadata={}
) -> None:
    scene = trimesh.Scene(metadata=metadata)
    index = 0
    for mesh in meshes:
        mesh2 = trimesh.Trimesh(vertices=mesh[0],
                                faces=mesh[1],
                                vertex_normals=mesh[2])

        mesh2.visual.material = trimesh.visual.material.SimpleMaterial(
            diffuse=np.asarray(colour[index]))
        print(colour[index])
        mesh2.apply_transform(trimesh.transformations.rotation_matrix(90, (0, 0, 1)))
        scene.add_geometry(mesh2)
        index += 1
    scene.export(output_obj_file_path)


