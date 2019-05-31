from json import loads
import tweepy
import re

CHIPOTLE_ID = 141341662
# ME_ID = 887544709836677120


def codes(parsed):
    accum = []

    if 'text' in parsed:
        try:
            message = parsed['text'].decode('utf-8', 'ignore')
            words = re.split(' |\"|:|\.|!|\?|,|;|\'|\n|/', str(message))
            print(words)
            for word in words:
                # if bool(re.search(r'\d', word)):  # Ineffective
                if 'FREE' in word:
                    accum.append(word)
        except UnicodeDecodeError:
            print('Cannot decode message')

    return accum


class StreamListener(tweepy.StreamListener):

    def __init__(self, sns_topic, sns):
        self.sns_topic = sns_topic
        self.sns = sns

    def on_data(self, data):
        parsed = loads(data)

        if 'user' in parsed and 'id' in parsed['user']:
            user = parsed['user']['id']

            # if user == CHIPOTLE_ID:
            #     print('CHIPOTLE')
            # else:
            #     print('NOT CHIPOTLE')

            if user == CHIPOTLE_ID:
                detected_codes = codes(parsed)
                for number in detected_codes:
                    self.sns.publish(
                        TopicArn=self.sns_topic,
                        Message=str(number),
                    )

                print(detected_codes)
