import pandas as pd
from updateData import updateID, addNewID, populateData
import os 
os.chdir('C:/Users/avery/Desktop') 

pdMovies = pd.read_csv('movies.csv', index_col='id')

populateData(pdMovies)

update = False

# MOVIE ID INPUT
rawInput = input('Enter the TMDB ID of the new movie: ').strip()
while True:
    try:
        if (rawInput == 'x') or (rawInput == 'X'):
            print('Exiting...')
            exit()

        newID = int(rawInput)
        if newID in pdMovies.index:
            raise KeyError

    except ValueError:
        print('============\nTYPE ERROR:\n    ' + str(rawInput) + ' must be an int.\n')
        rawInput = input('Re-enter the id, or type x to exit: ').strip()

    except KeyError:
        print('============\n    ' + str(newID) + ' already exists.\n')
        update = True
        break

    else:
        break


# MOVIE RATING INPUT 
rawInput = input('Enter a rating (1-10). Type 0 to set to null: ').strip() 
while True:
    try:
        if (rawInput == 'x') or (rawInput == 'X'):
            print('Exiting...')
            exit()

        newRating = int(rawInput)
        if (newRating < 0) or (newRating > 10):
            raise TypeError

    except ValueError:
        print('============\nTYPE ERROR:\n    ' + str(rawInput) + ' must be an int from 1-10 inclusive, or 0 to skip.\n')
        rawInput = input('Re-enter the rating, or press x to exit: ').strip()

    except TypeError:
        print('============\nVALUE ERROR:\n    ' + str(rawInput) + ' must be an int from 1-10 inclusive, or 0 to skip.\n')
        rawInput = input('Re-enter the rating, or press x to exit: ').strip()

    else:
        break

if update:
    updateID(pdMovies, newID, newRating)
else: 
    addNewID(pdMovies, newID, newRating)



