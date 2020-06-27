from onepass import OnePass
from instapy import Settings
from gettaggedlinks import getTaggedLinks
from my_database_util import storeTaggedLinks
from datetime import datetime, timezone

Settings.database_location = "C:\\Users\\john\\Projects\\instamint\\instapy.db"

tuples = (
    ("lovin_the_rva", "yellowbrickroad","shopreddress"),
    ("livin_in_rva",  "yellowbrickroad","shopthemint"),
    ("fabulously_rva","yellowbrickroad","thepinklilyboutique")
)

amountToQuickscan = 8000   # number of links on tagged page to quickscan
amountToLookup = 450      # max number of links to lookup

username = "livin_in_rva"
username1 = "shopthemint"

now = datetime.now(timezone.utc)
last_checked_datetime_str = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
last_checked_datetime = datetime.strptime(last_checked_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

links = getTaggedLinks(username,"yellowbrickroad",username1,amountToQuickscan)

links = {(username1,last_checked_datetime,link) for link in links }

storeTaggedLinks( links )
