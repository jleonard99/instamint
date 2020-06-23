import os
import sqlite3
import csv
from instapy.database_engine import get_database

csvfile = "links.csv"

SQL_CREATE_TAGGED_LINKS_ACTIVITY_TABLE = """
    CREATE TABLE IF NOT EXISTS `taggedLinksActivity` (
        `username1` TEXT NOT NULL,
        `last_checked_age_in_hrs` NUMERIC,
        `last_checked_datetime` DATETIME,
        `posted_link` TEXT NOT NULL,
        `posted_link_datetime` DATATIME,
        `posted_link_location_name` TEXT,
        `posted_link_image_text` TEXT,
        `posted_link_likes_count` INTEGER,
        `posted_link_comments_count` INTEGER,
        `posted_by_username` TEXT,
        `posted_by_followers_count` INTEGER,
        `posted_by_following_count` INTEGER );"""

def prepare_my_database(logger):
    db_address,profile_id = get_database()
    try:
        conn = sqlite3.connect(db_address)
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute( SQL_CREATE_TAGGED_LINKS_ACTIVITY_TABLE)

    except Exception as exc:
        conn = conn
        logger.warning(
            "Heeh! Error creating tagged links activity table:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return

def storeTaggedActivitytoDB(
    logger,
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
    db_address,profile_id = get_database()
    try:
        conn = sqlite3.connect(db_address)
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("INSERT INTO taggedLinksActivity VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (username1,
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
                )
            )
            conn.commit()

    except Exception as exc:
        conn = conn
        logger.warning(
            "Error storing tagged activity to DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return


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

def getFreshTaggedLinks( logger ):

        # get a DB, start a connection and sum a server call
    db, profile_id = get_database()
    links = []
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            cur.execute("SELECT posted_link FROM taggedLinksActivity WHERE last_checked_age_in_hrs<=60.0")
            data = cur.fetchall()
            conn.close()
            for d in data:
                links.append( d[0] )

    except Exception as exc:
        conn = conn
        logger.warning(
            "Error storing tagged activity to DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return links
