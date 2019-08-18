import pathlib


def write_mesh_as_obj(verts, faces, norm, output_obj_path):
    # Workaround according to https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python
    faces = (faces + 1)

    with open(str(pathlib.Path(output_obj_path)), "w") as obj_file:
        for item in verts:
            obj_file.write("v {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in norm:
            obj_file.write("vn {0} {1} {2}\n".format(item[0], item[1], item[2]))

        for item in faces:
            obj_file.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0], item[1], item[2]))
