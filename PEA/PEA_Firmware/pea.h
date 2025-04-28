#ifndef PEA_H
#define PEA_H

#include <Arduino.h>
#include <stdint.h>
#include <Wire.h>
#include <Ethernet.h> 
#include <SPI.h>
#include "Adafruit_ILI9341.h"
#include "Adafruit_GFX.h"

extern byte mac[];
extern IPAddress ip;
extern IPAddress serverIP;
extern unsigned int serverPort;
extern char* uid; 
extern EthernetClient client;

extern volatile uint64_t wiegandData;
extern volatile int bitCount;
extern volatile unsigned long lastPulseTime;

#define D0_PIN PC13
#define D1_PIN PC14
#define WIEGAND34 PA8
#define WIEGAND_TIMEOUT 50

#define RELAY_PIN PB5

#define TFT_DC PA2
#define TFT_CS PA4
#define TFT_MOSI PA7
#define TFT_CLK PA5
#define TFT_RST PA3
#define TFT_MISO PA6

#define SERVER_PORT 8000

void D0Interrupt();
void D1Interrupt();
String lireBadge26();
String lireBadge34();
void setupEthernet();
String sendHttpPost(String uidHex);
String sendHttpPostPassword(String code);
void actionResponse(String serverResponse);
void deverrouillerGache();

unsigned long ILIInit();
unsigned long verifySetup();
unsigned long askUser();
unsigned long ethSetup();
unsigned long useRFID();
unsigned long useDigits();
unsigned long writeUID(String uid);

#endif

#ifndef KEYPAD4X4_H
#define KEYPAD4X4_H

#include <Arduino.h>

class Keypad4x4 {
public:
  Keypad4x4(const byte* rowPins,
            const byte* colPins,
            const char* keymap,
            byte numRows = 4,
            byte numCols = 4);
            
  // À appeler dans setup()
  void begin();

  // Retourne 0 si pas de touche, sinon le caractère pressé
  char getKey();

  String password();

private:
  const byte* _rowPins;
  const byte* _colPins;
  const char* _keymap;
  byte _numRows, _numCols;
  
  void setRowOutput(byte row);
  void setAllColumnsInputPullup();
  int readColumns();
};

#endif
