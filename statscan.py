from onepass import OnePass
from instapy import Settings


Settings.database_location = "C:\\Users\\john\\Projects\\instamint\\instapy.db"

tuples = (
    ("lovin_the_rva", "yellowbrickroad","shopreddress"),
    ("livin_in_rva",  "yellowbrickroad","shopthemint"),
    ("fabulously_rva","yellowbrickroad","thepinklilyboutique")
)

amount = 351

for i,(username,password,username1) in enumerate( tuples ):
    print(i,username,password,username1)
    OnePass( username, password, username1, amount )

