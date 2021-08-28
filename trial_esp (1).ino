#include <ESP8266WiFi.h>
#include <PubSubClient.h>
//#include <cstdlib>
//#include <string>

//declare some global variables for our connections.
const char* ssid = "we98";
const char* password =  "01125698213asd";
const char* mqttServer = "34.70.140.201";
const int mqttPort = 1883;

/*if there was a username & pass to for the server */
//const char* mqttUser = "YourMqttUser";
//const char* mqttPassword = "YourMqttUserPassword";


WiFiClient espClient;            //we will declare an object of class WiFiClient, which allows to establish a connection to a specific IP and port [1].
PubSubClient client(espClient); // We will also declare an object of class PubSubClient, which receives as input of the constructor the previously defined WiFiClient.

 void callback(char* topic, byte* payload, unsigned int length) 
{
  //Serial.print("Message arrived in topic: ");
  //Serial.println(topic);
  //Serial.print("Message:");
  //Serial.println(*payload);
  String value = "";
 String msg;

  int i ;
  
  for (i = 0; i < length; i++) 
  {
     //Serial.println((char)payload[i]);
    value += (char)payload[i];
      Serial.println(i);
  }
  
 /*
     msg=value.c_str();
     Serial.print(msg);
 */
 /*
   for (i = 0; i < length; i++) 
  {
    Serial.print("msg[");
    Serial.print(i);
    Serial.print("] = '");
    Serial.print(value[i]);
    Serial.println("'");
  }
  */
//  printf("%s\n",payload.c_str());
// std::cout<<payload;
}

 
void setup() {


 
 Serial.begin(115200);
 WiFi.begin(ssid, password); //connect to wifi 

 //checking if the wifi is connected or not 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    //Serial.println("Connecting to WiFi..");
  }
  //Serial.println("Connected to the WiFi network");
  
 
  client.setServer(mqttServer, mqttPort);  //we call the setServer method on the PubSubClient object, passing as first argument the address and as second the port. 
  client.setCallback(callback);           //we use the setCallback method on the same object to specify a handling function that is executed when a MQTT message is received.
 
  while (!client.connected()) 
  {
    //Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client")) //unique identifier of our client, which we will call “ESP8266Client”,
    {
      //Serial.println("connected");  
    } 
    else 
    {
      //Serial.print("failed with state ");
      //Serial.print(client.state()); //we can call the state method on the the PubSubClient object, which will return a code with information about why the connection failled [2].
      delay(2000);
    }
  }


//we call the subscribe method, passing as input the name of the topic
client.subscribe("path_robot");

}
 

void loop() 
{
    client.loop();    
}
