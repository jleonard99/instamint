"""
Use to load historical links a bunch at a time.
"""
from onepass import gatherAndStoreLinkData,getLinksAfterLink
from instapy import InstaPy,Settings
from gettaggedlinks import getTaggedLinks
from my_database_util import storeTaggedLinks,getUnprocessedLinksFromDB,prepare_my_database
from datetime import datetime, timezone

Settings.database_location = "C:\\Users\\john\\Projects\\instamint\\instapy.db"


usernames = ("lovin_the_rva","livin_in_rva","fabulously_rva")

usernames = ("fabulous0_rva","fabulous1_rva","fabulous2_rva","fabulous3_rva","fabulous4_rva")


#usernames = ("fabulous0_rva","fabulous1_rva","fabulous2_rva","fabulous3_rva","fabulous4_rva","fabulous5_rva","fabulous6_rva","fabulous7_rva","fabulous8_rva","fabulous9_rva")
usernames = ("fabulous3_rva","fabulous4_rva","fabulous5_rva","fabulous6_rva","fabulous7_rva","fabulous8_rva","fabulous9_rva")
password = "yellowbrickroad"
shoppingsite = "shopreddress"


lastInMay = "https://www.instagram.com/p/CA3x6_in-Aq/" #shopreddress
lastInFeb = "https://www.instagram.com/p/B9K4Wp4AFoX/" #shopreddress

lastInMay = "https://www.instagram.com/p/CA05yaFFTlO/" #thepinklilyboutique

lastInMay = "https://www.instagram.com/p/CA3cxHXHaYW/" #shopthemint


shoppingsite = "thepinklilyboutique"
lastInMay = "https://www.instagram.com/p/CA05yaFFTlO/" #thepinklilyboutique
midMarch = "https://www.instagram.com/p/B9lR10iBLoN/"  # 3/15/2020 or so.

##
##
##

shoppingsite = "thepinklilyboutique"

linksPerSession = 475
#print("\nScanning for unprocessed links.  site: {}\n".format(shoppingsite))
missingLinks = getUnprocessedLinksFromDB( shoppingsite )

if (0):
    linksSincePost = getLinksAfterLink( "lovin_the_rva", password, shoppingsite,midMarch,9999)
    links = list(set(linksSincePost).intersection(missingLinks))

links = missingLinks
linkCount = 0

for usernameCount,username in enumerate(usernames):

    session = InstaPy(username=username, password=password)
    session.login()
    prepare_my_database(session.logger)

    linksOnUserCount = 0
    okToContinue = True
    while linksOnUserCount<linksPerSession and linkCount<len(links) and okToContinue:
        username1 = shoppingsite
        posted_link = links[linkCount]
        session.logger.info("Processing link:{}   {}/{}:{}/{}  userLinks:{}/{}  totalLinks: {}/{}".format(posted_link,usernameCount+1,len(usernames),shoppingsite,username,linksOnUserCount+1,linksPerSession,linkCount+1,len(links)))
        okToContinue = gatherAndStoreLinkData( session, username1, posted_link )
        linksOnUserCount += 1
        linkCount +=1

    session.end()

    if linkCount>=len(links):
        break

print("\n*** Links processed: {}".format(linkCount))
