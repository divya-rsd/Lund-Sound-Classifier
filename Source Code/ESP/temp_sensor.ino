#include <String.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <ThingSpeak.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int oneWireBus = 4;     

String serverName = "http://192.168.131.204:5000/";

char ssid[] = "Jahnavi";
char password[] = "WhySoSerious";

const char* server = "mqtt3.thingspeak.com";

const char* mqttUserName = "GSgKJQIOBzUaGQQIMwUKLy8";

const char* mqttPass = "BV9dbOZMhWEMAdkpZetDH7tR";

const char* clientID = "GSgKJQIOBzUaGQQIMwUKLy8";

int channelNum = 2165400;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

int port = 1883;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(1000);
  }
  ThingSpeak.begin(wifiClient);
  Serial.println(WiFi.localIP());

  Serial.println("WiFi connected");
  mqttClient.setServer(server, port);

  sensors.begin();

}

void loop() {
  if (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT...");
    while (!mqttClient.connect(clientID, mqttUserName, mqttPass)) {
      Serial.print(".");
    }
    Serial.println("Connected to MQTT");
  }
  mqttClient.loop();

  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureF = sensors.getTempFByIndex(0);
  Serial.print(temperatureC);
  Serial.println("ºC");
  Serial.print(temperatureF);
  Serial.println("ºF");

  String dataString = "field4="+String(temperatureC);
  String topicString = "channels/" + String(channelNum) + "/publish";
  
  // sendData("temp", temperatureC);
  mqttClient.publish(topicString.c_str(), dataString.c_str());
  delay(100);
}

void sendData(String type, float data){
  HTTPClient http;
  String route = "post-data";
  String url = serverName+route;

  http.begin(wifiClient, url.c_str());
  // Serial.println(url);
  // http.addHeader("Content-Type", "application/json");
  // int httpResponseCode = http.POST("{\"type\":" + String(type) + ",\"data\":"+String(data));
  // Serial.println(httpResponseCode);
  http.end();
}
