# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
from pipelines.components import compNifti2numpy
from pipelines.components import compJobStatus
from pipelines.components import compNumpy2obj
import pathlib
import sys


def main(job_ID, input_nifti_path, output_obj_path, threshold, flipNpy=False):
    compJobStatus.update_status(job_ID, "Pre-processing")
    generated_numpy_list = compNifti2numpy.main(str(pathlib.Path(input_nifti_path)))

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list, threshold, str(pathlib.Path(output_obj_path))
    )

    print("nifti2obj: done, obj saved to {}".format(generated_obj_path))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
