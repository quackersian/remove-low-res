import praw
from prawCreds import client_id, client_secret, username, password, user_agent
reddit = praw.Reddit(client_id=client_id , client_secret=client_secret, username=username, password=password, user_agent=user_agent) 

def main():
    # do some code here



if __name__ == "__main__":
    main()
