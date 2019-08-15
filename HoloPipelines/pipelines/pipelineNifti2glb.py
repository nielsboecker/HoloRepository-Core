from components import compCommonPath
from components import compJobStatus
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
from components import compPostToAccesor
import pathlib
import sys
from datetime import datetime
import json


def main(job_ID, input_nifti_path, output_glb_path, threshold, info_for_accessor):
    compJobStatus.update_status(job_ID, "Pre-processing")
    generated_numpy_list = compNifti2numpy.main(str(pathlib.Path(input_nifti_path)))

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )

    compJobStatus.update_status(job_ID, "3D format conversion")
    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    print("nifti2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Finished")
    info_for_accessor = json.loads(info_for_accessor)
    compPostToAccesor.send_file_request_to_accessor(
        info_for_accessor["bodySite"] + "apply on generic bone segmentation",
        output_glb_path,
        info_for_accessor["description"],
        info_for_accessor["bodySite"],
        info_for_accessor["dateOfImaging"],
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from nifti",
        info_for_accessor["author"],
        info_for_accessor["patient"],
    )


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
