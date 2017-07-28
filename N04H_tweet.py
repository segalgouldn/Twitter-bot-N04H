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
        random_int = randint(0, 4)
        if random_int == 0:
            try:
                selected_original_start = random_sublist(selected_original_tweet.split(), 2)
            except Exception:
                selected_original_start = choice(selected_original_tweet.split())
                
        elif random_int == 1:
            try:
                selected_original_start = random_sublist(selected_original_tweet.split(), 3)
            except Exception:
                selected_original_start = choice(selected_original_tweet.split())
        
        elif random_int == 2:
            try:
                selected_original_start = random_sublist(selected_original_tweet.split(), 4)
            except Exception:
                selected_original_start = choice(selected_original_tweet.split())
        
        elif random_int == 3:
            try:
                selected_original_start = random_sublist(selected_original_tweet.split(), 5)
            except Exception:
                selected_original_start = choice(selected_original_tweet.split())
        
        else:
            selected_original_start = choice(selected_original_tweet.split())
        
        desired_tweet_length = 140 - len(selected_original_start)
        
        command = "th sample.lua -checkpoint train_44000.t7 -length \"" + str(desired_tweet_length) + "\" -start_text \"" + b" ".join([str(s) for s in selected_original_start]).decode("ascii") + "\" -temperature 0.25 -gpu -1"
        final_tweet = subprocess.getoutput(command)
    
        if len(final_tweet) > 140:
            final_tweet = final_tweet[0:139] + '…'
            
        if '/bin/' in final_tweet:
            continue
        
        api.update_status(final_tweet)
        sleep(3600)  # Tweet 24 times per day.


tweet(input_tweets_list)
