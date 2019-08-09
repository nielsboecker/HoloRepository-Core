#!/usr/bin/env python

import json
import os
import glob
import fire
import logging
import random
import string


class ModifySyntheaData:
    def __init__(self, config="config.cfg"):
        self._config = None
        with open(config, "r") as config_f:
            self._config = json.load(config_f)
        self._photo_rand = random.Random(self._config["general"]["seed"])
        self._practitioners_rand = random.Random(self._config["general"]["seed"])
        self._practitioners_per_patient = self._config["general"][
            "practitioners_per_patient"
        ]

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
        """Modify existing imaging study resource

        Modify synthea generated imaging study with information for dev.
        - Create endpoints to a self-contained reference to the url
        - Fix subject refererence to enable FHIR RESTful search to work
        - Remove unused encounter refererence
        - Expand `instance` array to configured number of instances
        """
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

    def _clean_names(self, data):
        if "name" in data["resource"]:
            for i, name in enumerate(data["resource"]["name"]):
                data["resource"]["name"][i]["family"] = name["family"].rstrip(
                    string.digits
                )
                for j, given_name in enumerate(name["given"]):
                    data["resource"]["name"][i]["given"][j] = given_name.rstrip(
                        string.digits
                    )

        return data

    def _add_photo(self, data):
        gender = None
        pic_num = self._photo_rand.randrange(100)
        if "gender" in data["resource"]:
            if data["resource"]["gender"] == "male":
                gender = "men"
            elif data["resource"]["gender"] == "female":
                gender = "women"

        if gender:
            data["resource"]["photo"] = [
                {"url": f"https://randomuser.me/api/portraits/{gender}/{pic_num}.jpg"}
            ]

        return data

    def _patient_handler(self, data, prac_ids):
        """Handle patient resource

        - Add generalPractitioner based on found practitioner ids
        - Remove all digits in names
        - Add photo
        """
        logging.info("\tIncluding Patient resource")
        general_practitioners = []

        if self._practitioners_per_patient > len(prac_ids):
            sample_size = len(prac_ids)
        else:
            sample_size = self._practitioners_per_patient

        selected_practitioners = self._practitioners_rand.sample(prac_ids, sample_size)
        for pid in selected_practitioners:
            logging.debug(f"\tAdding generalPractitioner: {pid}")
            general_practitioners.append({"reference": "Practitioner/" + pid})
        data["resource"]["generalPractitioner"] = general_practitioners
        data = self._clean_names(data)
        data = self._add_photo(data)

        return data

    def _practitioner_handler(self, data):
        """ Handle practitioner resource

        - Remove all digits in names
        - Add photo
        """
        data = self._clean_names(data)
        data = self._add_photo(data)
        logging.info("\tIncluding Practitioner resource")

        return data

    def _imaging_study_handler(self, data, filename):
        result = None
        if filename in self._config["imagingStudy"]:
            logging.info("\tIncluding ImagingStudy resource")
            title, num_instances, display_name, url = self._config["imagingStudy"][
                filename
            ]
            result = self._modify_imaging_study(data, num_instances, display_name, url)
        return result

    def convert(self, in_dir, out_dir):
        practitioner_ids = []

        for filepath in sorted(glob.glob(os.path.join(in_dir, "*.json"))):
            logging.info(f"PreProcessing: {filepath}")
            with open(filepath, "r") as read_patient_file:
                data = json.load(read_patient_file)

            # Pre-proc, look for all prac ids
            for resource in data["entry"]:
                resource_type = resource["resource"]["resourceType"]
                if resource_type == "Practitioner":
                    pid = resource["resource"]["id"]
                    practitioner_ids.append(pid)
                    logging.debug(f"Found practitioner: {pid}")

        if self._practitioners_per_patient > len(practitioner_ids):
            logging.warning(
                f"Insufficient practitioners to assign per patient: {len(practitioner_ids)} found"
            )

        for filepath in sorted(glob.glob(os.path.join(in_dir, "*.json"))):
            logging.info(f"Processing: {filepath}")
            data = None
            entry_data = []
            already_included_img_study = False
            with open(filepath, "r") as read_patient_file:
                data = json.load(read_patient_file)

            # Actual processing
            for resource in data["entry"]:
                new_data = None
                resource_type = resource["resource"]["resourceType"]
                if resource_type == "ImagingStudy" and not already_included_img_study:
                    new_data = self._imaging_study_handler(
                        resource, os.path.basename(filepath)
                    )
                    already_included_img_study = True
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
