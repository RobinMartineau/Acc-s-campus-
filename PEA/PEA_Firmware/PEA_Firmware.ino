#include "pea.h"

const byte rowPins[4] = {PB7, PB8, PB9, PB1};
const byte colPins[4] = {PB3, PB4, PB5, PB6};
const char keys[16] = {
  '1','2','3','A',
  '4','5','6','B',
  '7','8','9','C',
  '*','0','#','D'
};

Keypad4x4 keypad(rowPins, colPins, keys);

void deverrouillerGache() {
  Serial.println("Déverrouillage de la gâche...");
  digitalWrite(RELAY_PIN, HIGH);
  delay(10000);
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("Gâche verrouillée.");
}


void setup() {
  Serial.begin(9600);

  
  Serial.println("Début du setup...");
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(D0_PIN, INPUT_PULLUP); 
  pinMode(D1_PIN, INPUT_PULLUP);
  pinMode(BUTTON, INPUT);
  pinMode(LED, OUTPUT);
  
  keypad.begin();
  
  //attachInterrupt(digitalPinToInterrupt(D0_PIN), D0Interrupt, FALLING);
  //attachInterrupt(digitalPinToInterrupt(D1_PIN), D1Interrupt, FALLING);
  //Serial.println("Lecture brute Wiegand en cours...");
  
  Ethernet.init(5);
  IPAddress ip(192,168,252,3);
  Serial.println("Starting ethernet");
  Ethernet.begin(mac,ip);

  Serial.println(Ethernet.localIP());
  Serial.println("Fin du setup !");
}

void loop() {
    delay(1000);
    Serial.println("Mot de passe :");
    String pwd = keypad.password();
    Serial.println(pwd);
 
}
