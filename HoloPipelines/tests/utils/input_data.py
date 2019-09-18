sample_medical_data = {
    "title": "Test Hologram",
    "description": "Synthetic data for testing purposes",
    "bodySite": "None",
    "dateOfImaging": "2017-07-21T17:32:28Z",
    "author": {
        "aid": "123123",
        "name": {
            "full": "Kawai Wong",
            "title": "Mr",
            "given": "Kawai",
            "family": "Wong",
        },
    },
    "patient": {
        "pid": "321321",
        "name": {"full": "Jason Lee", "title": "Mr", "given": "Jason", "family": "Lee"},
    },
}

sample_job = {
    "imagingStudyEndpoint": "https://holoblob.blob.core.windows.net/mock-pacs/normal-pelvis-soft.zip",
    "plid": "bone_segmentation",
    "medicalData": {
        "title": "Testing",
        "description": "Test bone segmentation pipeline",
        "bodySite": "Lung",
        "contentType": "glb",
        "dateOfImaging": "2017-07-21T17:32:28Z",
        "author": {
            "aid": "123123",
            "name": {
                "full": "Kawai Wong",
                "title": "Mr",
                "given": "Kawai",
                "family": "Wong",
            },
        },
        "patient": {
            "pid": "321321",
            "name": {
                "full": "Jason Lee",
                "title": "Mr",
                "given": "Jason",
                "family": "Lee",
            },
        },
    },
}
