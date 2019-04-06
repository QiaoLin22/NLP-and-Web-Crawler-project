import praw
import csv
from praw.models import MoreComments


reddit = praw.Reddit(client_id='B7R_0Uz49aARVQ',
                     client_secret='Cm4xgbhflZN8HvoYFhJnQossRMc',
                     user_agent='subSentiment')


submission = reddit.submission(url='https://www.reddit.com/r/movies/comments/b951kc/hi_im_trevor_stevens_director_of_the_film_rock/')


submission.comments.replace_more(limit=None)
print(submission.comments)


def get_comments(reddit):
    i = 0
    for submission in reddit.subreddit('movies').top('year',limit=10):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            print(comment.body)

def main():
    '''The main function that calls the other functions.'''
    get_comments(reddit)


if __name__ == '__main__':
    main()