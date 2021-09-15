import pandas as pd
import requests as req
import os
os.chdir('C:/Users/avery/Desktop') 

dataIWant = ['title','original_title','budget','genres','overview','runtime', 'release_date','popularity','production_companies','production_countries','revenue','vote_average','vote_count']

def getApiData(currentApiData, id):
    if currentApiData == {}:
        apiData = req.get('https://api.themoviedb.org/3/movie/'+str(id)+'?api_key=42468d346e59d2685235fee95a344f31').json()
        print('API call made on ' + apiData['title'])
        return apiData
    else:
        # print('Skipping API call.')
        return currentApiData

def populateData(existingData):
    newData = {}

    for id, data in existingData.iterrows():
        apiData = {} 
        newData[id]=[]
        
        if (data.loc['title'] == None) or (data.loc['title'] != data.loc['title']):
            apiData = getApiData(apiData, id)
            newData[id].append(apiData['title'])
        else: 
            newData[id].append(data.loc['title'])
        
        newData[id].append(data.loc['rating'])

        for d in dataIWant[1:]:
            if (data.loc[d] == None) or (data.loc[d] != data.loc[d]):
                apiData = getApiData(apiData, id)
                newData[id].append(apiData[d])
            else:
                newData[id].append(data.loc[d])

    df = pd.DataFrame.from_dict(newData, orient='index', columns=['title','rating','original_title','budget','genres','overview','runtime', 'release_date','popularity','production_companies','production_countries','revenue','vote_average','vote_count'])
    df.to_csv('movies.csv', index_label='id')

def addNewID(existingData, newID, newRating):
    newData = {}

    apiData = req.get('https://api.themoviedb.org/3/movie/'+str(newID)+'?api_key=42468d346e59d2685235fee95a344f31').json()

    newData[newID] = []
    newData[newID].append(apiData['title'])

    if (newRating == 0):
        newData[newID].append(None)
    else:
        newData[newID].append(newRating)

    for d in dataIWant[1:]:
        newData[newID].append(apiData[d])

    newMovie = pd.DataFrame.from_dict(newData, orient='index', columns=['title','rating','original_title','budget','genres','overview','runtime', 'release_date','popularity','production_companies','production_countries','revenue','vote_average','vote_count'])
    newMovie.index.name = 'id'

    newMovie.append(existingData).to_csv('movies.csv', index_label='id')

def updateID(existingData, movieID, newRating = None):
    existingData.loc[movieID, 'rating'] = newRating
    existingData.to_csv('movies.csv', index_label='id')