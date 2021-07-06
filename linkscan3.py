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

                ("fabulous3_rva","yellowbrickroad",None,None,475),    # john3@lowkeylabs.com, 404-247-1582
                ("fabulous10_rva","yellowbrickroad1",None,None,475),  # 404-247-1582
                ("fabulously_rva","yellowbrickroad",None,None,475),   # 3300   #jleonard99@precisiontraffic.com, 804-835-0224
                ("livin_in_rva",  "yellowbrickroad",None,None,475),   # 1100   #jleonard99@gmail, 804-835-0224
                ("fabulous4_rva","yellowbrickroad",None,None,475),    # john4@lowkeylabs.com, 404-247-1582
#                ("fabulous20_rva","yellowbrickroad",None,None,475),  # john20@lowkeylabs.com

#                ("fabulous21_rva","yellowbrickroad",None,None,475),  #john21@lowkeylabs.com
#                ("fabulous22_rva","yellowbrickroad",None,None,475),  #john22@lowkeylabs.com


#                ("fabulous0_rva","yellowbrickroad",None,None,475),  #john0@lowkeylabs.com
#                ("fabulous1_rva","yellowbrickroad",None,None,475),  #john1@lowkeylabs.com
#                ("fabulous2_rva","yellowbrickroad",None,None,475),  #john2@lowkeylabs.com

#                ("fabulous5_rva","yellowbrickroad",None,None,475),  #john5@lowkeylabs.com
#                ("fabulous6_rva","yellowbrickroad",None,None,475),  # john6@lowkeylabs.com
#                ("fabulous7_rva","yellowbrickroad",None,None,475),  #john7@lowkeylabs.com
#                ("fabulous8_rva","yellowbrickroad2",None,None,475), # john8@lowkeylabs.com
#                ("fabulous9_rva","yellowbrickroad2",None,None,475), #john9@lowkeylabs.com  804-835-0224

                ("lovin_the_rva", "yellowbrickroad1",None,None,475)    # 2700  #john@lowkeylabs.com, 404-247-1582
)

##
## For each username, determine recent account usage and set session limits
##

def availableLinks():
    iLinks = 0
    for usernameCount,(username,password,xx,yy,linksPerSession) in enumerate(usernames):
        recentLinks = getRecentSessionActivityFromDB( username )
        iLinks = iLinks + (475 - recentLinks)
    return iLinks

print(f"\n*** Available Links: {availableLinks()}")

##
## build list of recent posts, then filter out links already in DB
##

links = []

for i,(username,password,shoppingsite,imageToFind,linksPerSession) in enumerate( usernames ):

    shoppingsite = "shopthemint"
    linksPerSession = 1800

    if not shoppingsite==None:
        tempLinks = []

        # gather list of recent links.  linksPerSession sets max to retrieve.  Set imageToFind if looking for links after specific image
        if (1):
            fresh_links = getLinksAfterLink( username, password, shoppingsite,imageToFind,linksPerSession)
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

    break
##
##  At this stage, we've got a list of links that need checking.
##  Now, get activity on all user accounts over the past 24 hours and find unused capacity
##

print(f"\n*** Links to process: {len(links)}")

linkCount = 0
for usernameCount,(username,password,xx,yy,linksPerSession) in enumerate(usernames):

    recentLinks = getRecentSessionActivityFromDB( username )
    linksPerSession = min(linksPerSession,475-recentLinks)

    if (linksPerSession>0):

        session = InstaPy(username=username, password=password)
        session.dont_like = ["nsfw"]

        session.login()
        prepare_my_database(session.logger)

        linksOnUserCount = 0
        okToContinue = True
        while linksOnUserCount<linksPerSession and linkCount<len(links) and okToContinue:

            (username1,posted_link) = links[linkCount]
            session.logger.info("Processing link:{}   {}/{}:{}/{}  userLinks:{}/{}  totalLinks: {}/{}".format(posted_link,usernameCount+1,len(usernames),shoppingsite,username,linksOnUserCount+1,linksPerSession,linkCount+1,len(links)))
            okToContinue = gatherAndStoreLinkData( session, username1, posted_link )
            linksOnUserCount += 1
            linkCount +=1

        session.end()

        if linkCount>=len(links):
            break

print("\n*** Links processed: {}".format(linkCount))

availableLinks = 0
for usernameCount,(username,password,xx,yy,linksPerSession) in enumerate(usernames):
    recentLinks = getRecentSessionActivityFromDB( username )
    availableLinks = availableLinks + (475 - recentLinks)

print(f"\n*** Available Links: {availableLinks}")
