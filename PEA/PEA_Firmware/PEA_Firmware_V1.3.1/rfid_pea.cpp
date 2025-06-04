#include "pea.h"

volatile uint64_t wiegandData = 0;
volatile int bitCount = 0;
volatile unsigned long lastPulseTime = 0;

// Interruption sur D0 (LOW = 0)
void D0Interrupt() {
  wiegandData = (wiegandData << 1);
  bitCount++;
  lastPulseTime = millis();
}

// Interruption sur D1 (LOW = 1)
void D1Interrupt() {
  wiegandData = (wiegandData << 1) | 1;
  bitCount++;
  lastPulseTime = millis();
}

String lireBadge34() {
  if (bitCount == 34 && millis() - lastPulseTime > WIEGAND_TIMEOUT) {
    uint32_t data = (wiegandData >> 1) & 0xFFFFFFFF;

    wiegandData = 0;
    bitCount = 0;

    // Découpe les 4 octets
    byte byte1 = (data >> 24) & 0xFF;
    byte byte2 = (data >> 16) & 0xFF;
    byte byte3 = (data >> 8)  & 0xFF;
    byte byte4 =  data        & 0xFF;

    // Réordonne : byte4 byte3 byte2 byte1
    char uidStr[9];
    sprintf(uidStr, "%02X%02X%02X%02X", byte4, byte3, byte2, byte1);
    String uidHex = String(uidStr);

    Serial.print("Badge UID réordonné : ");
    Serial.println(uidHex);

    return uidHex;
  }
  return "";
}

void music(){
  digitalWrite(BUZZER_PIN, HIGH);
  delay(1000);
  digitalWrite(BUZZER_PIN, LOW);
  delay(500);
  for( int i =0; i < 5; i++){
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}
