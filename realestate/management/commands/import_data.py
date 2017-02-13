from django.core.management.base import BaseCommand, CommandError

import os, json, requests, glob


class Command(BaseCommand):
    help = 'imports external json data and images'

    # def add_arguments(self, parser):
    #     parser.add_argument('import_dir', nargs='+', type=str)

    def handle(self, *args, **options):
        print 'importing images'

        # get auth token first
        r = requests.post("http://localhost:8000/api-token-auth/", data={'username': 'admin', 'password': 'secret'})
        assert r.status_code == 200
        print 'got security token', r.json()
        token = r.json().get('token')
        print token

        # use auth token to post data via api

        for root, dirs, files in os.walk("./import_data"):
            path = root.split('/')
            if "data.json" in files:
                with open(os.path.join(root, 'data.json')) as data_file:
                    data = json.load(data_file)
            else:
                continue
            print file

            headers = {'Authorization': 'Token %s' % token}

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
