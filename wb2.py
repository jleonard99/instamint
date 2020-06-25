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



SHEET_ID = "13jCZpVEzYo0iAo3WuBaPxZrtB6curUrhpwZ2sJrlPfg"

FIELDS = ('username', 'last_checked_datetime', 'posted_link',
        'posted_link_datetime', 'posted_link_location_text',
        'posted_link_likes_count', 'posted_link_comments_count',
        'posted_by_username','posted_by_followers_count','posted_by_following_count')
cxn = sqlite3.connect('instapy.db')
cur = cxn.cursor()
rows = cur.execute("SELECT "
                    "username1,"
                    "last_checked_datetime,"
                    "posted_link,"
                    "posted_link_datetime,"
                    "posted_link_location_name,"
                    "posted_link_likes_count,"
                    "posted_link_comments_count,"
                    "posted_by_username,"
                    "posted_by_followers_count,"
                    "posted_by_following_count "
                    "FROM taggedLinksActivity a "
                    "WHERE last_checked_datetime=(select max(last_checked_datetime) from taggedLinksActivity b where a.username1=b.username1 and a.posted_link=b.posted_link) "
                    "ORDER BY username1,posted_link_datetime"
                    ).fetchall()
cxn.close()
rows.insert(0, FIELDS)
data = {'values': [row for row in rows]}

SHEETS.spreadsheets().values().update(spreadsheetId=SHEET_ID,
    range='A1', body=data, valueInputOption='RAW').execute()
print('Wrote data to Sheet:{}'.format(len(rows)))

#rows = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,
#    range='Sheet1').execute().get('values', [])

#for row in rows:
#    print(row)
