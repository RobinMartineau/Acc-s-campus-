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

String lireBadge26() {
  if (bitCount == 26 && millis() - lastPulseTime > WIEGAND_TIMEOUT) {
    // Récupère les 26 bits complets tels quels (sans shift ni masquage)
    uint32_t fullData = wiegandData;

    // Réinitialise les données Wiegand
    wiegandData = 0;
    bitCount = 0;

    // Convertit en string hexadécimale majuscule
    String uidHex = String(fullData, HEX);
    uidHex.toUpperCase();

    // Affiche l'UID complet en hexadécimal (les 26 bits)
    Serial.print("Badge détecté - Données brutes (26 bits) : ");
    Serial.println(uidHex);

    return uidHex;
  }

  // Rien à lire
  return "";
}


String lireBadge34() {
  if (bitCount == 34 && millis() - lastPulseTime > WIEGAND_TIMEOUT) {
    // Récupère les 34 bits complets tels quels (sans shift ni masquage)
    uint32_t fullData = wiegandData;

    // Réinitialise les données Wiegand
    wiegandData = 0;
    bitCount = 0;

    // Convertit en string hexadécimale majuscule
    String uidHex = String(fullData, HEX);
    uidHex.toUpperCase();

    // Affiche l'UID complet en hexadécimal (les 34 bits)
    Serial.print("Badge détecté - Données brutes (34 bits) : ");
    Serial.println(uidHex);

    return uidHex;
  }
}
