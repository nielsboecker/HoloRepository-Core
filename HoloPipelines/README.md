# HoloPipelines

## Requirements:
Python 3.7 or above

## Dependencies and installation:
Dependencies can be installed by using pip command as follow
```
pip install -r requirements.txt
```

Some dependencies are not available through pip, they are listed below with their installation instructions

**GDCM (Debian/Ubuntu)**
```
sudo apt-get install libgdcm2.8
sudo apt-get install libcdcm-tools
```

Verify installation success and see if `gdcmdump` or `gdcmconv` commands can be executed.

The final 2 dependencies can be installed using Node.js package manager. Please make sure to have the latest version of npm installed.

**obj2gltf**  https://github.com/AnalyticalGraphicsInc/OBJ2GLTF
```
npm install -g obj2gltf
```

**glTF Pipeline** https://github.com/AnalyticalGraphicsInc/gltf-pipeline
```
npm install -g gltf-pipeline
```

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
- this script has a built in help which will print out
```
usage: pipelineController.py [-h] [-c CONFIG] [-l] [-i INFO]
                             [-p [PARAM [PARAM ...]]]
                             [pipelineID]

Selct pipeline to process

positional arguments:
  pipelineID            ID of pipeline

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to pipeline config file relative to
                        pipelineController
  -l, --ls              list all the available piplines
  -i INFO, --info INFO  get info from pipeline's name
  -p [PARAM [PARAM ...]], --param [PARAM [PARAM ...]]
                        parameters for pipeline e.g. dicom folder name or HU
                        threshold
```

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
Note: Tests downloads sample files during the testing process. These files can be deleted by running *cleanUp.py*

