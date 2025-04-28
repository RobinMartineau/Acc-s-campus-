#include "pea.h"

const byte rowPins[4] = {PB7, PB8, PB9, PB10};
const byte colPins[4] = {PB11, PB12, PB13, PB14};
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
  pinMode(WIEGAND34, OUTPUT);
  keypad.begin();
  ILIInit();
  
  attachInterrupt(digitalPinToInterrupt(D0_PIN), D0Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(D1_PIN), D1Interrupt, FALLING);
  Serial.println("Lecture brute Wiegand en cours...");
  
  //Ethernet.init(5);
  //IPAddress ip(192,168,248,102);
  //Ethernet.begin(mac,ip);
  //digitalWrite(RELAY_PIN, LOW);

  //Serial.println(Ethernet.localIP());
  Serial.println("Fin du setup !");
  verifySetup();
  delay(1000);
  //ethSetup();
  //delay(2000);
  askUser();
}

void loop() {
  delay(5000);
  // Tente de lire un badge (si la trame est complète et le timeout atteint)
  String uidLu = "30E64AC4";

  if (uidLu != "") {
    // UID détecté, on l'envoie au serveur
    String reponseServeur = sendHttpPost(uidLu);
    
    // Analyse de la réponse : ouvre la gâche si autorisé
    actionResponse(reponseServeur);
    Serial.println(Ethernet.localIP());
  }
  delay(30000);
}
