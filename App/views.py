from django.shortcuts import render
# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery
# Create your views here.
def getresult(list):
    import pickle
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    filename = 'finalized_model.pkl'
    loaded_model = pickle.load(open(filename, 'rb'))
    vec_file = pickle.load(open("vec_file.pkl", 'rb'))
    comment1_vect = vec_file.transform(list)
    result=loaded_model.predict_proba(comment1_vect)[:,1]
    return result
def getcomment():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCoD2fDoUNW7zq9j1UvcjFpdGnChdRTY8Q"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="G1-8Hgy9z2I"
    )
    response = request.execute()
    cmt=response['items']
    text=[]
    ids=[]
    for i in cmt:
        text.append(i['snippet']['topLevelComment']['snippet']['textDisplay'])
        ids.append(i['id'])
    print(text)
    result=getresult(text)
    for i in range(len(result)):
        if result[i]>0.5:
            print(text[i])

getcomment()

