from pipelines.components import compJobStatus
from pipelines.components import compCommonPath
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components.compJobStatusEnum import JobStatus
from pipelines.components import compCombineInfoForAccesor
from pipelines.components import compNifti2numpy
from pipelines.components import compDcm2nifti
from pipelines.components.compGetPipelineListInfo import get_pipeline_list
import pipelines.components.lungSegment.main as comp_lung_segment

import pathlib
import sys
import logging


def main(job_ID, dicom_path, output_glb_path, meta_data):
    compJobStatus.update_status(job_ID, JobStatus.PPREPROCESSING.name)
    generated_nifti_path = compDcm2nifti.main(
        str(dicom_path),
        str(compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))),
    )  # convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder

    generated_segmented_lung_nifti_path = comp_lung_segment(
        generated_nifti_path, str(compCommonPath.nifti.joinpath("segmentedLungs"))
    )

    generated_numpy_list = compNifti2numpy.main(
        str(pathlib.Path(generated_segmented_lung_nifti_path).joinpath("lung.nii.gz"))
    )

    compJobStatus.update_status(job_ID, JobStatus.MODELGENERATION.name)

    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        0.5,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.update_status(job_ID, JobStatus.MODELCONVERSION.name)

    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    logging.debug("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Finished")
    list_of_pipeline = get_pipeline_list()
    logging.debug("dicom2glb: done, glb saved to {}".format(generated_glb_path))
    meta_data = compCombineInfoForAccesor.add_info_for_accesor(
        meta_data,
        "apply on generic bone segmentation",
        "Generate with " + list(list_of_pipeline.keys())[1] + " pipeline",
        output_glb_path,
    )
    compJobStatus.update_status(job_ID, JobStatus.FINISHED.name)


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
