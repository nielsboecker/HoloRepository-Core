# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
from pipelines.adapters.nifti_file import read_nifti_as_np_array_and_normalise
from pipelines.services.format_conversion import convert_numpy_to_obj
import pathlib
import logging

logging.basicConfig(level=logging.INFO)


def main(inputNiftiPath, outputObjPath, threshold, flipNpy=False):
    generatedNumpyList = read_nifti_as_np_array_and_normalise(str(pathlib.Path(inputNiftiPath)))
    generatedObjPath = convert_numpy_to_obj(
        generatedNumpyList, threshold, str(pathlib.Path(outputObjPath))
    )
    logging.info("nifti2obj: done, obj saved to {}".format(generatedObjPath))
