# Azure HoloRepository Kubernetes Setup
This details the steps needed to setup an azure kubernetes cluster and deploy the holorepository images to it.

## Prerequisites
- azure-cli
- kubectl

## Setup
### Create Azure Container Registry (ACR)
`az acr create --resource-group <myResourceGroup> --name <acrName> --sku Basic`

You will then deploy the holorepository images to the ACR. The steps will not be documented here, but you can reference it from the documentation link here: https://docs.microsoft.com/en-us/azure/container-registry/

### Create a service principal
First an Azure Active Directory service principal is created. This is necessary to allow AKS to interact with the ACR cluster.

`az ad sp create-for-rbac --skip-assignment`

The output will be similar to the following:

```
{
  "appId": "e7596ae3-6864-4cb8-94fc-20164b1588a9",
  "displayName": "azure-cli-2018-06-29-19-14-37",
  "name": "http://azure-cli-2018-06-29-19-14-37",
  "password": "52c95f25-bd1e-4314-bd31-d8112b293521",
  "tenant": "72f988bf-86f1-41af-91ab-2d7cd011db48"
}
```

The `appId` and `password` will be used in the next 2 steps.

### Configure ACR authentication
This step grants the AKS service principal the correct rights to pull images from ACR.

Get the name of the registry with the following command

`az acr show --resource-group <myResourceGroup> --name <acrName> --query "id" --output tsv`

Result of this command will be the `<acrId>`

Grant the access to pull images from the ACR

`az role assignment create --assignee <appId> --scope <acrId> --role acrpull`

### Create a kubernetes cluster
Use the following command to create a kubernetes cluster with rights to pull images from the ACR.

```
az aks create \
    --resource-group <myResourceGroup> \ --name <aksName> \ --node-count 5 \ --service-principal <appId> \ --client-secret <password>  \
    --generate-ssh-keys
```

### Configure the Kubernetes file
The following areas needs to be configured in the kubernetes file

- Docker image name
- Module configurations
- Secrets for blob storage
- IP address for services

#### Docker image names
Change the docker image names to point to where you are hosting your images.

e.g. `image: holocontainers.azurecr.io/holostorage-accessor:latest` to `image: <registryUrl>/<imageName>:<tag>`

#### Module configurations
Individual modules have their own configurations for their environment variables. Refer the respective module's README for more details.

#### Secret for blob storage
The access key to the blob storage should be kept secret. Use the following command to set the key so kubernetes knows how to set it before deploying it to the container.

`kubectl create secret generic blobstorekey --from-literal=AZURE_STORAGE_ACCESS_KEY=<yourKey>`

#### IP addresses for services
Many of the IP Addresses for the Accessor and Pipelines etc requires an IP address.

First [deploy the application](###Apply-Kubernetes-configuration-to-cluster), and wait for the ip addresses to be assigned. Then change the configurations again to point to the ip addresses and apply the configurations again.

### Apply Kubernetes configuration to cluster
Connect to cluster using kubectl

`az aks get-credentials --resource-group <myResourceGroup> --name <aksName>`

Apply deployment configuration

`kubectl apply -f holorepo-kubes.yaml`

View deployment status

`kubectl get services --watch` or `kubectl get pods --watch`

## References
https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr
https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster
