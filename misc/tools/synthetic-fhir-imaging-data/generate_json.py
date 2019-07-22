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


def find_imaging_study(data):
    for i in range(len(data["entry"])):
        if data["entry"][i]["resource"]["resourceType"] == "ImagingStudy":
            return i
    else:
        raise LookupError("ImagingStudy resource not found")


def write_data(output_path, content):
    dir_name = os.path.dirname(output_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(output_path, "w") as output_f:
        output_f.write(json.dumps(content, indent=4, sort_keys=True))


def patient_handler(filename, data):
    pass


def practitioner_handler(filename, data):
    pass


def imaging_study_handler(filename, data):
    result = None

    if filename in config.CONFIG:
        print(data)
        title, num_instances, display_name, url = config.CONFIG[filename]
        result = modify_imaging_study(data, num_instances, display_name, url)
    return result


def main(resource_handler):
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    for filepath in glob.glob(os.path.join(input_dir, "*")):
        data = None
        entry_data = []
        with open(filepath, "r") as read_patient_file:
            data = json.load(read_patient_file)
        for i, resource in enumerate(data["entry"]):
            resource_type = resource["resource"]["resourceType"]
            if resource_type in resource_handler:
                print(resource_type)
                new_data = resource_handler[resource_type](
                    os.path.basename(filepath), resource
                )

                if new_data:
                    entry_data.append(new_data)

        if entry_data:
            data["entry"] = entry_data
            write_data(
                os.path.join(output_dir, os.path.basename(filepath) + ".modified"), data
            )


if __name__ == "__main__":
    resource_handler = {
        "ImagingStudy": imaging_study_handler,
        "Practitioner": practitioner_handler,
        "Patient": patient_handler,
    }
    main(resource_handler)
