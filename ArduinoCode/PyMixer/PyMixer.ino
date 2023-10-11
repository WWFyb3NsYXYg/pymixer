#include <Adafruit_SSD1306.h>
#include <EncButton.h>
#include <Arduino.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

#define FAST_STEP 10
#define STEP 1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
EncButton eb(4, 3, 2, INPUT, INPUT_PULLUP);

int volume[] = {50, 100, 100, 100, 100 };
int rotation;
int mode = 0;

char app_name[9];

void setup() {
  Serial.begin(115200);
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  eb.setFastTimeout(60);
  eb.setBtnLevel(LOW);
  eb.setClickTimeout(500);

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(30, 0);
  display.print("Main Vol");
  display.setTextSize(5);
  display.setCursor(30, 30);
  display.print(volume[mode]);
  display.display();
}

void loop() {
  eb.tick();

  if (eb.left() || eb.right()) {
    rotation = eb.fast() ? FAST_STEP : STEP;
    volume[mode] += (eb.left() ? -rotation : rotation);

    if (volume[mode] < 0) {
      volume[mode] = 0;
    }

    if (volume[mode] > 100) {
      volume[mode] = 100;
    }
    sendData();
  }

  if (eb.turn()) {

    if (eb.rightH()) {
      mode++;
      if (mode > 4) {
        mode = 4;  // Limit mode to 4
      }
    }
    if (eb.leftH()) {
      mode--;
      if (mode < 0) {
        mode = 0;  // Limit mode to 0
      }
    }

    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(30, 0);

    switch (mode) {
      case 0:
        strcpy(app_name, "Main Vol");
        break;
      case 1:
        strcpy(app_name, "Chrome");
        break;
      case 2:
        strcpy(app_name, "AIMP");
        break;
      case 3:
        strcpy(app_name, "Social");
        break;
      case 4:
        strcpy(app_name, "APP");
        break;
    }

    display.print(app_name);
    display.setTextSize(5);
    display.setCursor(30, 30);

    if (volume[mode] < 10) {
      display.print("0");
    }
    display.print(volume[mode]);
    display.display();
  }
}

void sendData() {
  Serial.print(mode);
  Serial.print(',');
  Serial.print(volume[mode]);
  Serial.print('\n');
}