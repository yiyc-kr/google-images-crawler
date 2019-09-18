#!/usr/bin/env python
# coding: utf-8

import time
import argparse
import json
from urllib.parse import quote


def user_input():
    config = argparse.ArgumentParser()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=True)
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        json_file = json.load(open(config_file_check[0].config_file))

    return json_file


class googleimagescrawler:
    def __init__(self):
        pass

    def build_search_url(self, search_term):
        url = 'https://www.google.com/search?q=' + quote(search_term.encode('utf-8')) + \
              '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

        return url

    def download(self, arguments):
        paths = {}
        errorCount = None

        if arguments['keyword']:
            keyword = str(arguments['keyword'])
        else:
            raise ValueError('keyword is a required argument!')

        if arguments['blacklist']:
            blacklist = [str(item).strip() for item in arguments['blacklist'].split(',')]

        if arguments['limit']:
            limit = int(arguments['limit'])
        else:
            limit = 100

        if arguments['output_directory']:
            main_directory = arguments['output_directory']
        else:
            main_directory = "images"

        if arguments['id']:
            id = str(arguments['id'])
        else:
            id = None

        if arguments['word_slice']:
            word_slice = int(arguments['word_slice'])
            if len(keyword.split()) <= word_slice:
                raise ValueError("word_slice should be lower than keyword's word counts("
                                 + str(len(keyword.split())) + ")")
            else:
                keywords = []
                for i in range(word_slice, len(keyword.split())+1):
                    keywords += [' '.join(keyword.split()[item:item+i]) for item in range(len(keyword.split())-i+1)]
        else:
            keywords = [keyword]

        for search_term in keywords:
            url = self.build_search_url(search_term)

            print(url)


def main():
    arguments = user_input()
    total_errors = 0
    t0 = time.time()  # start the timer

    response = googleimagescrawler()
    paths, errors = response.download(arguments)
    total_errors = total_errors + errors

    t1 = time.time()
    total_time = t1 - t0
    if not arguments["silent_mode"]:
        print("\nDownloaded!")
        print("Total errors: " + str(total_errors))
        print("Total time taken: " + str(total_time) + " Seconds")


if __name__ == "__main__":
    main()
