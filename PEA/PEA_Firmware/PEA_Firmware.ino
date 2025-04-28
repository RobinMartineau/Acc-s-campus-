#include "pea.h"

enum ModeAcces {
  MODE_INDEFINI,
  MODE_RFID,
  MODE_DIGICODE
};

ModeAcces modeActuel = MODE_INDEFINI;



const byte rowPins[4] = {PB10, PB9, PB8, PB7};
const byte colPins[4] = {PB14, PB13, PB12, PB11};
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
  setupEthernet();
  ethSetup();
  delay(2000);
  menuChoixMode();
}

void menuChoixMode() {
  afficherMessage("1: RFID  2: Digicode");

  bool choixFait = false;
  while (!choixFait) {
    char k = keypad.getKey();
    if (k) {
      if (k == '1') {
        modeActuel = MODE_RFID;
        afficherMessage("Mode RFID choisi");
        delay(1000);
        choixFait = true;
      } else if (k == '2') {
        modeActuel = MODE_DIGICODE;
        afficherMessage("Mode Digicode choisi");
        delay(1000);
        choixFait = true;
      } else {
        afficherErreur("Choix invalide");
        delay(1000);
        afficherMessage("1: RFID  2: Digicode");
      }
    }
  }
}

void loop() {
 if (modeActuel == MODE_RFID) {
    useRFID();

    String dataToSend = "";

    // Attente indéfinie d'un badge
    while (dataToSend == "") {
      lireBadge26();
      dataToSend = "40A255C4";
    }

    writeUID(dataToSend);

    String reponseServeur = sendHttpPost(dataToSend);
    if (reponseServeur.indexOf("\"autorise\":true") != -1) {
      deverrouillerGache();
      afficherMessage("Acces Autorise");
    } else {
      afficherErreur("Acces Refuse");
    }

    delay(2000);
    menuChoixMode();  
  }

  else if (modeActuel == MODE_DIGICODE) {
    useDigits();
    String code = keypad.password();

    String reponseServeur = sendHttpPostPassword(code);
    if (reponseServeur.indexOf("\"autorise\":true") != -1) {
      deverrouillerGache();
      afficherMessage("Acces Autorise");
    } else {
      afficherErreur("Acces Refuse");
    }

    delay(2000);
    menuChoixMode();  
  }
}
