# this pipeline may be removed in the future as obj is not used to display 3D model on hololens
import pipelines.services.format_conversion
from pipelines.services.format_conversion import convert_numpy_to_obj, convert_nifty_to_numpy
import pathlib
import logging

logging.basicConfig(level=logging.INFO)


def main(inputNiftiPath, outputObjPath, threshold, flipNpy=False):
    generatedNumpyList = convert_nifty_to_numpy(str(pathlib.Path(inputNiftiPath)))
    generatedObjPath = convert_numpy_to_obj(
        generatedNumpyList, threshold, str(pathlib.Path(outputObjPath))
    )
    logging.info("nifti2obj: done, obj saved to {}".format(generatedObjPath))
