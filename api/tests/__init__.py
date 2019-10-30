from pathlib import Path
import json

from definitions import FIXTURE_DIR


def saveResponse(response, resource, description=""):
    path = getFixturePath(response, resource, description)
    data = {'data': response.json}
    saveResponseToPath(data, path)


def getFixturePath(response, resource, description):
    name = resource + str(response.status_code) + description
    return Path(FIXTURE_DIR, name + '.json')


def saveResponseToPath(data, path):
    if not path.exists():
        with path.open('w') as file:
            json.dump(data, file, indent=3)
