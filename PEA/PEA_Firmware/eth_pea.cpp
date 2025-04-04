#include "pea.h"

//Définitions
byte mac[] = {0x00, 0x80, 0xE1, 0x12, 0x34, 0x56};
IPAddress serverIP(192, 168, 252, 1);
unsigned int serverPort = 8000;
char* uid = "40A255C4";  
EthernetClient client;

//Fonction d'initialisation
void setupEthernet() {
  Serial.begin(115200);
  while (!Serial) {
  }
  Serial.println("Initialisation du W5500 et DHCP...");

  //pin CS du SPI
  Ethernet.init(PA4);

  if (Ethernet.begin(mac) == 0) {
    Serial.println("Échec de la configuration Ethernet via DHCP");
    while (true) {
    }
  }
  IPAddress ip = Ethernet.localIP();
  IPAddress gw = Ethernet.gatewayIP();
  IPAddress mask = Ethernet.subnetMask();
  IPAddress dns = Ethernet.dnsServerIP();
  Serial.print("Adresse IP obtenue : ");
  Serial.println(ip);
  Serial.print("Masque de sous-reseau : ");
  Serial.println(mask);
  Serial.print("Passerelle : ");
  Serial.println(gw);
  Serial.print("DNS : ");
  Serial.println(dns);
}

void sendHttpPost() {
  char macStr[18];  // Format "AA:BB:CC:DD:EE:FF"
  sprintf(macStr, "%02X:%02X:%02X:%02X:%02X:%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  String jsonBody = String("{\"uid\":\"") + uid + "\",\"adresse_mac\":\"" + macStr + "\"}";
  
  Serial.print("Corps JSON construit : ");
  Serial.println(jsonBody);

  Serial.println("Connexion au serveur...");
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connecté au serveur, envoi de la requête HTTP POST...");

    // Envoi de la requête HTTP POST
    client.println("POST /pea/acces/ HTTP/1.1");
    client.println("Host: 192.168.252.1:8000");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonBody.length());
    client.println("Connection: close");
    client.println();  // Ligne vide pour terminer les en-têtes
    client.print(jsonBody);  // Envoi du corps de la requête

    // Attente de la réponse du serveur (timeout de 5 secondes)
    unsigned long startTime = millis();
    while (client.connected() && !client.available()) {
      if (millis() - startTime > 5000) {
        Serial.println(">>> Pas de réponse du serveur (timeout)");
        break;
      }
    }

    // Lecture et affichage de la réponse du serveur
    Serial.println("Réponse du serveur :");
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
    }

    // Fermeture de la connexion
    client.stop();
    Serial.println("\nConnexion fermée.");
  } else {
    Serial.println("Échec de la connexion au serveur.");
  }
}
