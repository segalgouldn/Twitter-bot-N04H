import subprocess
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from random import choice, randint


consumer_key = 'INSERT_YOUR_OWN'
consumer_secret = 'INSERT_YOUR_OWN'
access_token = 'INSERT_YOUR_OWN'
access_token_secret = 'INSERT_YOUR_OWN'
account_user_id = 'INSERT_YOUR_OWN'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)


def random_sublist(lst, length):
    start = randint(0, len(lst) - length)
    return lst[start:start + length]


class ReplyToTweet(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user', {}).get('id_str', '') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweet_id = tweet.get('id_str')
            screen_name = tweet.get('user', {}).get('screen_name')
            tweet_text = tweet.get('text')
            
            reply_text = '@' + screen_name + ' '

            cleaned_tweet = tweet_text.replace("@N04H5G", "").encode()
            cleaned_tweet_list = cleaned_tweet.split()
            word_count = len(cleaned_tweet_list)
            
            if word_count > 2:
                tweet_sample = b" ".join(random_sublist(cleaned_tweet_list, 2))
                generation_length = abs(randint(len(tweet_sample) + len(reply_text), 140) - len(tweet_sample) - len(reply_text))
            else:
                tweet_sample = choice(cleaned_tweet_list)
                generation_length = abs(randint(len(tweet_sample) + len(reply_text), 140) - len(tweet_sample) - len(reply_text))
        
            if tweet_sample == b"":
                generation_command = b"th sample.lua -checkpoint train_44000.t7 -length \"" + str(generation_length).encode() + b"\" -temperature 0.25 -gpu -1"
            
            else:
                generation_command = b"th sample.lua -checkpoint train_44000.t7 -length \"" + str(generation_length).encode() + b"\" -start_text \"" + tweet_sample.decode("utf-8").encode("ascii", "ignore") + b"\" -temperature 0.25 -gpu -1"
            
            final_response = subprocess.getoutput(generation_command)
            
            reply_text += final_response

            # check if response is over 140 char
            if len(reply_text) > 140:
                reply_text = reply_text[0:139] + '…'
            
            print('Tweet ID:'
            print(tweet_id)
            print('From:')
            print(screen_name)
            print('Tweet Text:')
            print(tweet_sample)
            print('Reply Text:'
            print(reply_text)

            # If rate limited, the status posts should be queued up and sent on an interval
            if ('/bin/' not in reply_text) and ('/root/' not in reply_text):
                twitterApi.update_status(status=reply_text, in_reply_to_status_id=tweet_id)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
