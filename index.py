import os
import json


def main():
    try:
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

        #groups the songs by month in a dictionary
        monthly_stats = group_by_month(master_list)

        #makes a new dict with the songs ranked by month
        rankings = rank(monthly_stats)

        #makes it so that every month has a max of 30 songs
        final_list = chop(rankings)

        #show results 
        show(final_list)

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except OSError as oe:
        print(f"Error reading directory or files: {oe}")
    except Exception as e:
        print(f"Error: {e}")

    



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

def group_by_month(master_list):
    """
    Takes in the master list of the combined json files and returns a list
    of dictionaries where the key is the date in year/month and the value
    is a list of the songs listlened to in that month
    """

    monthly_stats = dict()

    for song in master_list:
        timestamp = song['ts']

        #I use timestamp[:7] because spotify json files use "YYYY-MM" so
        #you have to get the first 7 digits including the dash
        year_month = timestamp[:7]

        #extract the name of the song
        name = song['master_metadata_track_name']

        #makes a new key value pair for every month
        if year_month not in monthly_stats:
            monthly_stats[year_month] = []
        monthly_stats[year_month].append(name)

    return monthly_stats

def rank(monthly_stats):
    """
    Takes in a dictionary of the the songs divided by month and returns 
    a dictionary with the keys being the year and month and the values 
    being another dictionary with the songs and the amount of times it's gotten it played
    """
    song_rankings = dict()

    #makes it a touple with the first object being the year-month and the scond the list of songs
    for month, songs in monthly_stats.items():
            ranking = dict()
            for song in songs:
                name = song['master_metadata_track_name']
                if name in ranking:
                    ranking[name] += 1
                else:
                    ranking[name] = 1
            #using the sorted function to sort while turing it into a list
            #of touples and then turning it into a dict after 
            sorted_ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
            song_rankings[month] = sorted_ranking

    return song_rankings

def chop(rankings):
    """
    Limits the number of songs of every month to 30
    """
    final_rankings = {}

    for month, songs in rankings.items():
        final_rankings[month] = []
        counter = 0
        for song in songs:
            if counter == 30:
                break
            final_rankings[month].append(song)
            counter += 1
                
    return final_rankings

def show(final_list):
    """
    prints out final list in a formated way
    """

    for month in final_list:
        songs = []
        print(f"For the year-month: {month} your top songs were:")
        for song in month:
            songs.append(song)
        print(songs)


if __name__ == "__main__":
    main()