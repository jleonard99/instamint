import os
import sqlite3
import csv

csvfile = "links.csv"

def storeRecord(
    username1,
    last_checked_age_in_hrs,
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
    posted_link_image_text,
    posted_link_likes_count,
    posted_link_comments_count,
    posted_by_username,
    posted_by_followers_count,
    posted_by_following_count
):
#    s = "{}".format(posted_link_location_name.encode("utf-8")) if not posted_link_location_name is None else "b'None'"
    with open(csvfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            username1,
            last_checked_age_in_hrs,
            last_checked_datetime,
            posted_link,
            posted_link_datetime,
            "{}".format(posted_link_location_name.encode("utf-8")) if not posted_link_location_name is None else "b'None'",
            "{}".format(posted_link_image_text.encode("utf-8")) if not posted_link_image_text is None else "b'None'",
            posted_link_likes_count,
            posted_link_comments_count,
            posted_by_username,
            posted_by_followers_count,
            posted_by_following_count
        ])

