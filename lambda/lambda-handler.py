import datetime
import tweepy
import random
import os
from apiclient.discovery import build

# Setup Twitter API Access Using Secrets from Jenkins, otherwise add manually. Be careful !
consumer_key = os.getenv("twit_cons_key")
consumer_secret = os.getenv("twit_cons_sec")
access_token = os.getenv("twit_acc_tok")
access_token_secret = os.getenv("twit_acc_sec")

# Setup You Tube API Access
api_key = os.getenv("yt_api_key")
youtube = build('youtube', 'v3', developerKey=api_key)

def main(event, context):
    video = get_random_channel_video('UCFgZ8AxNf1Bd1C6V5-Vx7kA')
    publictweet(video)


# Retrieve a list of videos using channel ID (courtesy of @IndPythonnista)
def get_random_channel_video(channel_id):
    
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    next_page_token = None
    
    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    randomvideo = (random.choice(videos))
    return randomvideo

# Construct tweet 
def publictweet(video_info):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    subtitle = "Another Great Video from TechSnips!\n@techsnips_io"
    video = video_info['snippet']['resourceId']['videoId']
    title = video_info["snippet"]["title"]
    tweettopublish = title + "\nhttps://www.youtube.com/watch?v=" + video + "\n" + subtitle + "\n" + "#techsnipsTuesday"

    print(tweettopublish)
    api.update_status(tweettopublish)