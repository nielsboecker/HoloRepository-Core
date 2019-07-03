#!/bin/bash

deploy() {
    echo "[Logging into Azure]"
    az login

    if [[ $? -eq 1 ]]; then
        echo "Error logging into Azure. Were your credentials correct?"
        exit 1
    fi

    echo "[Create Resource Group] ${RESOURCE_GROUP} @ ${RESOURCE_LOCATION}"
    az group create \
        --name ${RESOURCE_GROUP} \
        --location ${RESOURCE_LOCATION}

    echo "[Start FHIR service deployment]"
    az group deployment create -g ${RESOURCE_GROUP} --template-file ./templates/fhir_server/deploy.json --parameters @./templates/fhir_server/parameters.json --parameters serviceName="${SERVICE_NAME}" --parameters sqlAdminPassword="${SQL_PASSWORD}"

    echo "[FHIR service deployed] Check at https://${SERVICE_NAME}.azurewebsites.net/metadata"
}

display_config() {
    cat <<EOT
Azure FHIR server will be configured with the following parameters

    Resource Group: ${RESOURCE_GROUP}
    Resource Location: ${RESOURCE_LOCATION}
    FHIR Service Name: ${SERVICE_NAME}
    SQL password: ${SQL_PASSWORD}

Press any key to continue or Ctr-C to stop execution.
EOT
    read
}

main() {
    if [[ "${1}" == "-h" || "${1}" == "--help" || "${#}" -ne 1 ]]; then
        echo "${#}"
        echo "Usage: ${0} config.cfg"
        exit 1
    fi
    . ${1}
    display_config
    deploy
}

main ${*}
