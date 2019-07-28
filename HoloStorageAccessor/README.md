# HoloStorageAccessor
The HoloStorage is a cloud-based storage for medical 3D models and associated metadata. Entirely hosted on Microsoft Azure, a FHIR server stores the structured medical data and a Blob Storage server provides for the binary holographic data. With the HoloStorageAccessor, we provide an enhanced facade, offering a consistent interface to the HoloStorage and translating the public REST API to internal FHIR queries. To facilitate development of 3rd party components, the interface comes with an interactive OpenAPI documentation.


## Description
<img src="https://user-images.githubusercontent.com/11090412/62010808-49d5b180-b167-11e9-9ce7-7335aa616926.png" alt="screenshot" height="350" align="left" />
To protect the HoloStorage and hide concrete implementation details, such as which FHIR resources are used to store data internally, the HoloStorage-Accessor provides a consistent and unified interface to the data, and the single entry-point for 3rd party systems. As such, it acts as a façade. However, it also performs some more complex business logic, like translating calls to a minimalistic interface to FHIR queries and building complex queries, potentially filtering and aggregating results.

The REST API is being carefully designed, so that it not only satisfies the requirements of the HoloPipelines’ artefacts, but also supports adjacent projects (DepthVisor, Annotator) and any future projects in this context. We strive to find a balance between an open, generic interface and enforcing enough relevant data to effectively query and utilise the data.


## Technologies
The API specification is written with OpenAPI v3.

The Accessor component is implemented in Go.

> TODO: Enhance this section?


# API specification
The API specification can be found in the `api/` directory. A deployed version of the interactive documentation is available [here](https://app.swaggerhub.com/apis/boonwj/HoloRepository/).


## Development
> TODO: Add this section


## Testing
> TODO: Add this section


## Build and deployment
> TODO: Add this section


## Contact and support
This component is owned by [boonwj](https://github.com/boonwj). Please get in touch if you have any questions. For change requests and bug reports, please open a new issue.