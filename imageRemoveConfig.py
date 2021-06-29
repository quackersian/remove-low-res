subreddit = "quackers987" #CHANGE THIS
#Multiple subreddits can be specified by joining them with pluses, for example AskReddit+NoStupidQuestions.

fileLog = "imageRemoveLog.txt"
neededModPermissions = ['posts', 'flair']
removeSubmission = False
logFullInfo = False

checkResolution = True
minHeight = 800
minWidth = 800
lowResReply = f"Your submission has been removed as it was deemed to be low resolution (less than {minWidth} x {minHeight})."
lowResPostFlairID = "90320684-d8c4-11eb-8b59-0e83c0f77ef7" #CHANGE THIS

checkImgDomain = False
acceptedDomain = ["i.redd.it", "i.imgur.com"]
wrongDomainReply = f"Your submission has been removed as it was deemed to be posted to a disallowed domain. Allowed domains are {acceptedDomain}"
wrongDomainPostFlairID = "4f78c98a-d8d2-11eb-bf32-0e0b42d5cc2b" #CHANGE THIS