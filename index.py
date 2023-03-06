import os
import datetime
import json


def main():
    #ask for the folder
    folder = input("input folder with spotify json files:")

    # creates the full path to the folder
    full_path = os.path.expanduser(folder)

    # finds all files in the folder
    files = os.listdir(full_path)

    # puts all the json files from the folder into a list
    json_files = [os.path.join(full_path, f) for f in files if f.endswith('.json')]

    #merges all the files into a list
    master_list = merge_files(json_files)

    print(master_list)
    



def merge_files(json_files):
    """
    Merges json files from a list of json files to a single
    list containing the merged json file
    """
    result = list()
    for file in json_files:
         with open(file, 'r') as infile:
            result.extend(json.load(infile))

    return result



if __name__ == "__main__":
    main()