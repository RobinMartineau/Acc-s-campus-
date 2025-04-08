#include "pea.h"

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
    deverrouillerGache();
    delay(5000);
 
}
