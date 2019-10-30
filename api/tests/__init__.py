from pathlib import Path
import json
import os

from definitions import ROOT_DIR

def saveResponse(response, resource, description = ""):
   path = getFixturePath(response, resource, description)
   data = prepareData(response)
   saveResponseToPath(data, path)

def getFixturePath(response, resource, description):
   name = resource + str(response.status_code) + description
   return Path(os.path.join(ROOT_DIR, 'tests/__fixtures/' + name + '.json'))

def prepareData(response):
   return {
      'code': response.status_code,
      'data': response.json
   }

def saveResponseToPath(data, path):
   if not path.exists():
      with path.open('w') as file:
         json.dump(data, file, indent=3)
