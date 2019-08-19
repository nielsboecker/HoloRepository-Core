import json
from datetime import datetime


def add_info_for_accesor(infoForAccessor, title, creationDes, outputDir):

    infoForAccessor.update(
        {
            "title": title,
            "creationDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "creationDescription": creationDes,
            "outputFileDir": outputDir,
        }
    )
    print("info: " + json.dumps(infoForAccessor))

    return infoForAccessor


if __name__ == "__main__":
    print("component can't run on its own")
