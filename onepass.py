from instapy import InstaPy

from instapy.like_util import check_link
from instapy.like_util import verify_liking
from instapy.like_util import get_links_for_tag
from instapy.like_util import get_links_from_feed
from instapy.like_util import get_tags
from instapy.like_util import get_links_for_location
from instapy.like_util import like_image
from instapy.like_util import like_comment
from instapy.util import get_relationship_counts
from instapy.util import web_address_navigator

from instapy.constants import MEDIA_PHOTO, MEDIA_CAROUSEL, MEDIA_ALL_TYPES
from my_like_util import get_links_for_username
from my_like_util import get_likes
from my_like_util import check_link2

import csv
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
current_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

ctime1 = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
ctime2 = datetime.strptime("2020-06-21T13:21:22.0Z","%Y-%m-%dT%H:%M:%S.%fZ")

deltatime = (ctime2 - ctime1)
deltatime_str = str("{:0.1f}").format(deltatime.seconds / 3600.00)

csvfile = "link.csv"

username = "lovin_the_rva"
password = "yellowbrickroad"

session = InstaPy(username=username, password=password)
session.login()

username1 = "shopthemint"
amount = 500
randomize = False
media = MEDIA_PHOTO
taggedImages = True

try:
   links = get_links_for_username(
    session.browser,
    session.username,
    username1,
    amount,
    session.logger,
    session.logfolder,
    randomize,
    media,
    taggedImages
    )
except NoSuchElementException:
    session.logger.error("Element not found, skipping this username")


for i, link in enumerate(links):

    try:
        inappropriate, user_name, likes_count, comments_count, posting_datetime_str, is_video, reason, scope = check_link2(
            session.browser,
            link,
            session.dont_like,
            session.mandatory_words,
            session.mandatory_language,
            session.is_mandatory_character,
            session.mandatory_character,
            session.check_character_set,
            session.ignore_if_contains,
            session.logger,
        )

        followers_count, following_count = get_relationship_counts(
                session.browser, user_name, session.logger
            )
        if not inappropriate:
#            session.logger.info(
#                "link:{},likes:{},".format(link,likes_count)
#            )
#                "likes:{},".format(likes_count),
#                "comments:{},".format(comments_count),
#                "posting_date:{},".format(posting_datetime_str),
#                "poster:{},".format(user_name),
#                "followers:{},".format(followers_count),
#                "following:{},".format(following_count),
#                )

            now = datetime.now(timezone.utc)
            current_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            ctime1 = datetime.strptime(posting_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            ctime2 = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")

            deltatime = (ctime2 - ctime1)
            deltatime_hrs = deltatime.seconds / 3600.00

            with open(csvfile, 'a', newline='') as f:
                writer = csv.writer(f)
                line = "link:{}, likes:{},".format(link,likes_count)
                writer.writerow([
                    username1,
                    deltatime_hrs,
                    current_datetime,
                    link,
                    likes_count,
                    comments_count,
                    posting_datetime_str,
                    user_name,
                    followers_count,
                    following_count] )

    except NoSuchElementException as err:
        self.logger.error("Invalid Page: {}".format(err))


session.end()
