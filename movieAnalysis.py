from sklearn import tree
import pandas as pd
from updateData import infoByID
import os
os.chdir('C:/Users/avery/Desktop')


def createMovieData(data, countriesMap, countriesMapNumber):
    movieData = []
    col = ['budget', 'runtime', 'release_date', 'production_countries',
           'revenue', 'vote_average', 'vote_count']
    for d in col:
        if (d == 'release_date'):
            # print(f'{data[d]}, {type(data[d])}')
            if isinstance(data, pd.DataFrame):
                movieData.append(int(data[d].values[0].split('-')[0]))
                movieData.append(int(data[d].values[0].split('-')[1]))
            else:
                movieData.append(int(data[d].split('/')[2]))
                movieData.append(int(data[d].split('/')[0]))
        elif (d == 'production_countries'):
            if isinstance(data, pd.DataFrame):
                if data[d].values[0] not in countriesMap:
                    countriesMap[data[d].values[0]] = countriesMapNumber
                    countriesMapNumber += 1
                movieData.append(countriesMap[data[d].values[0]])
            else:
                if data[d] not in countriesMap:
                    countriesMap[data[d]] = countriesMapNumber
                    countriesMapNumber += 1
                movieData.append(countriesMap[data[d]])
        else:
            movieData.append(data[d])
    return movieData, countriesMap, countriesMapNumber


def generateData(pdMovies, countriesMap={}, countriesMapNumber=0):
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
    return (trainingData, targetData, countriesMap, countriesMapNumber)


def createTree(movieData):
    countriesMap = {}
    countriesMapNumber = 0

    train, target, countriesMap, countriesMapNumber = generateData(movieData)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train, target)

    return (clf, countriesMap, countriesMapNumber)


def makePrediction(movieData, id):
    clf, *countriesInfo = createTree(movieData)
    movieData = pd.DataFrame.from_dict(infoByID(id), orient='index', columns=['title', 'rating', 'original_title', 'budget', 'genres', 'overview',
                                                                              'runtime', 'release_date', 'popularity', 'production_companies', 'production_countries', 'revenue', 'vote_average', 'vote_count'])
    movieData.index.name = 'id'
    moviePredInfo, *countriesInfo = createMovieData(movieData, *countriesInfo)
    return clf.predict([moviePredInfo])
