from time import sleep
from random import choice, randint

import tweepy
import subprocess


consumer_key = 'INSERT'
consumer_secret = 'INSERT'
access_token = 'INSERT'
access_token_secret = 'INSERT'

tweets_file = open("noah_tweets.txt", encoding="utf8")
tweets_text = tweets_file.read()
tweets_file.close()
input_tweets_list = [s.encode("ascii", "ignore") for s in tweets_text.split("\n\n")]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def random_sublist(lst, length):
    start = randint(0, len(lst) - length)
    return lst[start:start + length]
    

def tweet(tweets_list):
    for i in range(10000):
        selected_original_tweet = choice(tweets_list)
        selected_original_tweet_words = selected_original_tweet.split()
        words_length = len(selected_original_tweet_words)
        if words_length > 2:
            selected_original_start = b" ".join(random_sublist(selected_original_tweet_words, 2))
        else:
            selected_original_start = choice(selected_original_tweet_words)
        
        desired_tweet_length = abs(randint(40, 140) - len(selected_original_start))
        # print(selected_original_start)
        
        if selected_original_start == b"":
            command = b"th sample.lua -checkpoint train_44000.t7 -length \"" + str(desired_tweet_length).encode() + b"\" -temperature 0.25 -gpu -1"
        
        else:
            command = b"th sample.lua -checkpoint train_44000.t7 -length \"" + str(desired_tweet_length).encode() + b"\" -start_text \"" + selected_original_start.decode("utf-8").encode("ascii", "ignore") + b"\" -temperature 0.25 -gpu -1"            
        
        final_tweet = subprocess.getoutput(command)
    
        if len(final_tweet) > 140:
            final_tweet = final_tweet[0:139] + '…'
            
        if (b'/bin/' in final_tweet) or (b'/root/' in final_tweet):
            continue
        
        api.update_status(final_tweet)
        sleep(1800)  # Tweet 48 times per day.


tweet(input_tweets_list)
