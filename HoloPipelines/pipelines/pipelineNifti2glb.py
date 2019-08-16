# pipeline left in current state (work with local files) as unsure if there's a use case where user can download nii from PACS
# could be left as is for internal use? Keep this file but delete index from pipelineList.json?

# do i need status update on this 'internal' pipeline?
from pipelines.components import compJobStatus
from pipelines.components import compNifti2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compJobPath
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
        compJobPath.make_str_job_path(job_ID, ["temp", "temp.obj"]),
    )

    compJobStatus.update_status(job_ID, "3D format conversion")
    generated_glb_path = compObj2glbWrapper.main(
        generated_obj_path,
        str(pathlib.Path(output_glb_path)),
        delete_original_obj=True,
        compress_glb=False,
    )
    print("nifti2glb: done, glb saved to {}".format(generated_glb_path))
    compJobStatus.update_status(job_ID, "Posting data")
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
    compJobStatus.update_status(job_ID, "Cleaning up")
    compJobPath.clean_up(job_ID)
    compJobStatus.update_status(job_ID, "Finished")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
