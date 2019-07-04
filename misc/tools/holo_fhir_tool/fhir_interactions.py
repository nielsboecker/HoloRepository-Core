#!/usr/env/bin python

import json
import sys
import glob
import os
from urllib.parse import urljoin

import fire
import requests


class FHIRInteraction:
    def __init__(self, base_url):
        self._base_url = base_url
        self._headers = {"Content-Type": "application/fhir+json"}

    def _request(self, url: str, action: str, body: dict = None):
        if action == "PUT":
            r = requests.put(url, headers=self._headers, data=json.dumps(body))
        elif action == "POST":
            r = requests.post(url, headers=self._headers, data=json.dumps(body))
        elif action == "DELETE":
            r = requests.delete(url)
        elif action == "GET":
            r = requests.get(url)

        print(f"{r.status_code} - {action} to {url}")

        if not r.ok:
            sys.exit(r.json())

        return r

    def upload_bundle(self, fhir_json: str):
        print(f"Processing file: {fhir_json}")
        content = None
        with open(fhir_json, "r") as fhir_f:
            content = json.load(fhir_f)

        if not (
            content["resourceType"] == "Bundle" and content["type"] == "transaction"
        ):
            sys.exit("Selected file is not a FHIR transaction")

        for entry in content["entry"]:
            if entry["fullUrl"].index("urn:uuid:") == 0:
                uid = entry["fullUrl"].split("urn:uuid:")[1]
                url = urljoin(self._base_url, "/".join([entry["request"]["url"], uid]))
                self._request(url, "PUT", entry["resource"])
            else:
                url = urljoin(self._base_url, entry["request"]["url"])
                self._request(url, "POST", entry["resource"])

    def delete_all(self, resource: str = ""):
        next_url = urljoin(self._base_url, resource)
        while next_url:
            r = self._request(next_url, "GET")
            data = r.json()
            next_url = None

            for link in data["link"]:
                if link["relation"] == "next":
                    next_url = link["url"]

            for entry in data.get("entry", []):
                self._request(entry["fullUrl"], "DELETE")

    def upload_folder(self, src_dir: str, ext: str = "json"):
        print(f"Processing folder: {src_dir}")
        for file in glob.glob(os.path.join(src_dir, "*." + ext)):
            self.upload_bundle(file)


if __name__ == "__main__":
    fire.Fire(FHIRInteraction)
