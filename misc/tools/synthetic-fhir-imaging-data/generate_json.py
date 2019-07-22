import json
import config
import sys
import os
import glob


def create_contained_endpoint(tag, url):
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


def create_endpoint_reference(tag):
    return [{"reference": "#" + tag}]


def generate_instances(instances, display):
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


def modify_imaging_study(data, num_instances, display_name, url):
    resource_data = data["resource"]
    num_instances = int(num_instances)
    tag = "imagingEndpointId"
    resource_data["numberOfSeries"] = 1
    resource_data["numberOfInstances"] = num_instances
    resource_data["endpoint"] = create_endpoint_reference(tag)
    resource_data["contained"] = create_contained_endpoint(tag, url)
    resource_data["subject"]["reference"] = resource_data["subject"][
        "reference"
    ].replace("urn:uuid:", "Patient/")
    resource_data.pop("encounter", None)
    resource_data["series"][0]["numberOfInstances"] = num_instances
    resource_data["series"][0]["bodySite"]["display"] = display_name
    resource_data["series"][0]["instance"] = generate_instances(
        num_instances, display_name
    )

    data["resource"] = resource_data

    return data


def write_data(output_path, content):
    dir_name = os.path.dirname(output_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(output_path, "w") as output_f:
        output_f.write(json.dumps(content, indent=4, sort_keys=True))


def patient_handler(data, prac_ids):
    general_practitioners = []
    for pid in prac_ids:
        general_practitioners.append({"reference": "Practitioner/" + pid})

    data["resource"]["generalPractitioner"] = general_practitioners

    return data


def practitioner_handler(data):
    return data


def imaging_study_handler(data, filename):
    result = None

    if filename in config.CONFIG:
        title, num_instances, display_name, url = config.CONFIG[filename]
        result = modify_imaging_study(data, num_instances, display_name, url)
    return result


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    for filepath in glob.glob(os.path.join(input_dir, "*")):
        data = None
        entry_data = []
        practitioner_ids = []
        with open(filepath, "r") as read_patient_file:
            data = json.load(read_patient_file)

        # Pre-proc, look for all prac ids
        for resource in data["entry"]:
            resource_type = resource["resource"]["resourceType"]
            if resource_type == "Practitioner":
                practitioner_ids.append(resource["resource"]["id"])

        # Actual processing
        for resource in data["entry"]:
            new_data = None
            resource_type = resource["resource"]["resourceType"]
            if resource_type == "ImagingStudy":
                new_data = imaging_study_handler(resource, os.path.basename(filepath))
            elif resource_type == "Practitioner":
                new_data = practitioner_handler(resource)
            elif resource_type == "Patient":
                new_data = patient_handler(resource, practitioner_ids)

            if new_data:
                entry_data.append(new_data)

        if entry_data:
            data["entry"] = entry_data
            write_data(
                os.path.join(output_dir, os.path.basename(filepath) + ".modified"), data
            )


if __name__ == "__main__":
    main()
