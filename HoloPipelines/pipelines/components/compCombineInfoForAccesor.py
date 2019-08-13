import json


def combineInfoForAccesor(infoForAccessor, title, creationDate, creationDes, outputDir):

    infoForAccessor.update(
        {
            "title": title,
            "creationDate": creationDate,
            "creationDescription": creationDes,
            "outputFileDir": outputDir,
        }
    )
    print("info: " + json.dumps(infoForAccessor))

    return infoForAccessor


if __name__ == "__main__":
    print("component can't run on its own")
