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
    filename = './App/finalized_model.pkl'
    loaded_model = pickle.load(open(filename, 'rb'))
    vec_file = pickle.load(open("./App/vec_file.pkl", 'rb'))
    comment1_vect = vec_file.transform(list)
    result=loaded_model.predict_proba(comment1_vect)[:,1]
    return result
def getcomment(lnk):
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
        videoId=lnk
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
    print(ids)
    return result,text,ids
def home(request):
    if request.method=="POST":
        link=request.POST['Text']
        link=link.split("/")[-1]
        link=str(link)
        link = link[-11:]
        result,text,ids=getcomment(link)
        toxiccomment=[]
        toxicids=[]
        n=len(text)
        for i in range(len(result)):
            if result[i]>0.5:
                toxiccomment.append(text[i])
                toxicids.append(ids[i])
        m=len(toxiccomment)
        return render(request,'result.html',{'toxiccomment':toxiccomment,'m':m,'n':n})
    return render(request,'index.html')

def deletecomments(list):
    # -*- coding: utf-8 -*-

    # Sample Python code for youtube.comments.setModerationStatus
    # See instructions for running these code samples locally:
    # https://developers.google.com/explorer-help/code-samples#python

    import os

    import google_auth_oauthlib.flow
    import googleapiclient.discovery
    import googleapiclient.errors

    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "static/YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    str1=","
    request = youtube.comments().setModerationStatus(
        id=str1.join(list),
        moderationStatus="heldForReview",
        banAuthor=False
    )
    request.execute()
