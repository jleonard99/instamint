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

usernames = (
                ("fabulous8_rva","yellowbrickroad",None,None,475),
                ("fabulous9_rva","yellowbrickroad",None,None,475),
                ("fabulous0_rva","yellowbrickroad",None,None,475),
                ("fabulous1_rva","yellowbrickroad",None,None,475),
                ("fabulous2_rva","yellowbrickroad",None,None,475),
                ("fabulous3_rva","yellowbrickroad",None,None,475),
                ("fabulous4_rva","yellowbrickroad",None,None,475),
                ("fabulous5_rva","yellowbrickroad",None,None,475),
                ("fabulous6_rva","yellowbrickroad",None,None,475),
                ("fabulous7_rva","yellowbrickroad",None,None,475),
                ("livin_in_rva",  "yellowbrickroad","shopthemint",None,474),        # 1100
                ("lovin_the_rva", "yellowbrickroad","shopreddress",None,474),       # 2700
                ("fabulously_rva","yellowbrickroad","thepinklilyboutique",None,474) # 3300
)

##
## For each username, determine recent account usage and set session limits
##

#for i,(username1,password,shoppingsite,imageToFind,linksPerSession) in enumerate( usernames ):
#    recentLinks = getRecentSessionActivityFromDB( username1 )
#    usernames[i][5]=min(linksPerSession,475-recentLinks)

##
##
##

links = []

for i,(username,password,shoppingsite,imageToFind,linksPerSession) in enumerate( usernames ):

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

##
##  At this stage, we've got a list of links that need checking.
##  Now, get activity on all user accounts over the past 24 hours and find unused capacity
##

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
