#include <Adafruit_GFX.h>
#include <SPI.h>
#include <WiFi101.h>
#include <Wire.h>
#include <Adafruit_ILI9341.h>
#include <Adafruit_STMPE610.h>

// DEFINE OEF VALUE
#define CTRL(x) ('x' & 0x1F)

// SCREEN PINOUT
#define STMPE_CS 5
#define TFT_CS 1
#define TFT_DC 0

// SCREEN CALIBRATION
#define TS_MINX 150
#define TS_MINY 130
#define TS_MAXX 3800
#define TS_MAXY 4000

// DRAWING VARIABLE
#define PENRADIUS 3
#define COLOR ILI9341_RED

// SSID AND PASSWORD TO WIFI CONNECTION
char ssid[] = "SURFACE_WIFI";
char pass[] = "Surface12345678";

// TOUCH SCREEN AND TFT VARIABLES
Adafruit_STMPE610 ts = Adafruit_STMPE610(STMPE_CS);
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

// SERVER VARIABLES
int status = WL_IDLE_STATUS;
WiFiServer server(23);

// FRAME VARIABLES
int X0, X1, Y0, Y1;

void setup() {
  // START SERIAL PORT
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.println("SERIAL OK");

  // WIFI CONNECTION
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(4000);
  }
  Serial.println("WIFI OK");

  // START SERVER
  server.begin();

  // PRINT IP ADDRESS
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println("SERVER OK");

  // SCREEN INITILIZATION
  tft.begin();
  tft.fillScreen(ILI9341_BLACK);
  ts.begin();
  Serial.println("SCREEN OK");
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      // IF USER TOUCH THE SCREEN
      if (!ts.bufferEmpty()) {
        // GET TOUCH POINT
        TS_Point p = ts.getPoint();

        // SCALE TOUCH POINT
        p.x = map(p.x, TS_MINX, TS_MAXX, 0, tft.width());
        p.y = map(p.y, TS_MINY, TS_MAXY, 0, tft.height());

        // DRAW RED POINT ON THE SCREEN
        if (((p.y-PENRADIUS) > PENRADIUS) && ((p.y+PENRADIUS) < tft.height())) {
          tft.fillCircle(p.x, p.y, PENRADIUS, COLOR);
        }

        // SEND DATA
        if(p.x < 256) {
          X0 = p.x;
          X1 = 0;
        } else {
          X0 = 255;
          X1 = p.x - 255;
        }

        if(p.y < 256) {
          Y0 = p.y;
          Y1 = 0;
        } else {
          Y0 = 255;
          Y1 = p.y - 255;
        }
        Serial.print("X = ");Serial.print(p.x);Serial.print("\tY = ");Serial.println(p.y);
        //client.write('$');  // START
        //client.write('0');  // USER_ID
        client.write(char(X0));  // X0
        client.write('A');  // X1
        client.write('1');  // Y0
        client.write('B');  // Y1
        //client.write('0');  // Condition
        //client.write('1');  // Screen
        //client.write('3');  // Alpha
        //client.write('1');  // Beta
        //client.write('#');  // Stop
        client.write((char)CTRL(Z));  // EOF
      }
    }

    client.stop();
  }
}
