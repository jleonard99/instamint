'''sheets-toys.py -- Google Sheets API demo
    created Jun 2016 by +Wesley Chun/@wescpy
'''
from __future__ import print_function
import sqlite3
import time

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
SHEETS = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

if (0):
    data = {'properties': {'title': 'Tagged Links' }}
    res = SHEETS.spreadsheets().create(body=data).execute()
    SHEET_ID = res['spreadsheetId']
    print('Created "%s"' % res['properties']['title'])

cxn = sqlite3.connect('instapy.db')
cur = cxn.cursor()
rows = cur.execute("""
with RECURSIVE dates(date) AS (
  VALUES('2020-01-01')
  UNION ALL
  SELECT date(date, '+1 day')
  FROM dates
  WHERE date < '2020-12-31'
),
taggedLinks_cte as (
SELECT
    strftime("%Y-%m-%d",posted_link_datetime,'localtime','-1 hours') posted_link_date,
    strftime("%m",posted_link_datetime,'localtime','-1 hours') as month,
    case strftime("%m",posted_link_datetime,'localtime','-1 hours') 
      when '01' then 'Jan'
      when '02' then 'Feb'
      when '03' then 'Mar'
      when '04' then 'Apr'
      when '05' then 'May'
      when '06' then 'Jun'
      when '07' then 'Jul'
      when '08' then 'Aug'
      when '09' then 'Sep'
      when '10' then 'Oct'
      when '11' then 'Nov'
      when '12' then 'Dec'
    end as posted_link_month,
    strftime("%w",posted_link_datetime,'localtime','-1 hours') as dow,
    case strftime("%w",posted_link_datetime,'localtime','-1 hours')
      when '0' then 'Sun'
      when '1' then 'Mon'
      when '2' then 'Tue'
      when '3' then 'Wed'
      when '4' then 'Thu'
      when '5' then 'Fri'
      when '6' then 'Sat'
    end as posted_link_day_of_week,
    username1,
    last_checked_datetime,
    posted_link,
    posted_link_datetime,
    posted_link_location_name,
    posted_link_likes_count,
    posted_link_comments_count,
    posted_by_username,
    posted_by_followers_count,
    posted_by_following_count,
    1 as posted_link_count
FROM
    taggedLinksActivity a 
WHERE 
    1=1
    and not posted_link_datetime is NULL
),
taggedLinks_cte2 as (
select
  a.*
from 
  taggedLinks_cte a
where
   (a.last_checked_datetime=(select max(b.last_checked_datetime) from taggedLinks_cte b where a.username1=b.username1 and a.posted_link=b.posted_link))
)
SELECT
  username1,
  a.date,
  posted_link_count,
  posted_link_likes_count,
  posted_link_comments_count,
  posted_by_username,
  posted_by_followers_count,
  posted_by_following_count,
  month,
  posted_link_month,
  dow,
  posted_link_day_of_week,
  posted_link,
  posted_link_datetime,
  posted_link_location_name,
  last_checked_datetime,
  case when posted_by_followers_count>=50000 then 1 else 0 end as posted_by_plus_50k,
  strftime("%d",posted_link_date)||"-"||posted_link_month as converted_day
FROM
  dates a left join taggedLinks_cte2 b on (a.date=b.posted_link_date)
ORDER BY
    a.date,
    username1,
    posted_link_datetime
""").fetchall()
cxn.close()

SHEET_ID = "13jCZpVEzYo0iAo3WuBaPxZrtB6curUrhpwZ2sJrlPfg"

FIELDS = (
        'shopping site',
        'posted date',
        'posted link count',
        'posted link likes count',
        'posted link comments count',
        'posted by username',
        'posted by followers count',
        'posted by following count',
        'posted link month code',
        'posted link month desc',
        'posted link dow code',
        'posted link dow desc',
        'posted link',
        'posted link datetime',
        'posted link location text',
        'last checked datetime',
        'poster has 50k plus followers',
        'converted day for monthly charts'
        )

rows.insert(0, FIELDS)
data = {'values': [row for row in rows]}

SHEETS.spreadsheets().values().update(spreadsheetId=SHEET_ID,
    range='SourceData!A1', body=data, valueInputOption='RAW').execute()

print('Wrote data to Sheet:{}'.format(len(rows)))

#rows = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,
#    range='Sheet1').execute().get('values', [])

#for row in rows:
#    print(row)
