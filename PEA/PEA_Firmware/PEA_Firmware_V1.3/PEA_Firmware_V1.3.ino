
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

  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
    delay(50);
      tft.fillScreen(ILI9341_WHITE);
      tft.setTextColor(ILI9341_BLACK);
      tft.setTextSize(3);
      tft.setCursor(40, 80);
      tft.println("1 : RFID");
      tft.setCursor(40, 120);
      tft.println("2 : DIGICODE");
    digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
    delay(50);
    

  bool choixFait = false;
  while (!choixFait) {
    char k = keypad.getKey();
    if (k) {
      if (k == '1') {
        modeActuel = MODE_RFID;
      digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
      delay(50);
        tft.fillScreen(ILI9341_WHITE);
        tft.setTextColor(ILI9341_BLACK);
        tft.setTextSize(2);
        tft.setCursor(40, 80);
        tft.println("Attente d un badge");
        tft.setCursor(40, 110);
        tft.println("a scanner...");
      digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
      delay(50);
        delay(1000);
        choixFait = true;
        
      } else if (k == '2') {
        modeActuel = MODE_DIGICODE;
      digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
      delay(50);
        tft.fillScreen(ILI9341_WHITE);
        tft.setTextColor(ILI9341_BLACK);
        tft.setTextSize(2);
        tft.setCursor(40, 80);
        tft.println("Passage en mode digicode");
      digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
      delay(50);
        delay(1000);
        choixFait = true;
      } else {
        afficherErreur("Choix invalide");
        delay(1000);
        digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
        delay(50);
          tft.fillScreen(ILI9341_WHITE);
          tft.setTextColor(ILI9341_BLACK);
          tft.setTextSize(3);
          tft.setCursor(40, 80);
          tft.println("1 : RFID");
          tft.setCursor(40, 120);
          tft.println("2 : DIGICODE");
        digitalWrite(TFT_CS, HIGH); /*On choisit TFT*/
        delay(50);
      }
    }
  }
}

void setup() {
  
  Serial.begin(9600);

  Serial.println("Debut du setup...");

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
 // tft.setFont(&FreeMonoBoldOblique18pt7b);
  Serial.println("Initialisation de l'OLED !");
  
  attachInterrupt(digitalPinToInterrupt(D0_PIN), D0Interrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(D1_PIN), D1Interrupt, FALLING);
  //Serial.println("Lecture brute Wiegand en cours...");
  Serial.println("Attribution de l'adresse MAC...");
  makeMacFromUID(mac);
  //for(int i = 0;i < 6;i++){
  //  Serial.print(mac[i] + ";");
  //  if(i == 5){
  //    Serial.println(mac[i]);
  //  }
  //}
  Serial.println("Attribution de l'adresse MAC fait !");
  //Ethernet.init(5);
  //IPAddress ip(192,168,248,102);
  //Ethernet.begin(mac,ip);
  //digitalWrite(RELAY_PIN, LOW);
  delay(50);
  Serial.println("Connexion au réseaux...");
  delay(50);
  setupEthernet();
  delay(50);
  Serial.println("Connexion établie !"); 
  delay(50);
  Serial.println("Récupération de l'ID de la classe...");
  String numClass = keypad.numClass();
  int idSalle = httpGetIDSalle(numClass);
  Serial.println("Récupération de l'ID de la classe fait !");
  Serial.print("ID : ");
  Serial.println(idSalle);
  delay(500);
  Serial.println("Passage en mode menu");
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
      delay(2000);
      menuChoixMode();
  }

  else if (modeActuel == MODE_DIGICODE) {
      String password = keypad.password();
      serverResponse = sendHttpPostPassword(password);
      Serial.println(serverResponse);
      actionResponse(serverResponse);
      
    delay(2000);
    menuChoixMode();
  }
  
  
  
}
