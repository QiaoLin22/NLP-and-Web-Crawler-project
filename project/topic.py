import praw
import time
import csv



reddit = praw.Reddit(client_id='B7R_0Uz49aARVQ',
                     client_secret='Cm4xgbhflZN8HvoYFhJnQossRMc',
                     user_agent='subSentiment')

def get_posts(reddit):

    with open(r"out/dataset.csv", "a") as outfile:
        for submission in reddit.subreddit('movies').top('year', limit=10):
            print(submission.title)
            data = [
                submission.title,
            ]
            writer = csv.writer(outfile)
            writer.writerow(data)





def main():
    '''The main function that calls the other functions.'''
    get_posts(reddit)


if __name__ == '__main__':
    main()