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
    
    def _request(self, url: str, action: str, body: dict = {}):
        if action == 'PUT':
            r = requests.put(url, headers=self._headers, data=json.dumps(body))
        elif action == 'POST':
            r = requests.post(url, headers=headers, data=json.dumps(body))
        elif action == 'DELETE':
            r = requests.delete(url)
        elif action == 'GET':
            r = requests.get(url)

        print(f'{r.status_code} - {action} to {url}')

        if not r.ok:
            sys.exit(r.json())

        return r


    def upload_bundle(self, fhir_json: str):
        content = None
        with open(fhir_json, 'r') as fhir_f:
            content = json.load(fhir_f)

        if not (content['resourceType'] == "Bundle" and content['type'] == 'transaction'):
            sys.exit('Selected file is not a FHIR transaction')

        for entry in content['entry']:
            if entry['fullUrl'].index('urn:uuid:') == 0:
                id = entry['fullUrl'].split('urn:uuid:')[1]
                url = urljoin(self._base_url, '/'.join([entry['request']['url'], id]))
                self._request(url, 'PUT', entry['resource']) 
            else:
                url = urljoin(self._base_url, entry['request']['url'])
                self._request(url, 'POST', entry['resource']) 


    def delete_all(self):
        next_url = self._base_url
        while next_url:
            r = self._request(next_url, 'GET')
            data = r.json()
            next_url = None
            
            for link in data['link']:
                if link['relation'] == "next":
                    next_url = link['url'] 
            
            for entry in data.get('entry', []):
                self._request(entry['fullUrl'], 'DELETE')


if __name__ == "__main__":
    fire.Fire(FHIRInteraction)