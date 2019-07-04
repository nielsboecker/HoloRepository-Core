#!/usr/env/bin python

import requests
import json
import sys
import fire

from urllib.parse import urljoin

class FHIRInteraction(object):
    def __init__(self, base_url):
        self._base_url = base_url
        self._headers = {'Content-Type': 'application/fhir+json'}
    
    def _upload(self, url: str, content: dict, action: str):
        if action == 'PUT':
            r = requests.put(url, headers=self._headers, data=json.dumps(content))
        elif action == 'POST':
            r = requests.post(url, headers=headers, data=json.dumps(content))
        print(f'{r.status_code} - {action} to {url}')
        if r.status_code == 400:
            sys.exit(r.json())

    def bundle_file(self, fhir_json: str):
        content = None
        with open(fhir_json, 'r') as fhir_f:
            content = json.load(fhir_f)

        if not (content['resourceType'] == "Bundle" and content['type'] == 'transaction'):
            sys.exit('Selected file is not a FHIR transaction')

        for entry in content['entry']:
            if entry['fullUrl'].index('urn:uuid:') == 0:
                id = entry['fullUrl'].split('urn:uuid:')[1]
                url = urljoin(self._base_url, '/'.join([entry['request']['url'], id]))
                self._upload(url, entry['resource'], 'PUT') 
            else:
                url = urljoin(self._base_url, entry['request']['url'])
                self._upload(url, entry['resource'], 'POST') 


if __name__ == "__main__":
    fire.Fire(FHIRInteraction)