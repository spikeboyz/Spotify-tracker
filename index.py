import os
import sys
import json


def main():
    #ask for the folder
    folder = input("input folder with spotify json files:")

    files = os.listdir(folder)

    json_files = [f for f in files if f.endswith('.json')]

    merge_files(json_files)

def merge_files(json_files):
    result = list()
    for file in json_files:
         with open(file, 'r') as infile:
            result.extend(json.load(infile))



if __name__ == "__main__":
    main()