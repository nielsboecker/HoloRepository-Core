from datetime import datetime

# TODO: Refactor (or remove, if we only do the logging to file?)

status = {
    "j0": {"status": "segment", "timestamp": "2019-08-05 14:09:19"},
    "j1": {
        "status": "segment",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    },
}
