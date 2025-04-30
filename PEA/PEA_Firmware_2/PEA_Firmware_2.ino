
#include "pea.h"

enum ModeAcces {
  MODE_INDEFINI,
  MODE_RFID,
  MODE_DIGICODE
};

ModeAcces modeActuel = MODE_INDEFINI;

const byte rowPins[4] = {PB10, PB9, PB8, PB7};
const byte colPins[4] = {PA10, PA9, PA8, PB11};

const char keys[16] = {
  '1','2','3','A',
  '4','5','6','B',
  '7','8','9','C',
  '*','0','#','D'
};

Keypad4x4 keypad(rowPins, colPins, keys);


// --- Fonction : Lecture code Digicode et envoi ---
void attendreCodeEtEnvoyer() {
  useDigits(); // Affiche "Digicode..."

  String code = keypad.password();

  String reponse = sendHttpPostPassword(code);
  actionResponse(reponse);
}

void deverrouillerGache() {
  Serial.println("Déverrouillage de la gâche...");
  digitalWrite(RELAY_PIN, HIGH);
  delay(10000);
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("Gâche verrouillée.");
}

void menuChoixMode() {
  afficherMessage("1: RFID   2: Digicode");

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

void setup() {
  
  Serial.begin(9600);

  Serial.println("Début du setup...");

  Serial.println("Initialisation des pins...");
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(D0_PIN, INPUT_PULLUP); 
  pinMode(D1_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(TFT_CS, OUTPUT);
  pinMode(ETH_CS, OUTPUT);

  /* On désactive de base les 2 objets SPI */
  digitalWrite(TFT_CS, HIGH); 
  digitalWrite(ETH_CS, HIGH);

  Serial.println("Initialisation des pins fait !");
  Serial.println("Initialisation du keypad...");
  keypad.begin();
  Serial.println("Initialisation du keypad fait !");
  Serial.println("Initialisation de l'OLED...");
  ILIInit();
  Serial.println("Initialisation de l'OLED !");
  
  attachInterrupt(digitalPinToInterrupt(D0_PIN), D0Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(D1_PIN), D1Interrupt, FALLING);
  Serial.println("Lecture brute Wiegand en cours...");
  
  //Ethernet.init(5);
  //IPAddress ip(192,168,248,102);
  //Ethernet.begin(mac,ip);
  //digitalWrite(RELAY_PIN, LOW);

  Serial.println(Ethernet.localIP());
  Serial.println("Connexion au réseaux...");
  setupEthernet();
  Serial.println("Connexion établie !"); 
  delay(2000);
  menuChoixMode();
}



// --- Programme principal ---
void loop() {
  // Toujours assurer la connexion réseau
  String serverResponse = "";
  if (modeActuel == MODE_RFID) {
      String uid = "";
      while (uid == "") {
        
        uid = lireBadge34();     
        delay(10);               
       }
      serverResponse = sendHttpPost(uid);
      actionResponse(serverResponse);
      //music();
      uid = "";
      /* attendreBadgeEtEnvoyer(); */
      delay(2000);
      menuChoixMode();
  }

  else if (modeActuel == MODE_DIGICODE) {
    attendreCodeEtEnvoyer();
    delay(2000);
    menuChoixMode();
  }
  
  
  
}
