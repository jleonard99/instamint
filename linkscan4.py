"""
Use to load historical links a bunch at a time.
"""
from onepass import gatherAndStoreLinkData,getLinksAfterLink
from instapy import InstaPy,Settings
from gettaggedlinks import getTaggedLinks
from my_database_util import storeTaggedLinks,getUnprocessedLinksFromDB,prepare_my_database,getFreshTaggedLinks,getRecentSessionActivityFromDB
from datetime import datetime, timezone

Settings.database_location = "C:\\Users\\john\\Projects\\instamint\\instapy.db"


# changed order 8/2/2020 to reduce number of time-outs.

# shopthemint, pinklily, shopreddress

usernames = (
    ("livin_in_rva",  "yellowbrickroad"),    # jleonard99@gmail, 804-835-0224
    ("fabulous10_rva","yellowbrickroad3"),    # 404-247-1582
    ("fabulous4_rva", "yellowbrickroad"),    # john4@lowkeylabs.com, 404-247-1582
    ("fabulously_rva","yellowbrickroad"),    # jleonard99@precisiontraffic.com, 804-835-0224
    ("fabulous3_rva", "yellowbrickroad"),    # john3@lowkeylabs.com, 404-247-1582
    ("lovin_the_rva", "yellowbrickroad2")     # john@lowkeylabs.com, 404-247-1582
)

shoppingsites = (
    ("shopthemint",2000),
    ("pinklily",4000),
    ("shopreddress",3000)
)

##
## For each username, determine recent account usage and set session limits
##

def availableLinks():
    iLinks = 0
    for usernameCount,(username,password) in enumerate(usernames):
        recentLinks = getRecentSessionActivityFromDB( username )
        iLinks = iLinks + (475 - recentLinks)
    return iLinks

##
## build list of recent posts, then filter out links already in DB
##

print(f"\n*** Available Links: {availableLinks()}")

links = []

for i,(username,password) in enumerate( usernames ):

    if i<len(shoppingsites):
        (shoppingsite,linksPerSession) = shoppingsites[i]

        tempLinks = []

        # gather list of recent links.  linksPerSession sets max to retrieve.  Set imageToFind if looking for links after specific image
        if (1):
            fresh_links = getLinksAfterLink( username, password, shoppingsite,None,linksPerSession)
            # ignore links younger than 20 hours and older than 72 hours
            ignore_links = list(dict.fromkeys(getFreshTaggedLinks( shoppingsite ))) # these are links younger than 20 hours and older than 72 hours
            tempLinks = list(set(fresh_links) - set(ignore_links))

        # Check for any missing links from DB.  Missing links have a posted_link_datetime is NULL
        if (0):
            missingLinks = getUnprocessedLinksFromDB( shoppingsite )
            tempLinks = tempLinks + missingLinks

        # create tuples from list of links and append to list
        tempLinks = list( {(shoppingsite,link) for link in tempLinks } )
        links = links + tempLinks

    

print(f"\n*** Links to process: {len(links)}")
print(f"\n*** Available Links: {availableLinks()}")

##
##  At this stage, we've got a list of links that need checking.
##  Now, get activity on all user accounts over the past 24 hours and find unused capacity
##


linkCount = 0
for usernameCount,(username,password) in enumerate(usernames):

    recentLinks = getRecentSessionActivityFromDB( username )
    linksPerSession = min(475,475-recentLinks)

    if (linksPerSession>0):

        session = InstaPy(username=username, password=password)
        session.dont_like = ["nsfw"]

        session.login()
        prepare_my_database(session.logger)

        linksOnUserCount = 0
        okToContinue = True
        while linksOnUserCount<linksPerSession and linkCount<len(links) and okToContinue:

            (username1,posted_link) = links[linkCount]
            session.logger.info("Processing link:{}   {}/{}:{}/{}  userLinks:{}/{}  totalLinks: {}/{}".format(posted_link,usernameCount+1,len(usernames),username1,username,linksOnUserCount+1,linksPerSession,linkCount+1,len(links)))
            okToContinue = gatherAndStoreLinkData( session, username1, posted_link )
            linksOnUserCount += 1
            linkCount +=1

        session.end()

        if linkCount>=len(links):
            break

print("\n*** Links processed: {}".format(linkCount))

print(f"\n*** Available Links: {availableLinks()}")
