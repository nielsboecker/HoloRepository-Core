#!/usr/bin/env python

import json
import os
import glob
import fire
import logging


class ModifySyntheaData:
    def __init__(self, config="config.cfg"):
        self.config = None
        with open(config, "r") as config_f:
            self.config = json.load(config_f)

    def _create_contained_endpoint(self, tag, url):
        endpoint = {
            "resourceType": "Endpoint",
            "id": tag,
            "status": "active",
            "connectionType": {
                "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
                "code": "direct-project",
            },
            "address": url,
            "payloadType": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/resource-types",
                            "code": "ImagingStudy",
                        }
                    ]
                }
            ],
        }

        return endpoint

    def _create_endpoint_reference(self, tag):
        return [{"reference": "#" + tag}]

    def _generate_instances(self, instances, display):
        data = []
        for i in range(instances):
            data.append(
                {
                    "uid": "id-" + str(i + 1),
                    "sopClass": {
                        "system": "urn:ietf:rfc:3986",
                        "code": "1.2.840.10008.5.1.4.1.1.3.1",
                    },
                    "number": i + 1,
                    "title": "Image of " + display,
                }
            )

        return data

    def _modify_imaging_study(self, data, num_instances, display_name, url):
        resource_data = data["resource"]
        num_instances = int(num_instances)
        tag = "imagingEndpointId"
        resource_data["numberOfSeries"] = 1
        resource_data["numberOfInstances"] = num_instances
        resource_data["endpoint"] = self._create_endpoint_reference(tag)
        resource_data["contained"] = self._create_contained_endpoint(tag, url)
        resource_data["subject"]["reference"] = resource_data["subject"][
            "reference"
        ].replace("urn:uuid:", "Patient/")
        resource_data.pop("encounter", None)
        resource_data["series"][0]["numberOfInstances"] = num_instances
        resource_data["series"][0]["bodySite"]["display"] = display_name
        resource_data["series"][0]["instance"] = self._generate_instances(
            num_instances, display_name
        )

        data["resource"] = resource_data

        return data

    def _write_data(self, output_path, content):
        dir_name = os.path.dirname(output_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(output_path, "w") as output_f:
            output_f.write(json.dumps(content, indent=4, sort_keys=True))

    def _patient_handler(self, data, prac_ids):
        logging.info("\tIncluding Patient resource")
        general_practitioners = []
        for pid in prac_ids:
            logging.debug(f"\tAdding generalPractitioner: {pid}")
            general_practitioners.append({"reference": "Practitioner/" + pid})
        data["resource"]["generalPractitioner"] = general_practitioners

        return data

    def _practitioner_handler(self, data):
        logging.info("\tIncluding Practitioner resource")
        return data

    def _imaging_study_handler(self, data, filename):
        result = None
        if filename in self.config:
            logging.info("\tIncluding ImagingStudy resource")
            title, num_instances, display_name, url = self.config[filename]
            result = self._modify_imaging_study(data, num_instances, display_name, url)
        return result

    def convert(self, in_dir, out_dir):
        for filepath in sorted(glob.glob(os.path.join(in_dir, "*.json"))):
            logging.info(f"Processing: {filepath}")
            data = None
            entry_data = []
            practitioner_ids = []
            have_img_study = False
            with open(filepath, "r") as read_patient_file:
                data = json.load(read_patient_file)

            # Pre-proc, look for all prac ids
            for resource in data["entry"]:
                resource_type = resource["resource"]["resourceType"]
                if resource_type == "Practitioner":
                    pid = resource["resource"]["id"]
                    practitioner_ids.append(pid)
                    logging.debug(f"Found practitioner: {pid}")

            # Actual processing
            for resource in data["entry"]:
                new_data = None
                resource_type = resource["resource"]["resourceType"]
                if resource_type == "ImagingStudy" and not have_img_study:
                    new_data = self._imaging_study_handler(
                        resource, os.path.basename(filepath)
                    )
                    have_img_study = True
                elif resource_type == "Practitioner":
                    new_data = self._practitioner_handler(resource)
                elif resource_type == "Patient":
                    new_data = self._patient_handler(resource, practitioner_ids)

                if new_data:
                    entry_data.append(new_data)

            if entry_data:
                data["entry"] = entry_data
                self._write_data(
                    os.path.join(
                        out_dir,
                        os.path.basename(filepath).replace(".json", ".modified.json"),
                    ),
                    data,
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(ModifySyntheaData)
