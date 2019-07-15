# PIPELINE

## Requirements:
Python 3.7 or above

## Dependencies and installation:
Dependencies can be installed by using pip command as follow
```
pip install -r requirements.txt
```

Some dependencies are not available through pip, they are listed below with their installation instructions

**GDCM (Unix)** *This works, but should to be replaced with pacman or other package manager for ease of use*
```
 git clone --branch release git://git.code.sf.net/p/gdcm/gdcm
 mkdir gdcmbin
 cd gdcmbin
 ccmake ../gdcm
```
   [select your configuration] make sure to select *GDCM_BUILD_APPLICATIONS* and *GDCM_BUILD_EXAMPLES*
```
 Press 'c' (configure), Press 'g' (generate)
 make
```
Double check to see if installation is successful by running
```
 gdcmdump
```
or
```
 gdcmconv
```
If command is not found then please make sure to add to PATH

The final 2 dependencies can be installed using Node.js package manager. Please make sure to have the latest version of npm installed.

**obj2gltf**  https://github.com/AnalyticalGraphicsInc/OBJ2GLTF
```
 npm install -g obj2gltf
```

**glTF Pipeline** https://github.com/AnalyticalGraphicsInc/gltf-pipeline
```
 npm install -g gltf-pipeline
```

(optional)Run *setupDirectory.py* to download sample dicom and nifti files which can be used for manual testing.

Downloaded files from *setupDirectory.py* and all the produced 3D models can be deleted by running *cleanUp.py*

## Usage:
Example
```
python pipelineController.py p4 -p 3_Axial_CE
```
- p4: pipeline ID. In this case to segment lung and generate glb from it
- -p 3_Axial_CE: param(s) for the specific pipeline, in this case a directory for an upper ct scan from medicalScans/dicom

```
python pipelineController.py -h
```
- this script has a built in help

## Testing:
Testing can be done by using pytest:
```
pip install pytest
pip install pytest-cov
```
Then navigate to /HoloRepository-Core/HoloPipelines and run:
```
pytest --cov
```

### Refs:
- https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/      14/06/19
- https://wiki.idoimaging.com/index.php?title=Sample_Data   seems like the have some dicoms and a bit of niftis we can playwith    17/06/19
- https://www.researchgate.net/post/What_is_the_easiest_way_to_batch_resize_DICOM_files to down sample dicoms, incase if they're too large  17/06/19
- https://stackoverflow.com/questions/55560243/resize-a-dicom-image-in-python      this one is for python. the one above is for mathlab, i didn't see
- https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python   export mesh to obj   17/06/19
- (optional) new marching cubes with smoothing (?) https://github.com/ilastik/marching_cubes
