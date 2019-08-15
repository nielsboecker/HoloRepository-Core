from components import compCommonPath
from components import compJobStatus
from components import compDcm2nifti
from components.lungSegment.main import main as lungSegment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
from datetime import datetime
import pathlib
import sys
import json


def main(job_ID, dicom_path, output_glb_path, info_for_accessor):
    compJobStatus.update_status(job_ID, "Pre-processing")
    generated_nifti_path = compDcm2nifti.main(
        str(dicom_path),
        str(compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicom_path).parts[-1]))),
    )  # convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generated_segmented_lung_nifti_path = lungSegment(
        generated_nifti_path, str(compCommonPath.nifti.joinpath("segmentedLungs"))
    )
    generated_numpy_list = compNifti2numpy.main(
        str(pathlib.Path(generated_segmented_lung_nifti_path).joinpath("lung.nii.gz"))
    )

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        0.5,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.update_status(job_ID, "3D format conversion")
    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    print("lungDicom2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Finished")
    info_for_accessor = json.loads(info_for_accessor)
    compPostToAccesor.send_file_request_to_accessor(
        info_for_accessor["bodySite"] + "apply on generic bone segmentation",
        output_glb_path,
        info_for_accessor["description"],
        info_for_accessor["bodySite"],
        info_for_accessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        info_for_accessor["author"],
        info_for_accessor["patient"],
    )


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
