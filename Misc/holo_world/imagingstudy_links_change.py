import glob
import json

LINKS_CHANGE_CONFIG = {
    "left-renal-mass.zip": "https://holoblob.blob.core.windows.net/mock-pacs/left-renal-mass.zip",
    "left-scfe-pelvis-bone.zip": "https://holoblob.blob.core.windows.net/mock-pacs/left-scfe-pelvis-bone.zip",
    "left-scfe-pelvis-soft.zip": "https://holoblob.blob.core.windows.net/mock-pacs/left-scfe-pelvis-soft.zip",
    "normal-abdomen.zip": "https://holoblob.blob.core.windows.net/mock-pacs/normal-abdomen.zip",
    "normal-chest-lung.zip": "https://holoblob.blob.core.windows.net/mock-pacs/normal-chest-lung.zip",
    "normal-chest-mediastinal.zip": "https://holoblob.blob.core.windows.net/mock-pacs/normal-chest-mediastinal.zip",
    "normal-pelvis-bone.zip": "https://holoblob.blob.core.windows.net/mock-pacs/normal-pelvis-bone.zip",
    "normal-pelvis-soft.zip": "https://holoblob.blob.core.windows.net/mock-pacs/normal-pelvis-soft.zip",
}

for img_filepath in glob.glob("ehr_data/ImagingStudy*.json"):
    with open(img_filepath, "r") as img_file:
        json_data = json.load(img_file)
        if "contained" not in json_data or "address" not in json_data["contained"]:
            continue

        dl_url = json_data["contained"]["address"]
        new_dl_url = LINKS_CHANGE_CONFIG.get(dl_url, None)

        if new_dl_url:
            json_data["contained"]["address"] = new_dl_url
            print(f"Replacing links in {img_filepath}")
            with open(img_filepath, "w") as new_file:
                json.dump(json_data, new_file, indent=4)
