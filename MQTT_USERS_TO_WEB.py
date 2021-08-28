import paho.mqtt.client as paho
import time
import sys
import datetime
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
#allows me to use ObjectId function that searches using the _id
from bson.objectid import ObjectId

from threading import Timer

broker="34.70.140.201"  #host name

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client_mongo = MongoClient("mongodb+srv://mohammedmohhy:alfateam@cloudrobots.p8lyk.mongodb.net/hospital")

#reading the database named hospital for further work using the created db variable
db = client_mongo.users

#create client object     
pub_client= paho.Client("user2")
print("connecting to broker host",broker)
pub_client.connect(broker)#connection establishment with broker
users_collection = db.hospitals




########################## reading from database the users that can sign in the website and send the username and password to it#############################33
def UsersToWeb():
		global users_collection
		found_user=users_collection.find_one({"user":str("alphateam")},{"_id":0})
		id=found_user["hospital_id"]
		print(id)
		user=found_user["user"]
		print(user)
		password=found_user["pass"]
		print(password)
		idANDuserAndpassword = id+user+password
		print(idANDuserAndpassword)
		pub_client.publish("hospital/users",str(idANDuserAndpassword))
		Timer(3.0, UsersToWeb).start()
Timer(3.0, UsersToWeb).start()
################################################################################################################################################################