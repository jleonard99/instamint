import os
import sqlite3
import csv
from datetime import datetime, timezone
from instapy import Settings
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
        `posted_by_following_count` INTEGER,
        `posted_by_posts_count` INTEGER );"""

SQL_CREATE_SESSION_ACTIVITY= """
    CREATE TABLE IF NOT EXISTS sessionActivity (
        username1 TEXT NOT NULL,
        activity_datetime DATETIME
    )
"""
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
        print(
            "Error storing tagged activity to DB:\n\t{}".format(
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
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
    posted_link_likes_count,
    posted_link_comments_count,
    posted_by_username,
    posted_by_posts_count,
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
            cursor.execute("INSERT INTO taggedLinksActivity VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (username1,
                last_checked_datetime,
                posted_link,
                posted_link_datetime,
                posted_link_location_name,
                posted_link_likes_count,
                posted_link_comments_count,
                posted_by_username,
                posted_by_followers_count,
                posted_by_following_count,
                posted_by_posts_count
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

def updateTaggedActivitytoDB(
    logger,
    username1,
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
    posted_link_likes_count,
    posted_link_comments_count,
    posted_by_username,
    posted_by_posts_count,
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
            cursor.execute(
                """
                UPDATE taggedLinksActivity 
                SET 
                    last_checked_datetime=?,
                    posted_link_datetime=?,
                    posted_link_location_name=?,
                    posted_link_likes_count=?,
                    posted_link_comments_count=?,
                    posted_by_username=?,
                    posted_by_followers_count=?,
                    posted_by_following_count=?,
                    posted_by_posts_count=?
                WHERE 
                    username1=? 
                    and posted_link=? 
                    and posted_link_datetime is NULL 
                """,
                (last_checked_datetime,
                posted_link_datetime,
                posted_link_location_name,
                posted_link_likes_count,
                posted_link_comments_count,
                posted_by_username,
                posted_by_followers_count,
                posted_by_following_count,
                posted_by_posts_count,
                username1,
                posted_link
                )
            )
            conn.commit()

    except Exception as exc:
        conn = conn
        logger.warning(
            "Error updating tagged activity to DB:\n\t{}".format(
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
    posted_by_posts_count,
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
            posted_by_following_count,
            posted_by_posts_count
        ])


def getFreshTaggedLinks( username ):

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
            cur.execute("""
with tags_cte as (
SELECT
  username1,
  posted_link,
  last_checked_datetime,
  posted_link_datetime
FROM
  taggedLinksActivity a 
WHERE 
  (1=1)
  and not posted_link_datetime is NULL
  and (username1=?)
),
tags_cte2 as (
select
  *
from
  tags_cte a
where
  a.last_checked_datetime = (select max(b.last_checked_datetime) from tags_cte b where a.posted_link=b.posted_link)
),
tags_cte3 as (
select
  posted_link
from
  tags_cte2
where
  1=1
  and (
     ( (julianday(datetime('now')) - julianday(last_checked_datetime))*24 <= 20.0)
     or ( (julianday(datetime('now')) - julianday(posted_link_datetime))*24  >= 72.0)
  )
)
select
  posted_link
from
  tags_cte3
            """,(username,))
            data = cur.fetchall()
            for d in data:
                links.append( d[0] )

    except Exception as exc:
        conn = conn
        print(
            "Error retrieving ignore_list from DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return links

def getUnprocessedLinksFromDB( username1 ):
    # get a DB, start a connection and pull links
    db = Settings.database_location
    links = []
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            cur.execute("""
with x_cte as (
select 
  posted_link 
from 
  taggedLinksActivity a
where 
  a.username1=?
  and a.posted_link_datetime is NULL 
  and not posted_link in (select b.posted_link from taggedLinksActivity b where a.username1=b.username1 and not b.posted_link_datetime is NULL)
)
select * from x_cte
            """,(username1,))
            data = cur.fetchall()
            for d in data:
                links.append( d[0] )

    except Exception as exc:
        conn = conn
        print(
            "Error storing tagged activity to DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return links

def deleteLinkFromDB( session, username1, link ):
    db = Settings.database_location
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            cur.execute("""
delete from taggedLinksActivity where username1=? and posted_link=?
            """,(username1,link))
            session.logger.info("Deleted link from DB: {}".format(link))
            
    except Exception as exc:
        conn = conn
        session.logger.warning(
            "Error deleting link from DB:\n\t{}".format(
                str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return

def updateSessionActivityToDB( session ):

    db = Settings.database_location
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            now = datetime.now(timezone.utc)

            cur.execute("""
insert into sessionActivity values (?,?)
            """,(session.username,now))
            
    except Exception as exc:
        conn = conn
        session.logger.warning(
            "Error updating session activity: {} \n\t{}".format(
                session.username,str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

def getRecentSessionActivityFromDB( username1 ):
    # get a DB, start a connection and pull links
    db = Settings.database_location
    linkCount = 0
    try:
        conn = sqlite3.connect(db)

        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # collect today data
            cur.execute("""
select
 sum(1)
from
  sessionActivity
where
  (1=1)
  and (username1=?)
  and ((julianday(datetime('now')) - julianday(activity_datetime))*24 <= 30.0)
            """,
            (username1,))
            linkCount = cur.fetchall()[0][0]
            linkCount = 0 if linkCount==None else linkCount

    except Exception as exc:
        conn = conn
        print(
            "Error reading session activity to DB: {}\n\t{}".format(
                username1,str(exc).encode("utf-8")
            )
        )

    finally:
        if conn:
            # close the open connection
            conn.close()

    return linkCount
