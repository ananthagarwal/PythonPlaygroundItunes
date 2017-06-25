#Source: Python Playground by Mahesh Venkitachalam

import plistlib
import numpy as np
from matplotlib import pyplot
import sys
import re, argparse

def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    #read in a playlist
    plist = plistlib.readPlist(fileName)
    #get the tracks from the Tracks dictionary

    tracks = plist['Tracks']
    #Create a track name dictionary
    trackNames = {}
    #iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            #look for existing entries
            if name in trackNames:
                #if a name and duration match, increment the count
                #round track length to the nearest second
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)

            else:
                #add dictionary entry as tuple (duration, count)
                trackNames[name] = (duration, 1)
        except:
            #ignore
            pass


    #store duplicates as (name, count) tuples
    dups = []
    for key, value in trackNames.items():
        if value[1] > 1:
            dups.append((key, value[1]))
    #save duplicates to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
    file = open("dups.txt", "wb")
    for val in dups:
        file.write("[%d] %s\n" % (val[0], val[1]))
    file.close()

def findCommonTracks(fileNames):
    trackNameSets = []
    genreCounts = []
    for fileNames in fileNames:
        trackNames = set()
        genres = {}
        #read in playlist
        plist = plistlib.readPlist(fileNames)
        #get the tracks
        tracks = plist['Tracks']
        #iterate through the tracks
        for trackId, track in tracks.items():
            try:
                #add the track name to a set
                trackNames.add(track['Name'])
                genre = track['Genre']
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1
            except:
                #ignore
                pass
        trackNameSets.append(trackNames)
        genreCounts.append(genres)
        #get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    #write to file
    if len(commonTracks) > 0:
        f = open("common.txt", "wb")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. " 
            "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks")
    for val in range(len(genreCounts)):
        labels = tuple(genreCounts[val].keys())
        sizes = convertToPie(list(genreCounts[val].values()))
        fig1, ax1 = pyplot.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        pyplot.figure(val)
    pyplot.show()

def convertToPie(lst):
    add = sum(lst)
    return [(x / add) * 100 for x in lst]


#collect statistics for the track names. Graph the average time of different genres

def plotStats(fileName):
    #read in a playlist
    plist = plistlib.readPlist(fileName)
    #get the tracks from the playlist
    tracks = plist['Tracks']
    #create lists of song ratings and track durations
    genres = {}
    #iterate through the tracks
    for trackId, track in tracks.items():
        try:
            genre = track['Genre']
            duration = track['Total Time']
            if genre in genres:
                genres[genre] = np.mean([genres[genre], duration])
            else:
                genres[genre] = duration
        except:
            #ignore
            pass

        #ensure that valid data was collected
        if genres == {}:
            print("No valid Genre/Total Time data in %s." % fileName)
            return

    #scatter plot

    y = list(genres.values())
    x = tuple(genres.keys())

    for val in range(len(y)):
        y[val] = y[val] / 60000.0
    # convert to minutes

    y_pos = np.arange(len(x))

    pyplot.bar(y_pos, y, align='center', alpha=0.5)
    pyplot.xticks(y_pos, x)
    pyplot.ylabel('Average duration of track (s)')
    pyplot.xlabel('Genre')

    pyplot.show()
    #show plot

def main():
    #create parser

    decStr = """ 
    This program analyzes playlist files (.xml) exported from iTunes.
    """

    parser = argparse.ArgumentParser(description = decStr)
    #add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    #add expected arguments
    group.add_argument('--common', nargs = '*', dest = 'plFiles', required = False)
    group.add_argument('--stats', dest = 'plFile', required = False)
    group.add_argument('--dup', dest = 'plFileD', required = False)

    #parse args
    args = parser.parse_args()

    if args.plFiles:
        #find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        #plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        #find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

if __name__ == '__main__':
    main()
