#include "pea.h"

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC,TFT_RST);

unsigned long ILIInit(){
  tft.begin(4000000);
  tft.setRotation(3);
  delay(1000);
  tft.fillScreen(ILI9341_WHITE);
  tft.setCursor(15, 30);
  tft.setTextColor(ILI9341_BLACK); 
  tft.setTextSize(4);
  tft.println("Screen OK !");
}

unsigned long verifySetup(){
  tft.fillScreen(ILI9341_WHITE);
  tft.setCursor(15, 30);
  tft.setTextColor(ILI9341_BLACK); 
  tft.setTextSize(5);
  tft.println("Setup OK !");
}

//Les fonctions ILIInit() et verifySetup() sont à placer l'une après l'autre avec le fonction ILIInit en premier.

unsigned long askUser(){
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  
  tft.setCursor(15, 30);
  tft.setTextSize(2);
  tft.print("Utilisez votre");
  tft.setTextColor(ILI9341_RED);
  tft.println(" badge");
  tft.setTextColor(ILI9341_BLACK);
  
  tft.setTextSize(4);
  tft.setCursor(140, 100);
  tft.println("ou");
  
  tft.setTextSize(2);
  tft.setCursor(15, 180);
  tft.print("Tapez votre");
  tft.setTextColor(ILI9341_RED);
  tft.println(" mot de passe");
  tft.setTextColor(ILI9341_BLACK);
}

unsigned long ethSetup(){
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setCursor(15, 30);
  tft.setTextSize(2);
  tft.print("Adresse IP :");

  tft.setTextSize(3);
  tft.setCursor(140, 100);
  tft.println(Ethernet.localIP());
}

unsigned long useDigits(){
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setCursor(15, 30);
  tft.setTextSize(5);
  tft.print("Digicode...");
}

unsigned long useRFID(){
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setCursor(15, 30);
  tft.setTextSize(5);
  tft.print("RFID...");
}

unsigned long writeUID(String uid){
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setCursor(15, 30);
  tft.setTextSize(5);
  tft.print("UID : ");
  tft.print(uid);
}
