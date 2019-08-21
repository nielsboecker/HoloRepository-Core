<p align="center">
  <img width="300" alt="HoloRepository logo" src="https://user-images.githubusercontent.com/11090412/62009421-f491a400-b156-11e9-98ca-408dc2fab7e8.png">
  <p align="center">
    A system for transforming medical imaging studies such as CT or MRI scans into 3-dimensional holograms, storing data on a cloud-based platform and making it available for other systems.
  </p>
  <p align="center">
    <a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev">
      <img src="https://img.shields.io/azure-devops/build/MSGOSHHOLO/84bcb432-f279-452c-a53c-37df0f28baf0/1" alt="Build status"/>
    </a>
    <a href="https://www.codefactor.io/repository/github/nbckr/holorepository-core">
      <img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/nbckr/HoloRepository-Core" />
    </a>
    <a href="https://github.com/nbckr/HoloRepository-Core/issues">
      <img alt="GitHub issues" src="https://img.shields.io/github/issues/nbckr/HoloRepository-Core" />
    </a>
    <a href="https://github.com/nbckr/HoloRepository-Core/pulls">
      <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/nbckr/HoloRepository-Core" />
    </a>
    <a href="https://github.com/nbckr/HoloRepository-Core/blob/master/LICENSE">
      <img alt="GitHub" src="https://img.shields.io/github/license/nbckr/HoloRepository-Core" />
    </a>
  </p>
</p>

## Table of contents

- [Background](#background)
- [System overview](#system-overview)
  - [HoloRepositoryUI](#holorepositoryui)
  - [HoloPipelines](#holopipelines)
  - [HoloStorage](#holostorage)
  - [HoloStorageAccessor](#holostorageaccessor)
  - [HoloStorageConnector](#holostorageconnector)
  - [HoloRepository Demo application](#holorepository-demo-application)
  - [Other tools](#other-tools)
  - [Integration with other projects](#integration-with-other-projects)
- [Code organisation](#code-organisation)
- [Development](#development)
  - [Get started](#get-started)
  - [Set up the environment](#set-up-the-environment)
  - [System integration](#system-integration)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Background

Recent technical advancements in the realm of augmented reality (AR) and the availability of consumer head-mounted display (HMD) devices such as the Microsoft HoloLens have opened a wealth of opportunities for healthcare applications, particularly in medical imaging. Several approaches have been proposed to transform imaging studies, such as CT or MRI scans, into three-dimensional models which can be inspected and manipulated in an AR experience [1–4]. Generally, all studies agree that the technology is very promising and may even revolutionise the practice of medicine [5]. However, virtually every existing workflow relies on significant manual guidance to conduct steps like segmentation or conversion to polygonal models.

Neural networks can help automate many tedious tasks and are increasingly used in medical imaging. Architectures such as the 3D U-Net [6] generate models which autonomously create segmentation maps, even with relatively little training data. However, translating these advancements from theory to clinical practice has unique challenges: The source code may not be available, documentation may be missing or require too much technical knowledge. Furthermore, different operating systems, software packages and dependencies obstruct successful usage [7].

With the HoloRepository project, we intend to build the technical base for a seamless workflow that allows practitioners to generate 3D models from imaging studies and access them in an AR setting with as little manual involvement as possible. Pre-trained neural networks can be packaged into shareable Docker containers and accessed with a unified interface. Additionally, the Fast Healthcare Interoperability Resources (FHIR) standard, which is rapidly being adapted and also has a significant impact on the field of radiology [8], will connect the 3D models with existing patient health records.

<details>
  <summary><b>Show references</b></summary>

>  * [1]	Smith CM. Medical Imaging in Mixed Reality: A holographics software pipeline. University College London, 2018.
>  * [2]	Pratt P, Ives M, Lawton G, Simmons J, Radev N, Spyropoulou L, et al. Through the HoloLensTM looking glass: augmented reality for extremity reconstruction surgery using 3D vascular models with perforating vessels. Eur Radiol Exp 2018;2:2. doi:10.1186/s41747-017-0033-2.
>  * [3]	Affolter R, Eggert S, Sieberth T, Thali M, Ebert LC. Applying augmented reality during a forensic autopsy—Microsoft HoloLens as a DICOM viewer. Journal of Forensic Radiology and Imaging 2019;16:5–8. doi:10.1016/j.jofri.2018.11.003.
>  * [4]	Page M. Visualization of Complex Medical Data Using Next-Generation Holographic Techniques 2017.
>  * [5]	Beydoun A, Gupta V, Siegel E. DICOM to 3D Holograms: Use Case for Augmented Reality in Diagnostic and Interventional Radiology. SIIM Scientific Session Posters and Demonstrations 2017:4.
>  * [6]	Çiçek Ö, Abdulkadir A, Lienkamp SS, Brox T, Ronneberger O. 3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation. ArXiv:160606650 [Cs] 2016.
>  * [7]	Beers A, Brown J, Chang K, Hoebel K, Gerstner E, Rosen B, et al. DeepNeuro: an open-source deep learning toolbox for neuroimaging. ArXiv:180804589 [Cs] 2018.
>  * [8]	Kamel PI, Nagy PG. Patient-Centered Radiology with FHIR: an Introduction to the Use of FHIR to Offer Radiology a Clinically Integrated Platform. J Digit Imaging 2018;31:327–33. doi:10.1007/s10278-018-0087-6.
</details>

## System overview

![HoloRepository system overview](https://user-images.githubusercontent.com/11090412/62009929-4852bc00-b15c-11e9-9e2a-6d7f667a286e.png)

The HoloRepository ecosystem consists of multiple sub-systems and remains open to future extensions. Currently, core components are:

### [HoloRepositoryUI](https://github.com/nbckr/HoloRepository-Core/tree/master/HoloRepositoryUI)<a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloRepositoryUI%20-%20Client" alt="Client build status" align="right" /></a><a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloRepositoryUI%20-%20Server" alt="Server build status" align="right" /></a>

A web-based application that allows practitioners to browse their patients and manage the generation of 3D models sourced from imaging studies like CT or MRI scans. The client-side application is accompanied by an API server that is responsible for communicating with the other components.

### [HoloPipelines](https://github.com/nbckr/HoloRepository-Core/tree/master/HoloPipelines)<a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloPipelines%20-%20Core" alt="HoloPipelines core build status" align="right" /></a><a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloPipelines%20-%20Models" alt="HoloPipelines models build status" align="right" /></a>

A cloud-based service that performs the automatic generation of 3D models from 2D image stacks. Pre-trained neural network models are deployed and accessed with this component alongside traditional techniques like Hounsfield value thresholding.

### HoloStorage

A cloud-based storage for medical 3D models and associated metadata. Entirely hosted on Microsoft Azure, a FHIR server stores the structured medical data and a Blob Storage server provides for the binary holographic data.

### [HoloStorageAccessor](https://github.com/nbckr/HoloRepository-Core/tree/master/HoloStorageAccessor)<a href="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_build/latest?definitionId=1&branchName=dev"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloStorageAccessor" alt="HoloStorageAccessor build status" align="right" /></a>

An enhanced facade, offering a consistent interface to the HoloStorage and translating the public REST API to internal FHIR queries. To facilitate development of 3rd party components, the interface comes with an interactive OpenAPI documentation.

### [HoloStorageConnector](https://github.com/nbckr/HoloRepository-HoloLens/tree/master/HoloStorageConnector)

A Unity library handling the runtime network connections from HoloLens applications to the HoloStorage. Distributed as a separate UnityPackage, this is meant to facilitate development of 3rd party applications that plug into the HoloRepository ecosystem.

### [HoloRepository demo application](https://github.com/nbckr/HoloRepository-HoloLens/tree/master/HoloRepositoryDemoApplication)

A simple application that demonstrates how to dynamically access 3D models stored in the HoloStorage. The scenes can be distributed alongside the Connector library and serve as examples and interactive documentation.

### [Other tools](https://github.com/nbckr/HoloRepository-Core/tree/master/Misc)

Several scripts and tools were developed to help perform tasks, for instance test data generation or deployment automation.

### Integration with other projects

The system is designed to enable other systems to integrate. Some current projects plugging into the system are DepthVisor, Annotator and SyntheticDataGenerator.

## Code organisation

Most of the components are kept here in the [HoloRepository-Core](https://github.com/nbckr/HoloRepository-Core) mono-repository. The sub-directories correspond to sub-components as described above. The only exception are the components that are developed in Unity/C#, they are separately kept in the [HoloRepository-HoloLens](https://github.com/nbckr/HoloRepository-HoloLens) repository.

## Development

### Get started

To get started, you should clone both relevant git repositories:
```shell
$ git clone git@github.com:nbckr/HoloRepository-Core.git
$ git clone git@github.com:nbckr/HoloRepository-HoloLens.git
```

Next, it is highly recommended to expolore the `README`s that are provided for each component.

### Set up the environment

The different components are developed in different languages and making use of different tools, so your next step should be inspecting the `README` in the respective directory.

#### Pre-commit hooks

As some languages, like Python, are used for multiple components, we use a common tool to enforce coherent coding style. The code formatter [black](https://github.com/psf/black) is checking new commits via a pre-commit hook. Steps to set it up:

1. Install developer dependencies with `pipenv install --dev` or `pip install -r requirements-dev.txt` in the project root directory
2. Setup pre-commit hooks with `pre-commit install`

For the TypeScript portions, similar tooling is used. To set it up, follow the instructions in the respective sub-directories.

#### CodeFactor

CodeFactor is another tool we use to ensure high code quality. It will run automatically on GitHub for any activated branches, as well as for all pull requests. If the service finds any issues, please fix them before we will continue to consider the pull request.

_Note: The `tslint.json` config is solely for this purpose. The actual JavaScript / TypeScript code is linted with ESLint, given that TSLint will be deprecated. Use the TSLint config only when CodeFactor's default rules are unreasonable._

### System integration

#### Ports and interfaces

The different components are meant to be deployed independently. They communicate via REST APIs, which are documented in the sub-directories' `README`s. For development, the system can be run on the same host, using these default ports:
```c
HoloRepositoryUI/client:  3000
HoloRepositoryUI/server:  3001
HoloPipelines/core:       3100
HoloStorageAccessor:      3200
HoloPipelines/models:     5000, 5001, 5002, ...
```

#### Run system in docker-compose

As the system comprises multiple separate components, it can be helpful to use docker-compose to locally start all of them at once, for instance to perform integration tests or develop a new component.

Note: To successfully start the Accessor, you need to provide the relevant configuration in `./HoloStorageAccessor/config.env` (see the sub-component's `README` for more information).

This will also reflect the current state of the sub-components' `Dockerfile`s. To build and start all images (if they haven't been build already), run:
```shell
$ docker-compose --file docker-compose.dev.yml up
Starting holorepository-core_holorepository-ui-client_1                      ... done
Starting holorepository-core_holopipelines-models__dense_vnet_abdominal_ct_1 ... done
Starting holorepository-core_holorepository-ui-server_1                      ... done
Creating holorepository-core_holostorage-accessor_1                          ... done
```

In cases where only selective services are required, they can be started by specifying the service name
```shell
$ docker-compose -f docker-compose.dev.yml up holorepository-ui-client holorepository-ui-server
Starting holo-repo-clean_holorepository-ui-server_1 ... done
Starting holo-repo-clean_holorepository-ui-client_1 ... done
```

Force a rebuild by replacing `docker-compose up` with `docker-compose build`.

You can also just run a single component or a selection of components, but still use the provided configurations, port mappings etc. from the `docker-compose` file for convenience:
```shell
$ docker-compose --file docker-compose.dev.yml up holostorage-accessor holorepository-ui-server
```

Lastly, it is also possible to start the whole system except for one component, which will allow you to develop this component and, for instance, manually run it in dev mode.
```shell
$ docker-compose --file docker-compose.dev.yml up --scale holostorage-accessor=0
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. For feature requests, please also open an issue.

## Acknowledgements

Built at [University College London](https://www.ucl.ac.uk/) in cooperation with [Microsoft](https://www.microsoft.com/en-gb) and [GOSH DRIVE](https://www.goshdrive.com/).

Academic supervision: Prof. Dean Mohamedally, Prof. Neil Sebire

Product logo is derived from a work by <a href="https://www.freepik.com/">Freepik</a> at <a href="https://www.flaticon.com/">www.flaticon.com</a>.

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
