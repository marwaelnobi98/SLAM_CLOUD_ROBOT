import time
import sys
import datetime
import pickle
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
#allows me to use ObjectId function that searches using the _id
from bson.objectid import ObjectId


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client_mongo = MongoClient("mongodb+srv://mohammedmohhy:alfateam@cloudrobots.p8lyk.mongodb.net/hospital")

#reading the database named hospital for further work using the created db variable
db = client_mongo.hospital

#arrays that will be sent to path planning
robot1_array = [('f','f'),('f','f')]
robot2_array = [('f','f'),('f','f')]
robot3_array = [('f','f'),('f','f')]

robot1_collection = db.robot_1


def robot1_array_func():
	global robot1_array
	global robot1_collection
	for i in range(len(robot1_array)):
		#reading the updated flag and the content of the document
		found_document=robot1_collection.find_one({"index":i},{"_id":0})
		flag_updated = found_document["bed_occupency"]
		x = found_document["x"]
		y = found_document["y"]
		#index of the bed in the array that will be sent to path planning algorithm
		read_index = found_document["index"]
		######################################################################################################################################################
		
		##########################working on the array that will be sent to the path planning algorithm####################
		if flag_updated == 1:
			robot1_array[read_index] = (x,y)
		elif flag_updated == 0:	
			# f in the list that will be sent to the path planning means don't go to this bed
						
			print("flag_updated is :")
			print(flag_updated)
			print("")
			robot1_array[read_index] = ('f','f')
			
		with open('robotPoints.txt', 'wb') as fb:
			pickle.dump(robot1_array,fb)
		time.sleep(0.5)
		print(robot1_array)

while 1:	
	robot1_array_func()
