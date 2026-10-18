// BNO055 -> Adafruit WebSerial 3D viewer, for the Seeed XIAO ESP32S3.
// Based on Adafruit_BNO055/examples/webserial_3d (BSD license).
//
// Wiring: SDA = D4 (GPIO5), SCL = D5 (GPIO6), 3V3, GND. BNO055 address 0x28.
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

constexpr int SDA_PIN = 5;  // D4
constexpr int SCL_PIN = 6;  // D5
constexpr uint8_t BNO055_ADDR = 0x28;  // 0x29 if ADR is pulled high
constexpr unsigned long SAMPLE_PERIOD_MS = 50;

Adafruit_BNO055 bno = Adafruit_BNO055(55, BNO055_ADDR, &Wire);

void setup() {
  Serial.begin(115200);
  unsigned long t = millis();
  while (!Serial && millis() - t < 3000);  // native USB: wait for the host

  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(400000);
  Wire.setTimeOut(50);  // BNO055 stretches the clock

  Serial.println("WebSerial 3D Firmware (XIAO ESP32S3)");
  while (!bno.begin()) {
    Serial.println("No BNO055 detected - check SDA=D4, SCL=D5, 3V3, GND and the I2C address");
    delay(1000);
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}

void loop() {
  sensors_event_t event;
  bno.getEvent(&event);

  // The viewer expects heading, pitch, roll
  Serial.print(F("Orientation: "));
  Serial.print(360 - (float)event.orientation.x);
  Serial.print(F(", "));
  Serial.print((float)event.orientation.y);
  Serial.print(F(", "));
  Serial.println((float)event.orientation.z);

  imu::Quaternion quat = bno.getQuat();
  Serial.print(F("Quaternion: "));
  Serial.print((float)quat.w(), 4);
  Serial.print(F(", "));
  Serial.print((float)quat.x(), 4);
  Serial.print(F(", "));
  Serial.print((float)quat.y(), 4);
  Serial.print(F(", "));
  Serial.println((float)quat.z(), 4);

  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(F("Calibration: "));
  Serial.print(sys);
  Serial.print(F(", "));
  Serial.print(gyro);
  Serial.print(F(", "));
  Serial.print(accel);
  Serial.print(F(", "));
  Serial.println(mag);

  delay(SAMPLE_PERIOD_MS);
}
