#!/usr/env/bin python

import requests
import json
import sys

from urllib.parse import urljoin

def upload(url: str, content: dict, action: str):
    headers = {'Content-Type': 'application/fhir+json'}
    if action == 'PUT':
        r = requests.put(url, headers=headers, data=json.dumps(content))
    elif action == 'POST':
        r = requests.post(url, headers=headers, data=json.dumps(content))
    print(f'{r.status_code} - {action} to {url}')
    if r.status_code == 400:
        sys.exit(r.json())

def process_fhir_transaction(fhir_json: str, base_url: str):
    content = None
    with open(fhir_json, 'r') as fhir_f:
        content = json.load(fhir_f)

    if not (content['resourceType'] == "Bundle" and content['type'] == 'transaction'):
        sys.exit('Selected file is not a FHIR transaction')

    for entry in content['entry']:
        if entry['fullUrl'].index('urn:uuid:') == 0:
            id = entry['fullUrl'].split('urn:uuid:')[1]
            url = urljoin(base_url, '/'.join([entry['request']['url'], id]))
            upload(url, entry['resource'], 'PUT') 
        else:
            url = urljoin(base_url, entry['request']['url'])
            upload(url, entry['resource'], 'POST') 


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"To use: {sys.argv[0]} fhirTransactionJSON fhir_server_uri")
    process_fhir_transaction(sys.argv[1], sys.argv[2])