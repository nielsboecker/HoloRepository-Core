"""
This module contains the functionality of the abdominal_organs_segmentation pipeline
of splitting the combined result into multiple sub-results.

Currently this module is not in used. The current implementation of
this module is unable to provide an appropriate name to each output
,and of which we feel that it will not provide much useful information
for the user. Under time constrain, we were unable to provide each output with colour
and merge it back together and have every organs with different colours in a single
3D model as we have originally envisioned. So, in the end we decided to provide the user
with a single output instead of 8 separate ones.
"""

import logging
from typing import Optional

import numpy as np

from core.adapters.glb_file import convert_obj_to_glb_and_write
from core.adapters.obj_file import write_mesh_as_obj
from core.services.marching_cubes import generate_mesh


def get_organ_name(hu_value: int) -> Optional[str]:
    """
    Maps the "HU value" to the according organ name. Note that this is just an
    assumption. The paper (Automatic multi-organ segmentation on abdominal CT with
    dense v-networks https://doi.org/10.1109/TMI.2018.2806309) doesn't actually state
    the mapping. But it always uses this order, thus the assumption. Also, I manually
    compared outputs with Google image search :-) Note that 0 is how the authors
    encoded empty space around the organs.
    """
    organs = [
        None,
        "Spleen",
        "Left_Kidney",
        "Gallbladder",
        "Esophagus",
        "Liver",
        "Stomach",
        "Pancreas",
        "Duodenum",
    ]
    return organs[hu_value]


def split_to_separate_organs(input: np.ndarray, output_directory_path: str) -> None:
    logging.info("Separating different organs")
    # Each segmented organ has been masked with a unique "HU value"
    unique_hu_values = np.unique(input)

    # Value 0 is the empty space, remove
    unique_hu_values = unique_hu_values[1:]

    for hu_value in unique_hu_values:
        organ_name = get_organ_name(hu_value)
        logging.info(f"Processing organ: {organ_name} [{hu_value}]")
        organ_mask = input == hu_value
        organ_mask = organ_mask.astype(int)
        threshold = 0

        obj_output_path = f"{output_directory_path}/Organ_{hu_value}.obj"
        glb_output_path = f"{output_directory_path}/Organ_{hu_value}.glb"
        verts, faces, norm = generate_mesh(organ_mask, threshold)
        write_mesh_as_obj(verts, faces, norm, obj_output_path)

        convert_obj_to_glb_and_write(obj_output_path, glb_output_path)
