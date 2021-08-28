#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <EasyStringStream.h>


//////////////
String string_msg = "";
char array_of_characters[8];
float float_msg;
 

 
const char* ssid = "WE_98DB03";
const char* password =  "k6m00183";
const char* mqttServer = "35.226.23.95";
const int mqttPort = 1883;

 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266client2")) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }

  client.subscribe("test");



}
 
void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    
    string_msg += (char)payload[i];
    
    //convet the string msg to an array of characters and determine the size of the array
    string_msg.toCharArray(array_of_characters,string_msg.length()+1);

    //convert the array of characters to a float number
    float_msg = atof(array_of_characters);
    Serial.print(float_msg);
  }
 
  Serial.println();
  Serial.println("-----------------------");
 
}
 
void loop() {
    client.loop();    
}
