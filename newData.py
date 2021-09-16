import pandas as pd
import requests as req
from updateData import updateID, addNewID, populateData
import os
os.chdir('C:/Users/avery/Desktop')

pdMovies = pd.read_csv('movies.csv', index_col='id')
populateData(pdMovies)

rawInput = ''

while True:
    pdMovies = pd.read_csv('movies.csv', index_col='id')

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
            print('============\nTYPE ERROR:\n    ' +
                  str(rawInput) + ' must be an int.\n')
            rawInput = input('Re-enter the id: ').strip()

        except KeyError:
            print('============\n    ' + str(newID) + ' already exists.\n')
            update = True
            break

        else:
            break

    print()
    if update:
        print('Movie: ', pdMovies.loc[newID, 'title'])
        print('Rating: ', pdMovies.loc[newID, 'rating'])
    else:
        apiData = req.get('https://api.themoviedb.org/3/movie/' +
                          str(newID)+'?api_key=42468d346e59d2685235fee95a344f31').json()
        try:
            print('Movie: ', apiData['title'])
        except KeyError:
            print('Invalid movie ID.')
            continue
    print()

    # MOVIE RATING INPUT
    rawInput = input(
        'Enter a rating (1-10, ? for key). Type 0 to set to null: ').strip()
    while True:
        try:
            if (rawInput == 'x') or (rawInput == 'X'):
                print('Exiting...')
                exit()

            elif (rawInput == '?'):
                print(' 10 - A favorite')
                print('  9 - Great')
                print('  8 - Definitely recommend')
                print('  7 - Recommend')
                print('  6 - Nothing special, but recommend')
                print('  5 - Nothing special')
                print('  4 - Nothing special, don\'t go out of your way')
                print('  3 - Don\'t bother')
                print('  2 - Avoid')
                print('  1 - Trash')
                rawInput = input(
                    'Enter a rating (1-10, ? for key). Type 0 to set to null: ').strip()
                continue

            newRating = int(rawInput)
            if (newRating < 0) or (newRating > 10):
                raise TypeError

        except ValueError:
            print('============\nTYPE ERROR:\n    ' + str(rawInput) +
                  ' must be an int from 1-10 inclusive, or 0 to skip.\n')
            rawInput = input('Re-enter the rating: ').strip()

        except TypeError:
            print('============\nVALUE ERROR:\n    ' + str(rawInput) +
                  ' must be an int from 1-10 inclusive, or 0 to skip.\n')
            rawInput = input('Re-enter the rating: ').strip()

        else:
            break

    if update:
        updateID(pdMovies, newID, newRating)
    else:
        addNewID(pdMovies, newID, newRating, apiData)
