#ifndef PEA_H
#define PEA_H

#include <Arduino.h>
#include <stdint.h>
#include <Wire.h>
#include <Ethernet.h> 
#include <SPI.h>

extern byte mac[];
extern IPAddress ip;
extern IPAddress serverIP;
extern unsigned int serverPort;
extern char* uid; 
extern EthernetClient client;

extern volatile uint64_t wiegandData;
extern volatile int bitCount;
extern volatile unsigned long lastPulseTime;
extern String cardAddress;

#define D0_PIN PA2
#define D1_PIN PA3
#define WIEGAND_TIMEOUT 50
#define RELAY_PIN PB3
#define BUTTON PB15
#define LED PC13

#define SERVER_PORT 8000

void D0Interrupt();
void D1Interrupt();
void decodeWiegand(uint64_t data, int bitCount);
void printRawWiegandBits();
void setupEthernet();
String sendHttpPost();
void actionReponse(String serverResponse);
void deverrouillerGache();


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

#endif // KEYPAD4X4_H
