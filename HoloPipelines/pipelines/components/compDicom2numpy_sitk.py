import numpy as np
import pydicom as dicom
import os
import scipy.ndimage
import SimpleITK as sitk
import pathlib
import sys
import logging


def loadScan(scanPath):
    slices = [
        dicom.read_file(str(pathlib.Path(scanPath, s)))
        for s in os.listdir(str(scanPath))
    ]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slickThickness = np.abs(
            slices[0].ImagePositionscan[2] - slices[1].ImagePositionscan[2]
        )
    except Exception as e:
        logging.warning(
            "Unable to load sclice's image positon, using slice location instead: {}".format(
                str(e)
            )
        )
        slickThickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slickThickness

    return slices


def loadPixelArray(inputPath):
    reader = sitk.ImageSeriesReader()

    dicomName = reader.GetGDCMSeriesFileNames(inputPath)
    reader.SetFileNames(dicomName)

    image = reader.Execute()
    numpyArrayImage = sitk.GetArrayFromImage(image)

    return numpyArrayImage


def resample(dataPath, new_spacing=[1, 1, 1]):
    scan = loadScan(dataPath)
    image = loadPixelArray(dataPath)
    print("Shape before resampling\t", image.shape)
    # Determine current pixel spacing
    try:
        spacing = map(
            float,
            (
                [scan[0].SliceThickness]
                + [scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]]
            ),
        )
        spacing = np.array(list(spacing))
    except Exception as e:
        print(len(scan[0].PixelSpacing))
        print(
            "Pixel Spacing (row, col): (%f, %f) "
            % (scan[0].PixelSpacing[0], scan[0].PixelSpacing[1])
        )
        sys.exit("dicom2numpy: error loading scan: {}".format(str(e)))

    # calculate resize factor
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    print("Shape after resampling\t", image.shape)

    return image, new_spacing


def main(dicomPath):
    print("dicom2numpy: resampling dicom...")
    imgs_after_resamp, spacing = resample(dicomPath)
    print("dicom2numpy: resampling done")
    return imgs_after_resamp


if __name__ == "__main__":
    print("component can't run on its own")
