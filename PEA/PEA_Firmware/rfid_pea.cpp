#include "pea.h"

volatile uint64_t wiegandData = 0;
volatile int bitCount = 0;
volatile unsigned long lastPulseTime = 0;
String  cardAddress = "";

void D0Interrupt() {
  wiegandData = (wiegandData << 1);
  bitCount++;
  lastPulseTime = millis();
}

void D1Interrupt() {
  wiegandData = (wiegandData << 1) | 1;
  bitCount++;
  lastPulseTime = millis();
}

void decodeWiegand(uint64_t data, int bitCount) {
 if(bitCount != 44) {
   Serial.println("Erreur : le nombre de bits reçus n'est pas égal à 44.");
   return;
 }
 
 uint64_t cardData = data >> 4;  // Exclure les 4 derniers bits (pour la parité)
 uint8_t xorValue = data & 0xF;  // Récupérer les 4 derniers bits (xor)
 uint8_t calculatedXor = 0;

 // Calcul du XOR
 for (int i = 0; i < 10; i++) {
   uint8_t nibble = (cardData >> ((9 - i) * 4)) & 0xF;
   calculatedXor ^= nibble;
 }

 // Stocker l'adresse en hexadécimal dans la variable cardAddress
 cardAddress = "0x";
 for (int i = 9; i >= 0; i--) {
   uint8_t nibble = (cardData >> (i * 4)) & 0xF;
   if(nibble < 10)
     cardAddress += String(nibble, HEX);
   else
     cardAddress += (char)('A' + nibble - 10);
 }

 Serial.print("Card Data: 0x");
  for (int i = 9; i >= 0; i--) {
    uint8_t nibble = (cardData >> (i * 4)) & 0xF;
    if(nibble < 10)
      Serial.print(nibble);
    else
      Serial.print((char)('A' + nibble - 10));
  }
  
  if(calculatedXor == xorValue) {
    Serial.println(" + Checksum valide.");
  } else {
    Serial.println("Checksum invalide !");
  }
}
void printRawWiegandBits() {
  Serial.print("Trame reçue (");
  Serial.print(bitCount);
  Serial.println(" bits):");
  
  for (int i = bitCount - 1; i >= 0; i--) {
    Serial.print((wiegandData >> i) & 1);
  }
  Serial.println();
  
  wiegandData = 0;
  bitCount = 0;
}
