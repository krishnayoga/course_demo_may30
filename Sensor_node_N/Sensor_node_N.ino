#include "DHT.h"

//Define DHT
#define DHTPIN 7
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int ID = 4;
int counter = 0;

String c = "";
char a;
String cmd;

void setup() {
  Serial.begin(9600);
  c = "'Initialize'";
  dht.begin();
}

void loop(){
  if(Serial.available()){
    int b = Serial.read();
    if(b==90){ //Trigger "X"
      float h = dht.readHumidity(); // Humidity
      float t = dht.readTemperature(); // Celcius
      if (isnan(h) || isnan(t)){
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
      }
      c = "i" + String(ID) + "a" + String(h,1) + "b" + String(t,1);
      Serial.println(c);
      delay(200);
    }
  }
}
