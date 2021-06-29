import praw, imageRemoveConfig, prawCreds, imageio
from datetime import datetime

reddit = praw.Reddit(client_id=prawCreds.client_id, client_secret=prawCreds.client_secret, username=prawCreds.username, password=prawCreds.password, user_agent=prawCreds.user_agent) 
lowResReply = imageRemoveConfig.lowResReply
wrongDomainReply = imageRemoveConfig.wrongDomainReply
subreddit = reddit.subreddit(imageRemoveConfig.subreddit)
lowResPostFlairID = imageRemoveConfig.lowResPostFlairID
wrongDomainPostFlairID = imageRemoveConfig.wrongDomainPostFlairID
imgHeight = 0 
imgWidth = 0

def main():
    if reddit.user.me() != prawCreds.username:
        # if we're here, then we have not logged in correctly.
        print("ERROR - Failed to log in!")
        log("ERROR - Failed to log in.")
        return 

    print(f"INFO - Logged in as {reddit.user.me()}, running {prawCreds.user_agent}")
    log(f"INFO - Logged in as {reddit.user.me()}, running {prawCreds.user_agent}")
    
    
    mods = subreddit.moderator()
    
    #check that the bot has permissions to mod the subreddit.    
    if reddit.user.me() in mods:
        for mod in mods:
            if mod == reddit.user.me().name:
                perms = mod.mod_permissions

                if imageRemoveConfig.neededModPermissions == perms:
                    #bot is a mod and has required permissions, so can continue
                    if imageRemoveConfig.logFullInfo:                        
                        log(f"INFO - {reddit.user.me()} is a mod of {imageRemoveConfig.subreddit} with permissions of {perms}.")

                else:
                    #bot is a mod, but does not have required permissions so can't continue
                    log(f"WARNING - {reddit.user.me()} is a mod of {imageRemoveConfig.subreddit}, but does not have required perms ({imageRemoveConfig.neededModPermissions}). Has {perms} instead.")
                    return

    else:
        #bot is not a mod of the subreddit, so can't continue
        log(f"WARNING - {reddit.user.me()} is NOT a mod of {imageRemoveConfig.subreddit}.")
        return


    for submission in subreddit.stream.submissions():
        if not submission.stickied and not submission.is_self:
        # ignores stickies and self (text only) posts 

            if imageRemoveConfig.logFullInfo:
                log(f"INFO - Checking {submission.id}")

            imgUrl = submission.url

            #check if posts have already been flaired or not
            try:
                postFlair = submission.link_flair_template_id
            except:
                postFlair = None
                continue

            
            if postFlair == imageRemoveConfig.lowResPostFlairID:
                #ignore posts if they have already been flaired as low res
                if imageRemoveConfig.logFullInfo:
                    log(f"INFO - Ignoring {submission.id} as it has already been flaired as low res")
                continue

            elif postFlair == imageRemoveConfig.wrongDomainPostFlairID:
                #ignore posts if they have already been flaired as wrong domain
                if imageRemoveConfig.logFullInfo:
                    log(f"INFO - Ignoring {submission.id} as it has already been flaired as wrong domain")
                continue


            if imageRemoveConfig.checkImgDomain:
                #if bot is configured to check the domain of the image then get the domain of the image
                imgDomain = imgUrl.split("/")[2]

                if imgDomain not in imageRemoveConfig.acceptedDomain:
                    #domain is not an approved domain, so flair it
                    submission.mod.flair(text="Wrong Domain", flair_template_id=wrongDomainPostFlairID)

                    if imageRemoveConfig.removeSubmission:
                        #only remove submissions if configured to do so
                        doRemoveSubmission(submission.id, "domain")

                else:
                    #image was in the right domain
                    if imageRemoveConfig.logFullInfo:
                        log(f"INFO - {submission.id} domain OK")
                
                    
            if imageRemoveConfig.checkResolution:        
                #getting image resolution
                imgInfo = imageio.imread(imgUrl)
                imgHeight = imgInfo.shape[0]
                imgWidth = imgInfo.shape[1]


                if imgHeight < imageRemoveConfig.minHeight or imgWidth < imageRemoveConfig.minWidth:
                    #image width or height does not meet minimum requirements
                    log(f"INFO - {submission.id} - Low Resolution")
                    submission.mod.flair(text="Low Resolution", flair_template_id=lowResPostFlairID)         

                    if imageRemoveConfig.removeSubmission is True:
                        #only remove submissions if configured to do so
                        doRemoveSubmission(submission.id, "resolution")

                else:
                    #image was the right resolution
                    if imageRemoveConfig.logFullInfo:
                        log(f"INFO - {submission.id} resolution OK")



                
def doRemoveSubmission(submissionID, reason):
    """Removes a submission based on reason provided
    :param submission: ID of a reddit submission <str>
    :param reason: reason for submission. One of "resolution" or "domain" <str>
    :return: Nothing.
    """

    if reason == "resolution":        
        submissionID.mod.remove(mod_note="Low Resolution Auto")
        submissionID.mod.send_removal_message(lowResReply, title="Low Resolution Auto Remove", type="private")
        log(f"INFO - Removed {submissionID} for {reason}")

    elif reason == "domain":        
        submissionID.mod.remove(mod_note="Wrong Domain Auto")
        submissionID.mod.send_removal_message(wrongDomainReply, title="Wrong Domain Auto Remove", type="private")
        log(f"INFO - Removed {submissionID} for {reason}")
        

    else:
        log(f"WARNING - Failed to remove {submissionID}, incorrect reason provided - {reason}")
        


#################################################################

def log(text):
    """ Custom logging function. Writes to file specified in config.
    :param text: format <str>, the text to be written to file.
    :return: Nothing, will write to file or print to console if errors.
    """
    try:        
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S ")
        with open(imageRemoveConfig.fileLog, "a") as log:
            log.write("\n")
            log.write(now)
            log.write(text)        
            log.close()
            
    except Exception as e:
        print("Error with log function")
        print(str(e))
#################################################################
if __name__ == "__main__":
    main()
