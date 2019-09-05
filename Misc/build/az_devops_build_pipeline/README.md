# Azure HoloRepository DevOps Build Pipelines Configuration

These are the configurations we set up to provide CI for the HoloRepository components.
They consist of multiple jobs, which in turn are assembled of multiple steps. Jobs can
be run in parallel on different servers.

![image](https://user-images.githubusercontent.com/11090412/64019201-624e3880-cb26-11e9-9da3-20d249117d19.png)

## Prerequisites

The jobs include steps which push Docker images to an Azure Container Registry (ACR),
for the Kubernetes deployment to use. To enable these steps, you will need to create
such an ACR (see [Deployment
README](https://github.com/nbckr/HoloRepository-Core/blob/master/Misc/deployment/az_kubes_setup/README.md)).
Then, you will need to modify your Azure DevOps project settings:

* Go to https://dev.azure.com/ucabnbo/<your-organisation>/_settings/
* Service Connections > New Service Connection > Docker Registry
* Select "Azure Container Registry"
* Select your ACR and enter a suitable connection name (to recreate our setup, name it "holocontainers")

## Import YAML configuraton

* New > New Build Pipeline
* Select from GitHub and select the `HoloRepository-Core` repo
* Select "Existing Azure Pipelines YAML file"
* Set path to `/Misc/build/azure-pipelines.yml`
* Verify the imported YAML configuration and run the pipeline

## References

* [YAML schema docs](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema)
* [Service connections
  docs](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoint)
