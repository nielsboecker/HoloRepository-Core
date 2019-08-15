from pipelines.components import compJobStatus
from pipelines.components import compCommonPath
from pipelines.components import compDicom2numpy
from pipelines.components import compNumpy2obj
from pipelines.components import compObj2glbWrapper
from pipelines.components import compPostToAccesor
from pipelines.components import compCombineInfoForAccesor
from datetime import datetime
import pathlib
import json
import sys


def main(job_ID, dicom_folder_path, output_glb_path, info_for_accessor):
    compJobStatus.update_status(job_ID, "Pre-processing")
    print(output_glb_path)
    info_for_accessor = json.loads(info_for_accessor)
    generated_numpy_list = compDicom2numpy.main(str(pathlib.Path(dicom_folder_path)))
    threshold = 300

    compJobStatus.update_status(job_ID, "3D model generation")
    generated_obj_path = compNumpy2obj.main(
        generated_numpy_list,
        threshold,
        str(
            compCommonPath.obj.joinpath(
                str(pathlib.PurePath(dicom_folder_path).parts[-1])
            )
        )
        + ".obj",
    )
    compJobStatus.update_status(job_ID, "3D format conversion")
    generatedGlbPath = compObj2glbWrapper.main(
        generated_obj_path,
        output_glb_path,
        delete_original_obj=True,
        compress_glb=False,
    )
    print("dicom2glb: done, glb saved to {}".format(generatedGlbPath))
    compJobStatus.update_status(job_ID, "Finished")

    info_for_accessor = compCombineInfoForAccesor.add_info_for_accesor(
        info_for_accessor,
        "apply on generic bone segmentation",
        datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "Generate glb mesh from dicom",
        output_glb_path,
    )
    print(json.dumps(info_for_accessor))
    print(datetime.now())
    compPostToAccesor.send_file_request_to_accessor(info_for_accessor)
    print(datetime.now())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
