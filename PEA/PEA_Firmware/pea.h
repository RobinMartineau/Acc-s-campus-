#ifndef PEA_H
#define PEA_H

#include <Arduino.h>
#include <stdint.h>
#include <Wire.h>
#include <Ethernet.h> 
#include <SPI.h>

extern byte mac[];
extern IPAddress ip;
extern IPAddress serverIp;
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
void sendHttpPost();


#endif
