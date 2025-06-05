#include "pea.h"


Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC,TFT_RST);

unsigned long ILIInit(){

  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
  delay(50);
  
  tft.begin(4000000);
  tft.setRotation(3);
  delay(1000);
  tft.fillScreen(ILI9341_WHITE);
  tft.setCursor(15, 30);
  tft.setTextColor(ILI9341_BLACK); 
  tft.setTextSize(4);
  tft.println("Screen OK !");
  //tft.drawRGBBitmap(0, 0, image_data_Logo_SaintAubin_ILI9341, 320, 240);
  //delay(3000);
  digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
  delay(50);
}


unsigned long ethSetup(){

  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
  delay(50);
  
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setTextSize(2);
  tft.setCursor(15, 30);
  tft.print("Adresse IP :");
  tft.println(Ethernet.localIP());
  tft.setCursor(30, 30);
  tft.print("Passerelle IP :");
  tft.println(Ethernet.gatewayIP());
  tft.setCursor(45, 30);
  tft.print("DNS :");
  tft.println(Ethernet.dnsServerIP());
  tft.setCursor(60, 30);
  tft.print("Mask :");
  tft.println(Ethernet.subnetMask());

  digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
  delay(50);
}

void afficherErreur(String message) {

  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
  delay(50);
  
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_RED);
  tft.setTextSize(2);
  tft.setCursor(20, 80);
  tft.println(message);

  digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
  delay(50);
}

void afficherMessage(String message){

  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
  delay(50);
  
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setTextSize(2);
  tft.setCursor(20, 80);
  tft.println(message);

  digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
  delay(50);
}
