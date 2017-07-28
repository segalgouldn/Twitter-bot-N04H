import subprocess
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from random import choice, randint


consumer_key = 'INSERT'
consumer_secret = 'INSERT'
access_token = 'INSERT'
access_token_secret = 'INSERT'
account_user_id = 'INSERT'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)


def random_sublist(lst, length):
    start = randint(0, len(lst) - length)
    return lst[start:start + length]


class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print(data)
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user', {}).get('id_str', '') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweet_id = tweet.get('id_str')
            screen_name = tweet.get('user', {}).get('screen_name')
            tweet_text = tweet.get('text')
            
            reply_text = '@' + screen_name + ' '

            cleaned_tweet = tweet_text.replace("@N04H5G", "")
            cleaned_tweet_list = cleaned_tweet.split()
            word_count = len(cleaned_tweet_list)
            
            try:
                if word_count > 9:
                    tweet_sample = " ".join(random_sublist(cleaned_tweet_list, 5))
                    generation_length = abs(110 - len(tweet_sample) - len(reply_text))
                elif word_count > 7:
                    tweet_sample = " ".join(random_sublist(cleaned_tweet_list, 4))
                    generation_length = abs(110 - len(tweet_sample) - len(reply_text))
                elif word_count > 5:
                    tweet_sample = " ".join(random_sublist(cleaned_tweet_list, 3))
                    generation_length = abs(110 - len(tweet_sample) - len(reply_text))
                else:
                    tweet_sample = choice(cleaned_tweet_list)
                    generation_length = abs(70 - len(tweet_sample) - len(reply_text))
            except Exception:
                tweet_sample = cleaned_tweet.split()[0]
                generation_length = abs(70 - len(tweet_sample) - len(reply_text))
            
            generation_command = "th sample.lua -checkpoint train_44000.t7 -length \"" + str(generation_length) + "\" -start_text \"" + tweet_sample + "\" -temperature 0.25 -gpu -1"
            
            final_response = subprocess.getoutput(generation_command)
            
            reply_text += final_response

            # check if response is over 140 char
            if len(reply_text) > 140:
                reply_text = reply_text[0:139] + '…'

            print('Tweet ID: ' + tweet_id)
            print('From: ' + screen_name)
            print('Tweet Text: ' + tweet_sample)
            print('Reply Text: ' + reply_text)

            # If rate limited, the status posts should be queued up and sent on an interval
            twitterApi.update_status(status=reply_text, in_reply_to_status_id=tweet_id)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')