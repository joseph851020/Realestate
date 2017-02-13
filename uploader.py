import os
import json
import requests
import glob

for root, dirs, files in os.walk("import_data"):
    path = root.split('/')
    if "data.json" in files:
        with open(os.path.join(root, 'data.json')) as data_file:
            data = json.load(data_file)
    else:
        continue

    print file

    headers = {'Authorization': 'Token 44bcd32456ebba4532e539c4e39696f0543d4b03'}

    values = {
        'title': data['property']['summary'],
        'description': data['property']['fullDescription'],
        'coords': "{}, {}".format(data['property']['latitude'], data['property']['longitude']),
        'features': json.dumps(data['property']['features'])
    }

    files = []  # append here all jpg in "root" variable
    for image in glob.glob(os.path.join(root, '*.jpg')):
        files.append((os.path.basename(image), open(image, 'rb')))

    r = requests.post("http://localhost:8000/api/listings/", headers=headers, files=files, data=values)
