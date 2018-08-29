#include <SPI.h>
#include <WiFi101.h>

char ssid[] = "XXXX";
char pass[] = "XXXX";

int status = WL_IDLE_STATUS;
IPAddress server(192,168,137,203);

WiFiClient client;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);

    delay(4000);
  }
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void loop() {
  if (!client.connected()) {
    Serial.println();
    Serial.println("Starting connection to server...");
    client.connect(server, 80);
    delay(1000);
    if(client.connected()) {
      Serial.println("Connected");
      client.println("Connected");
    }
  } else {
    while(client.available()) {
      char c = client.read();
      Serial.write(c);
    }
    while(Serial.available() > 0) {
      char c = Serial.read();
      client.write(c);
      if(Serial.available() == 0) {
        client.write('\n');
      }
    }
  }
}
