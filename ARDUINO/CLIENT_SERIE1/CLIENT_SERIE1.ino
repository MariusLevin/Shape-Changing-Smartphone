#include <Adafruit_GFX.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_ILI9341.h>
#include <Adafruit_STMPE610.h>

// DEFINE OEF VALUE
#define CTRL(x) ('x' & 0x1F)

#define SCREEN_NUMBER '2'

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

// TOUCH SCREEN AND TFT VARIABLES
Adafruit_STMPE610 ts = Adafruit_STMPE610(STMPE_CS);
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

void setup() {
  // SCREEN INITILIZATION
  tft.begin();
  tft.fillScreen(ILI9341_BLACK);
  ts.begin();

  // START SERIAL PORT
  Serial.begin(9600);
  while (!Serial);
}

void loop() {
  // IF USER TOUCH THE SCREEN
  if (!ts.bufferEmpty()) {
    // GET TOUCH POINT
    TS_Point p = ts.getPoint();
    Serial.println("touch");

    // SCALE TOUCH POINT
    p.x = map(p.x, TS_MINX, TS_MAXX, 0, tft.width());
    p.y = map(p.y, TS_MINY, TS_MAXY, 0, tft.height());

    // DRAW RED POINT ON THE SCREEN
    tft.fillCircle(p.x, p.y, PENRADIUS, COLOR);
    

    // SEND DATA
    sendData(p);
  }

  // IF CLIENT AVAILABLE
  if(Serial.available()) {
    char c = Serial.read();
    if(c == '0') {
      tft.fillScreen(ILI9341_BLACK);
    }
  }
}

void sendData(TS_Point p) {
  Serial.println("send data");
  // FRAME VARIABLES
  int X0, X1, X2, Y0, Y1, Y2;
  
  X2 = (p.x / 100) + int('0');
  X1 = ((p.x % 100) / 10) + int('0');
  X0 = (p.x % 10) + int('0');
  Y2 = (p.y / 100) + int('0');
  Y1 = ((p.y % 100) / 10) + int('0');
  Y0 = (p.y % 10) + int('0');
  
  Serial.write('$');  // START
  Serial.write(SCREEN_NUMBER);  // SCREEN NUMBER
  Serial.write(char(X2));  // X2
  Serial.write(char(X1));  // X1
  Serial.write(char(X0));  // X0
  Serial.write(char(Y2));  // Y2
  Serial.write(char(Y1));  // Y1
  Serial.write(char(Y0));  // Y0
  //Serial.write((char)CTRL(c));  // EOF
}

