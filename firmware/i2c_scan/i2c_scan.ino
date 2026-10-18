#include <Wire.h>
void setup() {
  Serial.begin(115200);
  unsigned long t = millis();
  while (!Serial && millis() - t < 3000);
  Wire.begin(5, 6);  // SDA=D4/GPIO5, SCL=D5/GPIO6
  Wire.setClock(100000);
}
void loop() {
  int found = 0;
  for (uint8_t a = 1; a < 127; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0) {
      Serial.printf("I2C device at 0x%02X\n", a);
      found++;
      if (a == 0x28 || a == 0x29) {
        Wire.beginTransmission(a); Wire.write(0x00); Wire.endTransmission(false);
        Wire.requestFrom(a, (uint8_t)1);
        if (Wire.available()) Serial.printf("  BNO055 CHIP_ID = 0x%02X (expect 0xA0)\n", Wire.read());
      }
    }
  }
  Serial.printf("scan done, %d device(s)\n", found);
  delay(1500);
}
