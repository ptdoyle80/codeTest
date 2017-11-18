#!usr/bin/python
#
# Written by:
# Pat Doyle
# Hardware Test Engineer Candidate
# 16 November 2017
#
#####################################################################################################
# Coding Challenge:
# An anagram is a word formed by rearranging the letters of another, like "topside" and "deposit". 
# In some cases, there might be as many (or more) anagrams than there are characters, like "post", 
# "spot", "stop" and "tops".
#
# Write a program to find all of the anagrams in a dictionary in which there are at least 4 letters 
# in the word and at least as many anagrams as there are letters.
#
# The dictionary will be a file on disk with one line per word. Your operating system likely already
# has such a file in /usr/dict/words or /usr/share/dict/words.
#
# The output produced by your code should be in this format:
#
# emit, item, mite, time
# merit, miter, mitre, remit, timer
# reins, resin, rinse, risen, serin, siren
# inert, inter, niter, retin, trine
# inset, neist, snite, stein, stine, tsine
#####################################################################################################

import re, sys, argparse, shutil
import os.path
from collections import OrderedDict

# Globals:
quiet   = 0
terse	= 1
debug   = 2
toomuch = 3
verbosity = quiet

def loadDictionary():
    
    if verbosity >= debug:
        print '*******************************   You are in debugger->loadDictionary   **************************\n\n'

    # Bring in words from local dictionary as a list without newlines
    dictionaryFile = open('/usr/dict/words')
    with dictionaryFile as fid:
        wordList = fid.read().splitlines()

    # Make sure all letters are lowercase 
    wordList = [letter.lower() for letter in wordList]
    
    # create a test list for debugging
    if verbosity >= debug:
        wordList = []
        wordList = ['ante','fract','neat','eatn','tracf','tarcf','tean','frcat','craft','car','arc','rac','jump']

    if verbosity >= debug:
    	print '\n\nHello again. You are in debugger\n\n'
    	# output shows how many words do you have? 
        print 'Number of words: ' + str(len(wordList))
    if verbosity >= toomuch:
        # hope it's not too big
        print wordList
    
    # return the dictionary entries
    return wordList
    
def findAnagrams(loadedDictionary):
    # function to provide anagrams with at least 4 letters that have as many entries as letters or more
    
    if verbosity >= debug:
        print '*******************************   You are in debugger->findAnagrams   ****************************\n\n'

    # create copy of the dictionary with individual words sorted alphabetically
    # e.g. aardvark == aaadkrrv

    # define words to compare
    sortedWords1 = list()
    sortedWords2 = list()
    for word in loadedDictionary:
        sortedWords1.append(''.join(sorted(word)))
        sortedWords2.append(''.join(sorted(word)))

    if verbosity >= debug:
        print '\n\nYou are in debugger\n\n'
        print 'Sorted dictionary: \n'
        print sortedWords1

    # duplicate entries in the sorted words will be anagrams, so let's find them
    foundDuplicates = findDuplicates(sortedWords1, sortedWords2)
    
    # sort to find duplicates in the duplicates
    sortedDuplicates = list()
    for duplicate in foundDuplicates:
        temp = duplicate
        temp.sort()
        sortedDuplicates.append(temp)

    # remove duplicated duplicates and then we can print our anagrams!
    i = 0
    numAnagrams = 0

    # sort the list so that duplicates are consecutive
    sortedDuplicates.sort()

    # remove duplicate entries
    while i < len(sortedDuplicates) - 1:
        if sortedDuplicates[i] == sortedDuplicates[i+1]:
            sortedDuplicates.remove(sortedDuplicates[i])
        else: 
            i = i+1

    if verbosity >= terse:
        print '\n\n sortedDuplicates: \n\n'
        print sortedDuplicates

    return sortedDuplicates

def findDuplicates(sortedWords1, sortedWords2):

    # function to find duplicate entries of sorted word lists from dictionary
    # since words are sorted by letter, duplicate entries are anagrams

    if verbosity >= debug:
        print '*******************************   You are in debugger->findDuplicates   **************************\n\n'

    allDuplicatesFound = []
    duplicates = 0

    # brute force scrub the sorted list for duplicates and record the indices 
    # make sure you aren't recording the same set though!
    for i in range(len(sortedWords1)):
    	# reinitialize
        numAnagrams = 0 # number of anagrams added to list
        iFoundFlag = False # I found an i for an anagram this turn or not
        foundIndex = list() # list of indexes found this turn

        for j in range(len(sortedWords2)): # loop through the duplicates
            if sortedWords1[i] == sortedWords2[j] and i != j and len(sortedWords1[i]) >= 4: # found a valid anagram
                # increase number found for this iteration
                numAnagrams = numAnagrams + 1
                # check if we've flagged this iteration
                if iFoundFlag == False:
                	iFoundFlag = True
                	foundIndex.append(i)
                	numAnagrams = numAnagrams + 1
                foundIndex.append(j)

                if verbosity >= toomuch:
	                print loadedDictionary[i] + ' i = ' + str(i) + ' ' + loadedDictionary[j] + ' j = ' + str(j)

                if verbosity >= debug:
                    print foundIndex
                    print str(numAnagrams)

        
        # final test to make sure there are at least as many anagrams as there are letters
    	if numAnagrams >= len(sortedWords1[i]):
    		if verbosity >= debug:
    			print 'We found ' + str(numAnagrams) + ' anagrams'
    		allDuplicatesFound.append(foundIndex)
    	
    if verbosity >= debug:
        print '\n\n allDuplicatesFound: \n\n'
        print allDuplicatesFound


    return allDuplicatesFound

def printAnagrams(anagramIndices, loadedDictionary):
    
    # function to print out the anagrams with four or more letters 
    # and at least as many anagrams as letters from the dictionary

    if verbosity >= debug:
        print '*******************************   You are in debugger->printAnagrams   **************************\n\n'

    for index in anagramIndices:
        printToScreen = []
        for i in range(len(index)):
            printToScreen.append(loadedDictionary[index[i]])
        print ', '.join(printToScreen)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "planetCodeTest_Doyle_20171116.py", description = "A utility to extract anagrams from a dictionary.")
    parser.add_argument("-v", "--verbosity",        help="verbosity (0 = quiet, 1 = terse, 2 = verbose, 3 = debug)")
        
    args = parser.parse_args()
        
    if args.verbosity:
        verbosity = int(args.verbosity)

    loadedDictionary = loadDictionary()
    anagramIndices = findAnagrams(loadedDictionary)
    printAnagrams(anagramIndices, loadedDictionary)

