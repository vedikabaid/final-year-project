from flask import Flask , redirect , flash , request , render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twitterdatabase_setup import Base,Tweet,Hashtags,Url
import json
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import httplib2
from textblob import TextBlob



app = Flask(__name__)
engine = create_engine('sqlite:///twitterdatabase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

Tweets = session.query(Tweet).all()

tweetid = []
tweetlocation = []
latitudemap =[]
longitudemap = []
google_api_key = "AIzaSyDZ8KtdfP5nHKIVw2qeGUYyTrvKteOGDPU"



for t in Tweets:
	if t.user_location:
		try:
			locationString = (t.user_location).replace(" ", "+")
			url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
			h = httplib2.Http()
			result = json.loads(h.request(url,'GET')[1])
			if result['results']:
				latitude = result['results'][0]['geometry']['location']['lat']
    			longitude = result['results'][0]['geometry']['location']['lng']
    			tweetlocation.append(str(t.user_location))
    			tweetid.append(str(t.id))
    			latitudemap.append(latitude)
    			longitudemap.append(longitude)
		except:
			continue

print(len(tweetid))
print(len(tweetlocation))

res = [
    ('Tweetid',tweetid ),
    ('Location' , tweetlocation),
    ('Latitude',latitudemap),
    ('Longitude',longitudemap),
    ]
result = pd.DataFrame.from_items(res)

result.to_csv('locationdata.csv')
