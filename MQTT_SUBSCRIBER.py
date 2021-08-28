import paho.mqtt.client as paho
import time
import sys
import datetime
import pickle
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
db = client_mongo.hospital

#global variables for the callback functions receives the id of the document and the flag value which will be responsible for adding the bed or delete it
robot1_msg = ""
robot2_msg = ""
robot3_msg = ""

robot1_collection = db.robot_1

################callback function for robot1#########################
def on_message_robot1(sub_client, userdata, message):
	###############class to convert single quotes to double quotes############
	class str2(str):
		def __repr__(self):
			return ''.join(('"', super().__repr__()[1:-1], '"'))
	##########################################################################

	###############using the global variables########################
	global db
	global robot1_msg 
	global robot1_x
	global robot1_y
	global robot1_collection
	###############################################################
	
	#reading the messsage that had been received 
	robot1_msg = message.payload.decode("utf-8")
	
	############just checking the received message###############
	print("received data on topic hospital/robot1 :")
	print(robot1_msg) #printing Received message
	print("")
	###########################################################
	
	if robot1_msg == "emergency":
		#send the robot to its home position
		x=1
	else:
		############slicing the id and add or delete flag##########################
		id_recieved = str2(robot1_msg[3:])
		flag_received = robot1_msg[:3]
		##############################################################
	
		#########################adding or deleting from the array that will be sent to path planning #######################################################

		if flag_received == "add":
			robot1_collection.update_one({"id":str(id_recieved)},{"$set": {"bed_occupency": 1}})
		elif flag_received == "del":
			robot1_collection.update_one({"id":str(id_recieved)},{"$set": {"bed_occupency": 0}})
			


		print("id_received is :")
		print(id_recieved)
		print("")
		
		print("flag_received is :")
		print(flag_received)
		print("")


		##################################################################################################################
	
def on_message_robot2(sub_client, userdata, message):
	global robot2_msg 
	robot2_msg = message.payload.decode("utf-8")
	print("received data on topic hospital/robot2 :")
	print(robot2_msg) #printing Received message
	print("")	

def on_message_robot3(sub_client, userdata, message):
	global robot3_msg
	robot3_msg = message.payload.decode("utf-8")
	print("received data on topic hospital/robot3 :")
	print(robot3_msg) #printing Received message
	print("")
'''
def on_message_breakfast(client, userdata, message):
	breakfast_msg = message.payload.decode("utf-8")
	print("received data on topic hospital/breakfast :")
	print(breakfast_msg) #printing Received message
	print("")
'''




#create client object     
sub_client= paho.Client("user2")

print("connecting to broker host",broker)
sub_client.connect(broker)#connection establishment with broker

sub_client.message_callback_add('hospital/robot1', on_message_robot1)
sub_client.message_callback_add('hospital/robot2', on_message_robot2)
sub_client.message_callback_add('hospital/robot3', on_message_robot3)
#client.message_callback_add('hospital/breakfast', on_message_breakfast)


#attach the callback function to recieving a message  
#client.on_message=on_message

print("subscribing begins here")    
sub_client.subscribe("hospital/robot1")#subscribe topic hospital/robot1
sub_client.subscribe("hospital/robot2")
sub_client.subscribe("hospital/robot3")
#client.subscribe("hospital/breakfast")
'''
def bed_avail():
    client.publish("robot1/room1/bed1","ON")
    Timer(3.0, bed_avail).start()

Timer(3.0, bed_avail).start() # after 3 seconds, "hello, world" will be printed
'''


while 1:	
	sub_client.loop_start() #contineously checking for message 



	
	
