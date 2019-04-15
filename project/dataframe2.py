import praw
import time
import csv
import pandas as pd
import datetime as dt



reddit = praw.Reddit(client_id='B7R_0Uz49aARVQ',
                     client_secret='Cm4xgbhflZN8HvoYFhJnQossRMc',
                     user_agent='subSentiment')

subreddit = reddit.subreddit('movies')
top_subreddit = subreddit.top()
top_subreddit = subreddit.top(limit=1000)

topics_dict = { "title":[], \
                "score":[], \
                "id":[], \
                "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[], \
                "comment": []}


def getall(top_subreddit):
    i = 0
    for submission in top_subreddit:
        time = dt.datetime.fromtimestamp(submission.created)
        year = str(time).split('-')[0]
        month = str(time).split('-')[1]
        print(year)
        print(month)
        print(i)
        if (year == '2018' and (month == '01' or month == '02' or month == '03')) or (year == '2017' and (month == '06' or month == '07' or month == '08'or month == '09'or month == '10'or month == '11'or month == '12')):
            a = ""
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            print('a')
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                a += comment.body + '&&'
                print('b')
            topics_dict["comment"].append(a)
        i += 1

getall(top_subreddit)

topics_data = pd.DataFrame(topics_dict)

def get_date(created):
    return dt.datetime.fromtimestamp(created)

_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp = _timestamp)

#comment = topics_data["comment"]
#comment.to_csv("dataframe2.csv",index =  None, header= True)

title = topics_data["title"]
title.to_csv("topic1.csv",index =  None, header= True)


