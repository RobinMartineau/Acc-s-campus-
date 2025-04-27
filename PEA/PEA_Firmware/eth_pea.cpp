#include "pea.h"

//Définitions
byte mac[] = {0x00, 0x80, 0xE1, 0x12, 0x34, 0x56};
IPAddress serverIP(192, 168, 248, 3);
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

String sendHttpPost(String uidHex)
{
  char macStr[18];  // Format "AA:BB:CC:DD:EE:FF"
  sprintf(macStr, "%02X:%02X:%02X:%02X:%02X:%02X",
          mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  String jsonBody = String("{\"uid\":\"") + uidHex + "\",\"adresse_mac\":\"" + macStr + "\"}";
  String serverResponse;

  Serial.print("Corps JSON construit : ");
  Serial.println(jsonBody);

  Serial.println("Connexion au serveur...");
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connecté au serveur, envoi de la requête HTTP POST...");

    client.println("POST /pea/acces/ HTTP/1.1");
    client.println("Host: 192.168.248.1:8000");
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
    Serial.println("Échec de la connexion au serveur.");
  }

  return serverResponse;
}

String sendHttpPostPassword(String code)
{
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

    client.println("POST /pea/acces/ HTTP/1.1");
    client.println("Host: 192.168.248.1:8000");
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
    Serial.println("Échec de la connexion au serveur.");
  }

  return serverResponse;
}


void actionResponse(String serverResponse){
  if(serverResponse.indexOf("\"autorise\":true") != -1) {
    deverrouillerGache();
  }
  else{
    Serial.println("Pas autorisé à rentrer !");
    } 
}
