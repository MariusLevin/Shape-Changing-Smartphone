#include <SPI.h>
#include <WiFi101.h>

char ssid[] = "XXXX";
char pass[] = "XXXX";

int status = WL_IDLE_STATUS;

WiFiServer server(80);

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
  server.begin();

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}


void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
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

    client.stop();
  }
}
