""" Module to build a list of tagged links that go way back! """
from instapy import InstaPy

#from instapy.like_util import check_link
#from instapy.like_util import verify_liking
#from instapy.like_util import get_links_for_tag
#from instapy.like_util import get_links_from_feed
#from instapy.like_util import get_tags
#from instapy.like_util import get_links_for_location
#from instapy.like_util import like_image
#from instapy.like_util import like_comment
#from instapy.util import web_address_navigator

import csv
from datetime import datetime, timezone

from instapy.constants import MEDIA_PHOTO
from instapy.util import get_relationship_counts

from instapy import set_workspace
from instapy.time_util import sleep
from my_like_util import get_links_for_username
from my_like_util import get_likes
from my_like_util import check_link2
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from my_database_util import storeRecord,prepare_my_database, storeTaggedActivitytoDB, getFreshTaggedLinks


def getTaggedLinks( username, password, username1, amountToQuickscan ):

    # start the scan

    session = InstaPy(username=username, password=password)
    session.login()
    prepare_my_database(session.logger)


    # Get "amount" links from username1/tagged images. 
    # This is a fairly light-weight activity, and shouldn't consume any instragram-resources

    randomize = False
    media = MEDIA_PHOTO
    taggedImages = True

    links = []
    try:

    #   build list of links to ignore from the data base:  those recently queried (less than 20 hours old) and those posted more than 72 hours ago.
        ignore_links = getFreshTaggedLinks( username1, session.logger )
        ignore_links = list(dict.fromkeys(ignore_links))
    
        fresh_links = get_links_for_username(
            session.browser,
            session.username,
            username1,
            amountToQuickscan,
            session.logger,
            session.logfolder,
            randomize,
            media,
            taggedImages
        )
#        links = list(set(fresh_links) - set(ignore_links))
        links = fresh_links
        session.logger.info("Links quickscanned: {}".format(len(fresh_links)))
        session.logger.info("Links to ignore: {}".format(len(ignore_links)))

    except NoSuchElementException:
        session.logger.error("Element not found, skipping this username")


    session.end()

    return links
