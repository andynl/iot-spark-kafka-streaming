#include "DHT.h"
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

#define DHTPIN D7
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "";
const char* password = "";

HTTPClient http; 
WiFiClient client;

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.print(WiFi.localIP());
  dht.begin();
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    
    // put your main code here, to run repeatedly:
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["temp"] = t;
    JSONencoder["humd"] = h;
 
    // JsonArray& values = JSONencoder.createNestedArray("values"); //JSON array
    // values.add(20); //Add value to array
    // values.add(21); //Add value to array
    // values.add(23); //Add value to array
 
    // JsonArray& timestamps = JSONencoder.createNestedArray("timestamps"); //JSON array
    // timestamps.add("10:10"); //Add value to array
    // timestamps.add("10:20"); //Add value to array
    // timestamps.add("10:30"); //Add value to array
 
    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
    // Serial.println(JSONmessageBuffer);

    http.begin(client, "http://b963-103-119-66-139.ngrok.io/update-sensor");
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(JSONmessageBuffer);
    String payload = http.getString();

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();
    
  } else {
    Serial.println("Error in WiFi connection"); 
  }

  delay(2000);
}
