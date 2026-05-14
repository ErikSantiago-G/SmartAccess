#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

#define LED_VERDE 7
#define LED_ROJO 8

MFRC522 mfrc522(SS_PIN, RST_PIN);

// UID autorizado
byte Usuario1[4] = {0x81, 0x8D, 0x16, 0x05};

byte LecturaUID[4];

// Estado del usuario
bool dentro = false;

void setup() {

  Serial.begin(9600);

  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  Serial.println("Sistema RFID listo");
}

void loop() {

  if (!mfrc522.PICC_IsNewCardPresent()) return;

  if (!mfrc522.PICC_ReadCardSerial()) return;

  // Leer UID
  for (byte i = 0; i < 4; i++) {
    LecturaUID[i] = mfrc522.uid.uidByte[i];
  }

  // Imprimir UID
  Serial.print("UID:");

  for (byte i = 0; i < 4; i++) {

    Serial.print(" ");

    if (LecturaUID[i] < 0x10) {
      Serial.print("0");
    }

    Serial.print(LecturaUID[i], HEX);
  }

  // Comparar tarjeta
  if (comparaUID(LecturaUID, Usuario1)) {

    // Toggle ENTRY / EXIT
    if (!dentro) {

      Serial.println(" - Erik Garcia - ENTRY");

      accesoEntrada();

      dentro = true;

    } else {

      Serial.println(" - Erik Garcia - EXIT");

      accesoSalida();

      dentro = false;
    }

  } else {

    Serial.println(" - Desconocido");

    accesoDenegado();
  }

  mfrc522.PICC_HaltA();

  delay(1500);
}

boolean comparaUID(byte lectura[], byte usuario[]) {

  for (byte i = 0; i < 4; i++) {

    if (lectura[i] != usuario[i]) {
      return false;
    }
  }

  return true;
}

void accesoEntrada() {

  // Ambos LEDs parpadean 2 veces
  for (int i = 0; i < 2; i++) {

    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_ROJO, HIGH);

    delay(300);

    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_ROJO, LOW);

    delay(300);
  }
}

void accesoSalida() {

  // Solo LED rojo
  for (int i = 0; i < 2; i++) {

    digitalWrite(LED_ROJO, HIGH);

    delay(300);

    digitalWrite(LED_ROJO, LOW);

    delay(300);
  }
}

void accesoDenegado() {

  for (int i = 0; i < 3; i++) {

    digitalWrite(LED_ROJO, HIGH);

    delay(200);

    digitalWrite(LED_ROJO, LOW);

    delay(200);
  }
}