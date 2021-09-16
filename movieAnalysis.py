from sklearn import tree
import pandas as pd
import re
import os
os.chdir('C:/Users/avery/Desktop')

pdMovies = pd.read_csv('movies.csv', index_col='id')


def createMovieData(data, countriesMap, countriesMapNumber):
    movieData = []
    col = ['budget', 'runtime', 'release_date', 'production_countries',
           'revenue', 'vote_average', 'vote_count']
    for d in col:
        if (d == 'release_date'):
            movieData.append(int(data[d].split('/')[2]))
            movieData.append(int(data[d].split('/')[0]))
        elif (d == 'production_countries'):
            if data[d] not in countriesMap:
                countriesMap[data[d]] = countriesMapNumber
                countriesMapNumber += 1
            movieData.append(countriesMap[data[d]])
        else:
            movieData.append(data[d])
    return movieData, countriesMap, countriesMapNumber


def generateData(pdMovies):
    countriesMap = {}
    countriesMapNumber = 0

    trainingData = []
    targetData = []

    for id, data in pdMovies.iterrows():
        if (data['rating'] != data['rating']):
            continue
        else:
            targetData.append(data['rating'])
            movieData, countriesMap, countriesMapNumber = createMovieData(
                data, countriesMap, countriesMapNumber)
            trainingData.append(movieData)
    return (trainingData, targetData)
