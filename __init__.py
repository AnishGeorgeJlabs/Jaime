author="Pradeep"

import pymongo
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.jaime.authenticate('jaimeApi', 'goldenHead', mechanism='MONGODB-CR')

# hellow
db = dbclient.jaime