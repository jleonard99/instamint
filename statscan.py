"""
This utility scans to find the most recent links.  
"""
from onepass import OnePass
from instapy import Settings


Settings.database_location = "C:\\Users\\john\\Projects\\instamint\\instapy.db"

tuples = (
    ("lovin_the_rva", "yellowbrickroad","shopreddress"),
    ("livin_in_rva",  "yellowbrickroad","shopthemint"),
    ("fabulously_rva","yellowbrickroad","thepinklilyboutique")
)

amountToQuickscan = 500   # number of links on tagged page to scroll and review.
amountToLookup = 475     # max number of links to lookup (set to max links that Instagram permits downloaded in a single day.)

for i,(username,password,username1) in enumerate( tuples ):
    OnePass( username, password, username1, amountToQuickscan, amountToLookup, i+1, len(tuples) )

