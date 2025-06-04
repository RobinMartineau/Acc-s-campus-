#include "pea.h"

/* Variable utilisé */
byte mac[] = {0x00, 0x80, 0xE1, 0xAA, 0xBB, 0xCC};
//IPAddress serverIP(192, 168, 30, 3);
EthernetClient client;
   



/*==========================================
 * Fonction d'initialisation de l'ethernet
 ===========================================*/
 
void setupEthernet() { 
  
  digitalWrite(ETH_CS, LOW); /*On choisit ETH*/
  delay(50);
  
  Serial.println("Initialisation du W5500...");

  Ethernet.init(ETH_CS);

  // Utilisation IP statique pour éviter les bugs DHCP
  //IPAddress ipFixe(192, 168, 30, 100); // À adapter à ton réseau
  //IPAddress gateway(192, 168, 30, 1);
  //IPAddress subnet(255, 255, 255, 0);
  
  Ethernet.begin(mac);
  delay(500);

  // Vérification matérielle
  switch (Ethernet.hardwareStatus()) {
    case EthernetNoHardware:
      Serial.println("Erreur: Pas de module Ethernet détecté !");
      while (true);
      break;
    case EthernetW5100:
      Serial.println("Module W5100 détecté (mais pas W5500).");
      break;
    case EthernetW5200:
      Serial.println("Module W5200 détecté (mais pas W5500).");
      break;
    case EthernetW5500:
      Serial.println("Module W5500 détecté OK !");
      break;
    default:
      Serial.println("Module Ethernet inconnu détecté.");
      break;
  }
  /*Vérification de la précense du câble*/
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Erreur : Pas de câble Ethernet !");
    afficherErreur("Câble absent !");
    while (true);
  }

  /* Affichage série */
  IPAddress ip = Ethernet.localIP();
  Serial.print("Adresse IP : ");
  Serial.println(ip);

  IPAddress gw = Ethernet.gatewayIP();
  Serial.print("Passerelle : ");
  Serial.println(gw);

  IPAddress mask = Ethernet.subnetMask();
  Serial.print("Masque : ");
  Serial.println(mask);

  IPAddress dns = Ethernet.dnsServerIP();
  Serial.print("DNS : ");
  Serial.println(dns);

  // Affichage écran
  Ethernet.maintain();

  Serial.println("Tentative de connexion au serveur...");

  if (client.connect(serverIP, 8000)) {
    Serial.println("Connexion TCP serveur OK !");
    client.stop();
  } else {
    Serial.println("Echec de connexion serveur !");
  }
  
  digitalWrite(ETH_CS, HIGH); /*On choisit ETH*/
  delay(50);
}

/*===========================================================================================
 * 
 * SEND HTTP POST
 * Fontion pour envoyer un badge à l'API
 * 
 ============================================================================================*/

String sendHttpPost(String uidHex)
{
  digitalWrite(TFT_CS, LOW); /*On choisit TFT*/
  delay(50);
  
  tft.fillScreen(ILI9341_WHITE);
  tft.setTextColor(ILI9341_BLACK);
  tft.setTextSize(2);
  tft.setCursor(20, 80);
  tft.println("Envoi des donnees");
  tft.setCursor(20, 110);
  tft.println("au serveur...");
  
  digitalWrite(TFT_CS, HIGH); /*On enlève TFT*/
  delay(1000);
  
  digitalWrite(ETH_CS, LOW); /*On choisit ETH*/
  delay(50);
  
  char macStr[18]; 
  sprintf(macStr, "%02X:%02X:%02X:%02X:%02X:%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  String jsonBody = String("{\"uid\":\"") + uidHex + "\",\"adresse_mac\":\"" + macStr + "\"}";
  String serverResponse;
  

  Serial.print("Corps JSON construit : ");
  Serial.println(jsonBody);

  Serial.println("Connexion au serveur...");
  if (client.connect(serverIP, 8000)) {
    Serial.println("Connecté au serveur, envoi de la requête HTTP POST...");

    client.println("POST /pea/acces/badge HTTP/1.1");
    client.println("Host: 192.168.30.3:8000");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonBody.length());
    client.println("Connection: close");
    client.println();
    client.print(jsonBody);

    unsigned long startTime = millis();
    while (client.connected() && !client.available()) {
      if (millis() - startTime > 10000) {
        Serial.println(">>> Pas de réponse du serveur (timeout)");
        digitalWrite(ETH_CS, HIGH);
        delay(50);
        digitalWrite(TFT_CS, LOW);
        delay(50);
          tft.fillScreen(ILI9341_WHITE);
          tft.setTextColor(ILI9341_RED);
          tft.setTextSize(3);
          tft.setCursor(20, 20);
          tft.println("Erreur : TIMEOUT");
        digitalWrite(TFT_CS, HIGH);
        delay(1000);
        
        break;
        
      }
    }

    Serial.println("Réponse du serveur :");
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
      serverResponse += c;
    }
    bool jsonStarted = false;

  while (client.available()) {
    String line = client.readStringUntil('\n');
    line.trim();

    if (line.startsWith("{")) {  // début du vrai JSON
      serverResponse = line;
      break;
    }
  }

    client.stop();
    Serial.println("\nConnexion fermée.");
  } else {
    Serial.println("Échec de la connexion au serveur.");

        digitalWrite(ETH_CS, HIGH);
        delay(50);
        digitalWrite(TFT_CS, LOW); 
        delay(50);
  
        tft.fillScreen(ILI9341_WHITE);
        tft.setTextColor(ILI9341_RED);
        tft.setTextSize(2);
        tft.setCursor(20, 20);
        tft.println("Erreur : Echec de connexion au serveur");

        digitalWrite(TFT_CS, HIGH); 
        delay(1000);
        
  }

  /*
  digitalWrite(ETH_CS, HIGH); 
  delay(50);

        
        digitalWrite(TFT_CS, LOW);
        delay(50);
  
        tft.fillScreen(ILI9341_WHITE);
        tft.setTextColor(ILI9341_BLACK);
        tft.setTextSize(4);
        tft.setCursor(20, 80);
        tft.println("Erreur : TIMEOUT");

        digitalWrite(TFT_CS, HIGH);
        delay(1000);
        
  

  digitalWrite(TFT_CS, LOW);
  delay(50);
        tft.fillScreen(ILI9341_WHITE);
        tft.setTextColor(ILI9341_BLACK);
        tft.setTextSize(2);
        tft.setCursor(20, 20);
        tft.println("Reponse du serveur : ");
        delay(500);
        tft.setTextColor(ILI9341_GREEN);
        tft.setTextSize(2);
        tft.setCursor(20, 40);
        tft.println(serverResponse);
  digitalWrite(TFT_CS, HIGH);
  delay(1000);
  */

  
  return serverResponse;
}



/*===========================================================================================
 * 
 * SEND HTTP POST
 * Fontion pour envoyer un mot de passe à l'API
 * 
 ============================================================================================*/

String sendHttpPostPassword(String code)
{
  digitalWrite(ETH_CS, LOW); /*On choisit ETH*/
  delay(50);
  
  char macStr[18];  // Format "AA:BB:CC:DD:EE:FF"
  sprintf(macStr, "%02X:%02X:%02X:%02X:%02X:%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  String jsonBody = String("{\"code\":\"") + code + "\",\"adresse_mac\":\"" + macStr + "\"}";
  String serverResponse;

  Serial.print("Corps JSON (mot de passe) : ");
  Serial.println(jsonBody);

  Serial.println("Connexion au serveur...");
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connecté au serveur, envoi de la requête HTTP POST...");

    client.println("POST /pea/acces/digicode HTTP/1.1");
    client.println("Host: 192.168.30.3:8000");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonBody.length());
    client.println("Connection: close");
    client.println();
    client.print(jsonBody);

    unsigned long startTime = millis();
    while (client.connected() && !client.available()) {
      if (millis() - startTime > 5000) {
        Serial.println(">>> Pas de réponse du serveur (timeout)");
        break;
      }
    }

    Serial.println("Réponse du serveur :");
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
      serverResponse += c;
    }

    client.stop();
    Serial.println("\nConnexion fermée.");
  } else {
    Serial.println("Echec de la connexion au serveur.");
  }

  return serverResponse;

  digitalWrite(ETH_CS, HIGH); /*On choisit ETH*/
  delay(50);
}


/*===========================================================================================
 * 
 * ACTION RESPONSE
 * Fontion qui fait suite à la fonction d'envoie d'une requète HTTP
 * 
 ============================================================================================*/

void actionResponse(String serverResponse) {
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, serverResponse);

  if (error) {
    Serial.print("Erreur JSON : ");
    Serial.println(error.f_str());
    afficherErreur("Erreur serveur");
    return;
  }

  bool autorisee = doc["autorisee"];
  String prenom = doc["prenom"] | "";
  String nom    = doc["nom"] | "";
  String role   = doc["role"] | "";

  if (autorisee) {
    Serial.println("Autorisé à entrer !");
    Serial.print("Nom complet : ");
    Serial.println(prenom + " " + nom);
    Serial.print("Rôle : ");
    Serial.println(role);

    digitalWrite(TFT_CS, LOW);
    delay(50);
    tft.fillScreen(ILI9341_WHITE);
    tft.setTextColor(ILI9341_GREEN);
    tft.setTextSize(2);
    tft.setCursor(20, 60);
    tft.print("Bienvenue ");
    tft.println(prenom);
    tft.println(nom);
    tft.setCursor(20, 90);
    tft.print("Role : ");
    tft.println(role);
    tft.setCursor(20, 120);
    tft.println("Porte ouverte");
    digitalWrite(TFT_CS, HIGH);
    delay(50);

    deverrouillerGache();
  } else {
    Serial.println("Pas autorisé à entrer !");
    digitalWrite(TFT_CS, LOW);
    delay(50);
    tft.fillScreen(ILI9341_WHITE);
    tft.setTextColor(ILI9341_RED);
    tft.setTextSize(3);
    tft.setCursor(40, 80);
    tft.println("Acces refuse");
    digitalWrite(TFT_CS, HIGH);
    delay(50);
  }
}
