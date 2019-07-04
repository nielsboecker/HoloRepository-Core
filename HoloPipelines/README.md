# PIPELINE

## Requirements:
Python 3.7 or above
Dependencies can be installed by using or can be installed individually using the list from the section below
> pip install -r requirements.txt

## Dependencies:
- Anaconda https://www.anaconda.com/distribution/ (or alternatively, each dependencies can be install separately)
    - Numpy https://www.numpy.org/
    - Scipy https://www.scipy.org/
    - Matplotlib https://pypi.org/project/matplotlib/
- Pydicom https://pydicom.github.io/
- GDCM http://gdcm.sourceforge.net/wiki/index.php/Main_Page (conda install -c conda-forge gdcm)
- Skit-image https://scikit-image.org/
- Sklearn https://scikit-learn.org/stable/
- NiBabel https://nipy.org/nibabel/
- Nilearn https://nilearn.github.io/
- Dicom2Nifti (pip install dicom2nifti)
- (optional) new marching cubes with smoothing (?) https://github.com/ilastik/marching_cubes

## Usage:
> python pipelineController.py p4 -p 3_Axial_CE
- p4: pipeline ID. In this case to segment lung and generate glb from it
- -p 3_Axial_CE: param(s) for the specific pipeline, in this case a directory for an upper ct scan from medicalScans/dicom

> python pipelineController.py -h
- this script has a built in help

### Refs:
- https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
- https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
- https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
- https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
- https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19
