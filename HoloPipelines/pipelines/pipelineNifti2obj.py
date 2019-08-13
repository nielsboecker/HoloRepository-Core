# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
from pipelines.components import compNifti2numpy
from pipelines.components import compJobStatus
from pipelines.components import compNumpy2obj
import pathlib
import sys
import logging


def main(job_id, input_nifti_path, output_obj_path, threshold, flip_npy=False):
    compJobStatus.update_status(job_id, "Pre-processing")
    generatedNumpyList = compNifti2numpy.main(str(pathlib.Path(input_nifti_path)))

    compJobStatus.update_status(job_id, "3D model generation")
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList, threshold, str(pathlib.Path(output_obj_path))
    )

    logging.info("nifti2obj: done, obj saved to {}".format(generatedObjPath))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
