#!/bin/bash

RES_GRP="holorepository-rg"
LOC="uksouth"
BLOB_STORE_NAME="holoblob"
CONTAINERS=('3dmodels' 'attachments')

az login

az group create \
    --name ${RES_GRP} \
    --location ${LOC} 

az storage account create \
    --name ${BLOB_STORE_NAME} \
    --resource-group ${RES_GRP} \
    --location ${LOC} \
    --sku Standard_LRS \
    --kind StorageV2

KEY=$(az storage account keys list \
    --account-name ${BLOB_STORE_NAME} \
    --resource-group ${RES_GRP} \
    --output table | grep "key1" | awk '{print $3}')

for name in "${CONTAINERS[@]}"; do
    az storage container create --account-key ${KEY} --account-name ${BLOB_STORE_NAME} --name "${name}"
done
