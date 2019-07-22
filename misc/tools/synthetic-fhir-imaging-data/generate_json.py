import json
import config
import sys
import os


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
    num_instances = int(num_instances)
    tag = "imagingEndpointId"
    data["numberOfSeries"] = 1
    data["numberOfInstances"] = num_instances
    data["endpoint"] = create_endpoint_reference(tag)
    data["contained"] = create_contained_endpoint(tag, url)
    data["subject"]["reference"] = data["subject"]["reference"].replace(
        "urn:uuid:", "Patient/"
    )
    data.pop("encounter", None)
    data["series"][0]["numberOfInstances"] = num_instances
    data["series"][0]["bodySite"]["display"] = display_name
    data["series"][0]["instance"] = generate_instances(num_instances, display_name)

    return data


def find_imaging_study(data):
    for i in range(len(data["entry"])):
        if data["entry"][i]["resource"]["resourceType"] == "ImagingStudy":
            return i
    else:
        raise LookupError("ImagingStudy resource not found")


def main():
    for patient_file, info in config.CONFIG.items():
        title, num_instances, display_name, url = info
        if not os.path.isfile(patient_file):
            sys.exit("{0} cannot be found".format(patient_file))
        with open(patient_file, "r") as read_patient_file:
            data = json.load(read_patient_file)
            imaging_study_index = find_imaging_study(data)
            new_imaging_study = modify_imaging_study(
                data["entry"][imaging_study_index]["resource"],
                num_instances,
                display_name,
                url,
            )
            modified_data = data
            modified_data["entry"] = [
                data["entry"][0],
                new_imaging_study,
            ]  # first entry is patients

            print(json.dumps(modified_data))
        # print(name, instances, display, url)


if __name__ == "__main__":
    main()
