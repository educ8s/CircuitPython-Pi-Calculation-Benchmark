#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <SPI.h>

#if defined(ARDUINO_RASPBERRY_PI_PICO_W)
  #define TFT_CS        17
  #define TFT_RST       16 
  #define TFT_DC        20
#else
  #define TFT_CS        10
  #define TFT_RST        8 // Or set to -1 and connect to Arduino RESET pin
  #define TFT_DC         9
#endif

unsigned long startTime;
unsigned long endTime;
unsigned long duration;

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup() {

  initDisplay();
  drawUI();
  startTime = millis();
  double pi = calculatePi(20000);
  endTime = millis();
  duration = endTime - startTime;
 
  double execution_time = (float)duration/1000;
  drawResults(pi, execution_time);
}

void drawPercent(float percent){
  tft.fillRect(4,  60, (int)120*percent, 20, ST77XX_YELLOW);
}

void loop() {
  // put your main code here, to run repeatedly:

}

double calculatePi(int n) {

  double pi = 0;

  for (int i = 0; i <= n; i++)

  {

    pi += (1.0 / pow(16, i)) * 

    ((4.0 / (8 * i + 1)) - (2.0 / (8 * i + 4)) - 

    (1.0 / (8 * i + 5)) - (1.0 / (8 * i + 6)));

    if (i%50 == 0) {
      float percent = (float) i/n;
      drawPercent(percent);
    }  
  }

  return pi;
}

void drawText(char *text, uint16_t color, int x, int y) {
  tft.setCursor(x, y);
  tft.setTextColor(color);
  tft.setTextWrap(true);
  tft.print(text);
}

void initDisplay() {
  tft.initR(INITR_BLACKTAB);  
  tft.fillScreen(ST77XX_BLACK);
}

void drawUI() {
  drawText(strdup("Pi Benchmark"), ST77XX_RED, 30, 14);
  tft.drawRect(4, 60, 120, 20, ST77XX_YELLOW);
  tft.drawRect(5, 61, 118, 18, ST77XX_YELLOW);
  tft.drawRect(6, 62, 116, 16, ST77XX_YELLOW);
}

void drawResults(double pi, double execution_time) {
  char result[8]; 
  dtostrf(pi, 7, 5, result);

  char time[5];
  dtostrf(execution_time, 5, 3, time);

  drawText(strdup("Result: "), ST77XX_YELLOW, 20, 120);
  drawText(result, ST77XX_YELLOW, 65, 120);

  drawText(strdup("Time:"), ST77XX_YELLOW, 20, 140);
  drawText(time, ST77XX_YELLOW, 53, 140);
  drawText(strdup("sec"), ST77XX_YELLOW, 87, 140);
}