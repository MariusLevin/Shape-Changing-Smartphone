#include <Adafruit_GFX.h>
#include <SPI.h>
#include <WiFi101.h>
#include <Wire.h>
#include <Adafruit_ILI9341.h>
#include <Adafruit_STMPE610.h>

// DEFINE OEF VALUE
#define CTRL(x) ('x' & 0x1F)

#define SCREEN_NUMBER '1'

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
#define PENRADIUS 1
#define COLOR ILI9341_RED

// SSID AND PASSWORD TO WIFI CONNECTION
char ssid[] = "SURFACE_WIFI";
char pass[] = "Surface12345678";

// TOUCH SCREEN AND TFT VARIABLES
Adafruit_STMPE610 ts = Adafruit_STMPE610(STMPE_CS);
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

// SERVER VARIABLES
int status = WL_IDLE_STATUS;
IPAddress server(192,168,137,93);
WiFiClient client;

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

  // PRINT IP ADDRESS
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println("WIFI OK");

  // SCREEN INITILIZATION
  tft.begin();
  tft.fillScreen(ILI9341_BLACK);
  ts.begin();
  Serial.println("SCREEN OK");
}

void loop() {
  // SERVER CONNECTION
  if (!client.connected()) {
    Serial.println("Starting connection to server...");
    client.connect(server, 23);
    delay(1000);
    if(client.connected()) {
      Serial.println("Connected");
      client.println("0");
    }
  } else {
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
      sendData(p);
    }

    // IF CLIENT AVAILABLE
    if(client.available()) {
      char c = client.read();
      if(c == '0') {
        tft.fillScreen(ILI9341_BLACK);
      }
    }
  }
}

void sendData(TS_Point p) {
  // FRAME VARIABLES
  int X0, X1, X2, Y0, Y1, Y2;
  
  X2 = (p.x / 100) + int('0');
  X1 = ((p.x % 100) / 10) + int('0');
  X0 = (p.x % 10) + int('0');
  Y2 = (p.y / 100) + int('0');
  Y1 = ((p.y % 100) / 10) + int('0');
  Y0 = (p.y % 10) + int('0');
    
  //Serial.print("X = ");Serial.print(p.x);Serial.print("\tY = ");Serial.println(p.y);
  client.write('$');  // START
  client.write(SCREEN_NUMBER);  // SCREEN NUMBER
  client.write(char(X2));  // X2
  client.write(char(X1));  // X1
  client.write(char(X0));  // X0
  client.write(char(Y2));  // Y2
  client.write(char(Y1));  // Y1
  client.write(char(Y0));  // Y0
  //client.write((char)CTRL(Z));  // EOF
}

