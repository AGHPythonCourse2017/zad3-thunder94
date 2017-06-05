import argparse
import csv
import requests
import sys
from google import search
from io import BytesIO
from zipfile import ZipFile


class InformationValidator:

    def __init__(self):
        self.all = 0
        self.fake = 0

    @staticmethod
    def receive_zip():
        response = requests.get('https://github.com/BigMcLargeHuge/opensources/zipball/master')
        zipfile = ZipFile(BytesIO(response.content))
        for path in zipfile.namelist():
            if 'sources.csv' in path:
                zipfile.extractall()
                return path

    def validate_information(self, path, information, searches):
        query = ''
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for word in information:
                query = query + word + ' '
            query = query[:-1]
            for url in search(query, stop=searches):
                self.all += 1
                for row in reader:
                    if row[0] in url:
                        self.fake += 1


def main():

    parser = argparse.ArgumentParser(description='Information accuracy analyzer. Provide information as argument.')
    parser.add_argument('information', nargs='*', help='Information to check.')
    parser.add_argument('-s', '--searches', type=int, default=10, help='Number of google searches')
    args = parser.parse_args()
    validator = InformationValidator()
    try:
        path = InformationValidator.receive_zip()
    except Exception:
        print('Error getting zip file')
        sys.exit(1)
    validator.validate_information(path, args.information, args.searches)
    print("Probability of fake news: ", validator.fake/validator.all*100, "%")

if __name__ == '__main__':
    main()
