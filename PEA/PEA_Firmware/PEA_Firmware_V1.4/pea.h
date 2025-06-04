//Définition de PEA_H
#ifndef PEA_H
#define PEA_H


//Inclusion des différentes bibliothèques
#include <Arduino.h>
#include <stdint.h>
#include <Wire.h>
#include <Ethernet.h>
//#include <SSLClient.h> 
#include <SPI.h>
#include "Adafruit_ILI9341.h"
#include "Adafruit_GFX.h"
#include <ArduinoJson.h>
//#include <Fonts/FreeMonoBoldOblique18pt7b.h>

//Déclaration des variables
extern byte mac[];
extern IPAddress ip;
extern char* uid; 
extern const char* SERVER_HOST;
//extern SSLClient tlsClient;
extern Adafruit_ILI9341 tft;
extern volatile uint64_t wiegandData;
extern volatile int bitCount;
extern volatile unsigned long lastPulseTime;

/*================================================================================================================================================
 * Définitions
 *  - Pins du STM32
 *  - Port du serveur
 *  - Période
 */ 
#define D0_PIN PC14
#define D1_PIN PC13
#define BUZZER_PIN PB1
#define WIEGAND34 PA8
#define WIEGAND_TIMEOUT 50

#define RELAY_PIN PB5

#define ETH_CS PA4

#define TFT_DC PA2
#define TFT_CS PA0
#define TFT_MOSI PA7
#define TFT_CLK PA5
#define TFT_RST PA3
#define TFT_MISO PA6

#define SERVER_PORT 443
#define UID_ADDR  0x1FFFF7E8 

/*==============================================================================================================================================
================================================================================================================================================
 * Déclarations des fonctions
 *  
 */
void D0Interrupt();
void D1Interrupt();
void music();
String lireBadge26();
String lireBadge34();
void setupEthernet();
String sendHttpPost(String uidHex);
String sendHttpPostPassword(String code);
int httpGetIDSalle(const String& numSalle);
void makeMacFromUID(byte mac[6]);
void actionResponse(String serverResponse);
void deverrouillerGache();

unsigned long ILIInit();
unsigned long verifySetup();
unsigned long askUser();
unsigned long ethSetup();
unsigned long useRFID();
unsigned long useDigits();
unsigned long writeUID(String uid);

void afficherErreur(String message);
void afficherMessage(String message);
void menuChoixMode();



#endif


/*
 * Déclaration de la classe pour le clavier
 */
 
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
  String numClass();
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
