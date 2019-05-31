import tweepy
import boto3
from data import StreamListener, CHIPOTLE_ID

if __name__ == '__main__':
    sns_topic = ''
    sns_client = boto3.client('sns', region_name='us-east-1')

    consumer_token = ''
    consumer_secret = ''

    access_token = ''
    access_secret = ''

    stream_listener = StreamListener(sns_topic, sns_client)

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    print(api.me().name)

    stream = tweepy.Stream(auth=auth, listener=stream_listener)
    stream.filter(follow=[str(CHIPOTLE_ID)])
