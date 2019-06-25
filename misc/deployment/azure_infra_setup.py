#!/usr/bin/env python3

import subprocess
import json
import sys

AZURE_DEPLOY = """
{
    "$schema": "https://schema.management.azure.com/schemas/2014-04-01-preview/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "accountName": {
            "type": "string"
        },
        "accessPolicies": {
            "type": "array"
        },
        "offerThroughput": {
            "type": "int",
            "allowedValues": [1000],
            "defaultValue": 1000,
            "metadata": {
                "description": "Cosmos DB throughput. Fix at 1000 RUs in initial public preview"
            }
        }
    },
    "resources": [
        {
            "apiVersion": "2018-08-20-preview",
            "type": "Microsoft.HealthcareApis/services",
            "kind": "fhir",
            "name": "[parameters('accountName')]",
            "location": "[resourceGroup().location]",
            "properties": {
                "accessPolicies": "[parameters('accessPolicies')]",
                "cosmosDbConfiguration": {
                    "offerThroughput": "[parameters('offerThroughput')]"
                }
            }
        }
    ]
}
""".strip()

AZURE_DEPLOY_PARAMS = """
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "accountName": {},
        "accessPolicies": {}
    }
}
""".strip()

CONFIG = {
        "account_name": "holorepo-12345",
        "resource_group": "holorepo-rg",
        # List of available regions for the resource type 'Microsoft.HealthcareApis/services' is 'ukwest,northcentralus,westus2'.
        "location": "ukwest",
        # Get object id with `az ad user list` or `az ad user show <name@mail.com> | jq -r .objectId
        "object_id": ["c0ec53e4-3341-43ed-b4ad-d3dbad543625"],
        }


def format_object_id(obj_list):
    objs = []
    for x in obj_list:
        objs.append({"objectId": x})

    return objs


def main():
    allowed_objects = format_object_id(CONFIG['object_id'])
    json_params = json.loads(AZURE_DEPLOY_PARAMS)
    json_params["parameters"]["accountName"]["value"] = CONFIG['account_name']
    json_params["parameters"]["accessPolicies"]["value"] = allowed_objects
    
    
    with open('azuredeploy.json', 'w') as tmp:
        tmp.write(AZURE_DEPLOY)
    with open('azuredeploy.parameters.json', 'w') as tmp:
        tmp.write(json.dumps(json_params, indent=4))

    command = f'az group create --name {CONFIG["resource_group"]} --location {CONFIG["location"]}'
    print(command)
    subprocess.call(command.split())

    command = 'az group deployment create -g ' + CONFIG["resource_group"] + ' --template-file azuredeploy.json --parameters @azuredeploy.parameters.json'
    print(command)
    subprocess.call(command.split())


if __name__ == '__main__':
    main()
