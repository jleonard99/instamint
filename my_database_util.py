import os
import sqlite3
import csv
from instapy.database_engine import get_database

csvfile = "links.csv"

SQL_CREATE_TAGGED_LINKS_ACTIVITY_TABLE = """
    CREATE TABLE IF NOT EXISTS `taggedLinksActivity` (
        `username1` TEXT NOT NULL,
        `last_checked_datetime` DATETIME,
        `posted_link` TEXT NOT NULL,
        `posted_link_datetime` DATATIME,
        `posted_link_location_name` TEXT,
        `posted_link_likes_count` INTEGER,
        `posted_link_comments_count` INTEGER,
        `posted_by_username` TEXT,
        `posted_by_followers_count` INTEGER,
        `posted_by_following_count` INTEGER );"""

def prepare_my_database(logger):
    db_address,profile_id = get_database()
    profile_id = profile_id
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

def storeTaggedLinks(
    tagged_links
):
    db_address,profile_id = get_database()
    profile_id = profile_id
    try:
        conn = sqlite3.connect(db_address)
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO taggedLinksActivity (username1,last_checked_datetime,posted_link) VALUES (?,?,?)",tagged_links)
            conn.commit()
#            logger.info("tagged links stored: {}",cursor.rowcount)
            print("tagged links stored: {}".format(cursor.rowcount))

    except Exception as exc:
        conn = conn
#        logger.warning(
#            "Error storing tagged activity to DB:\n\t{}".format(
#                str(exc).encode("utf-8")
#            )
#        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return


def storeTaggedActivitytoDB(
    logger,
    username1,
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
    posted_link_likes_count,
    posted_link_comments_count,
    posted_by_username,
    posted_by_followers_count,
    posted_by_following_count
):
    db_address,profile_id = get_database()
    profile_id = profile_id
    try:
        conn = sqlite3.connect(db_address)
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("INSERT INTO taggedLinksActivity VALUES (?,?,?,?,?,?,?,?,?,?)",
                (username1,
                last_checked_datetime,
                posted_link,
                posted_link_datetime,
                posted_link_location_name,
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
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
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
            last_checked_datetime,
            posted_link,
            posted_link_datetime,
            "{}".format(posted_link_location_name.encode("utf-8")) if not posted_link_location_name is None else "b'None'",
            posted_link_likes_count,
            posted_link_comments_count,
            posted_by_username,
            posted_by_followers_count,
            posted_by_following_count
        ])


def getFreshTaggedLinks( username,logger ):

        # get a DB, start a connection and sum a server call
    db, profile_id = get_database()
    profile_id = profile_id
    links = []
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            cur.execute(" SELECT posted_link FROM taggedLinksActivity a WHERE"
                        " 1=1"
                        " and username1=?"
                        " and (last_checked_datetime = (select max(last_checked_datetime) from taggedLinksActivity b where a.posted_link=b.posted_link))"
                        " and ("
                        "    ( (julianday(datetime('now')) - julianday(last_checked_datetime))*24 <= 20.0)"
                        " or ( (julianday(datetime('now')) - julianday(posted_link_datetime))*24  >= 72.0)"
                        " )",(username,))
            data = cur.fetchall()
            for d in data:
                links.append( d[0] )

    except Exception as exc:
        conn = conn
        logger.warning(
            "Error retrieving ignore_list from DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return links
