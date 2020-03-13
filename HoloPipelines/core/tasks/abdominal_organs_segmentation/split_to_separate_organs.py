"""
This module contains the functionality of the abdominal_organs_segmentation pipeline
of splitting the combined result into multiple sub-results.

Currently, this component is unused, as the abdominal_organs_segmentation pipeline
yields only one output. This might be integrated later. Note that a further step will
need to be implemented, to either merge the 8 models back into 1, or make the pipeline
yield 8 outputs for one job.
"""

import logging
from typing import Optional

import numpy as np

from core.adapters.glb_file import write_mesh_as_glb
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
        meshes = [generate_mesh(organ_mask, threshold)]
        write_mesh_as_glb(meshes, obj_output_path)

